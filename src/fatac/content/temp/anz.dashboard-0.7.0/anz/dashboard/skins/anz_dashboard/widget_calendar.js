/*
 * SameSpace 4.0
 * Copyright(c) 2006-2010, Anzsoft
 * eastxing@gmail.com
 * 
 */

// reference local blank image
Ext.BLANK_IMAGE_URL = 'ext3/resources/images/default/s.gif';

// create namespace
Ext.namespace( 'Anz', 'Anz.widget' );

Anz.widget.calendar = Ext.extend( Anz.widget.base, {
    iconCls: 'widget_calendar_icon',
    bodyStyle: 'padding: 5px',
    view: 'Month',
    
    // save tips here
    tips: [],
    tipsCfg: [],
    
    getCustomisePreferences: function() {
    	return [{
    		'xtype': 'combo',
    		'name': 'weekStart',
    		'hiddenName': 'weekStart',
    		'fieldLabel': _('Start day of week'),
    		'value': 'Mon',
    		'mode': 'local',
    		'store': {
    			xtype: 'arraystore',
    			fields: ['id', 'name'],
    			data: [['Sun',_('Sun')],['Mon',_('Mon')]]
    		},
    		'displayField': 'name',
    		'valueField': 'id',
    		'triggerAction': 'all',
			'editable': false
    	},{
    		'xtype': 'combo',
    		'name': 'view',
    		'hiddenName': 'view',
    		'fieldLabel': _('View'),
    		'value': 'Month',
    		'mode': 'local',
    		'store': {
    			xtype: 'arraystore',
    			fields: ['id', 'name'],
    			data: [['Month',_('Month')],['Week',_('Week')],['Agenda',_('Agenda')]]
    		},
    		'displayField': 'name',
    		'valueField': 'id',
    		'triggerAction': 'all',
			'editable': false
    	}]
    },
    
    getDefaultValues: function() {
    	return {
    		view: 'Month',
    		weekStart: 'Mon'
    	};
    },
    
    updateOptions: function( options ) {
    	var oldOptions = this.options;
    	this.options = options;
    	
    	this.setTitle( Utf8.decode(options.title) );
    	
    	if( !this.collapsed ) {
    		var oldWeekStart = oldOptions.weekStart;
    		var oldView = oldOptions.view;
    	
	    	if( oldWeekStart !== options.weekStart ) {
		    	this.display();
		    }
		    else if( oldView !== options.view ) {
		    	this.display();
		    }
		}
    },
    
    display: function( date ) {
    	// show load indicator
    	this.body.update( '<div class="loading-indicator">Loading...</div>' );
    	
    	if( !date )
    		date = new Date();
    	
    	this.view = this.getValue( 'view' );
		this.weekStart = this.getValue( 'weekStart' );
		
		// calc event date range
    	var start = null;
    	var end = null;
    	switch( this.view ) {
    		case 'Month':
				start = date.getFirstDateOfMonth();
    			end = date.getLastDateOfMonth();
				break;
			case 'Week':
			case 'Agenda':
				var weekDay = date.format('w');
				if( this.weekStart == 'Sun' ) {
					start = date.add( Date.DAY, -weekDay );
				}
				else {
					if( weekDay == 0 ) {
						start = date.add( Date.DAY, -6 );
					}
					else {
						start = date.add( Date.DAY, 1-weekDay );
					}
				}
				end = start.add( Date.DAY, 6 );
				break;
			default:
				break;
    	}
    	
        Ext.Ajax.request({
        	url: this.contextUrl + '/@@mergedRequest/getMergedData',
    	    method: 'POST',
        	params: { 'requests:list': [
        		'events@@calendarWidget/events?start:date='+start.format('Y/m/d')+'&end:date='+end.format('Y/m/d'),
        		'stateStr@@calendarWidget/getReviewStateString'
        	] },
			timeout: 5000,
    	    scope: this,
    	    success: function ( result, request ) {
				var ret = Ext.decode( result.responseText );
				
				var eventsRet = ret.events;
				if( eventsRet.success ) {
					this.eventsInfo = eventsRet.events;
					this.startDate = start;
					
					var stateStrRet = ret.stateStr;
					if( stateStrRet.success )
						this.stateStr = stateStrRet.stateStr;
					
					var html = this.buildContents();
					
					this.destroyEventTips();
					this.body.update( html );
					this.createEventTips();
					
					this.attachListener();
					
					this.loaded = true;
				}
				else {
					if( ret.msg ) {
						this.body.update( ret.msg );
					}
					else {
						// maybe occur timeout issue, show msg to user
						this.body.update( _('Sorry, get data fail, rettry later.') );	
					}
					
					this.retryDisplay();
				}
			},
			failure: function ( result, request ) {
				var ret = result.responseText;
				if( ret ) {
					this.body.update( ret.msg );
				}
				else {
					// maybe occur timeout issue, show msg to user
					this.body.update( _('Sorry, get data fail, rettry later.') );	
				}
				
				this.retryDisplay();
			}
        });
    },
  	
  	attachListener: function() {
  		var view = this.view;
  		switch( view ) {
			case 'Month':
				this.buildMonthListener();
				break;
			case 'Week':
			case 'Agenda':
				this.buildWeekListener();
				break;
			default:
				break;
		}
  	},
  	
  	destroyEventTips: function() {
  		var tips = this.tips;
  		for( var i=0,len=tips.length; i<len; ++i ) {
  			Ext.QuickTips.unregister( tips[i].target );
  		}
  		
  		this.tips = [];
  	},
  	
  	createEventTips: function() {
  		var tipsCfg = this.tipsCfg;
  		for( var i=0,len=tipsCfg.length; i<len; ++i ) {
  			var cfg = tipsCfg[i];
  			var tip = new Ext.ToolTip({
		        target: cfg.target,
		        title: _('Events in this day'),
		        width: 'auto',
		        dismissDelay: 0,
		        html: cfg.html,
		        trackMouse: true
		    });
			
			this.tips.push( tip );
  		}
  		
  		this.tipsCfg = [];
  	},
  	
  	buildMonthListener: function() {
  		var preMonthE = this.body.child( 'a[class=preTimeCycle]' );
  		preMonthE.on( 'click', this.preMonth, this );
  		
  		var nextMonthE = this.body.child( 'a[class=nextTimeCycle]' );
  		nextMonthE.on( 'click', this.nextMonth, this );
  	},
  	
  	preMonth: function() {
  		var preDate = this.startDate.add( Date.MONTH, -1 );
		this.display( preDate );
  	},
  	
  	nextMonth: function() {
  		var nextDate = this.startDate.add( Date.MONTH, 1 );
		this.display( nextDate );
  	},
  	
  	buildWeekListener: function() {
  		var preWeekE = this.body.child( 'a[class=preTimeCycle]' );
  		preWeekE.on( 'click', this.preWeek, this );
  		
  		var nextWeekE = this.body.child( 'a[class=nextTimeCycle]' );
  		nextWeekE.on( 'click', this.nextWeek, this );
  	},
  	
  	preWeek: function() {
  		var preDate = this.startDate.add( Date.DAY, -7 );
		this.display( preDate );
  	},
  	
  	nextWeek: function() {
  		var nextDate = this.startDate.add( Date.DAY, 7 );
		this.display( nextDate );
  	},
  	
  	buildContents: function() {
  		var view = this.view;
  		
  		var html = null;
		switch( view ) {
			case 'Month':
				html = this.buildMonthHtml();
				break;
			case 'Week':
				html = this.buildWeekHtml();
				break;
			case 'Agenda':
				html = this.buildAgendaHtml();
				break;
			default:
				html = this.buildMonthHtml();
		}
		return html;
  	},
  	
  	buildMonthHtml: function() {
  		var events = this.eventsInfo;
  		var weekStart = this.weekStart;
  		var startDate = this.startDate;
  		
  		// calc left/right padding days
  		var firstDay = startDate.getFirstDayOfMonth(); // 0-6( Sunday-Saturday )
  		var lastDay = startDate.getLastDayOfMonth();
  		var leftPaddingDays = 0;
  		var rightPaddingDays = 0;
  		if( weekStart === 'Sun' ) {
  			// Sunday is first day of week
  			leftPaddingDays = firstDay;
  			rightPaddingDays = 6 - lastDay;
  		}
  		else {
  			// Monday is first day of week
  			if( firstDay === 0 ) {
  				leftPaddingDays = 6;
  				rightPaddingDays = 0;
  			}
  			else {
  				leftPaddingDays = firstDay - 1;
  				rightPaddingDays = 7 - lastDay;
  			}
  		}
  		
  		var dayCount = startDate.getDaysInMonth();
  		var days = [];
  		
  		// add left padding
  		for( var i=0; i<leftPaddingDays; ++i ) {
			days.push( 0 );
		}
  		
  		// add normal days
  		for( var i=1; i<=dayCount; ++i ) {
			days.push( i );
		}
  		
  		// add right padding
  		for( var i=0; i<rightPaddingDays; ++i ) {
			days.push( 0 );
		}
  		
  		var html = [];
  		var headerT = new Ext.Template(
  			'<div class="calendar_month_view">',
  				'<table class="calendar_header_table"><tbody><tr>',
  					'<td class="alignLeft"><a class="preTimeCycle">&lt;&lt;</a></td>',
  					'<td class="alignCenter">{month}</td>',
  					'<td class="alignRight"><a class="nextTimeCycle">&gt;&gt;</a></td>',
  				'</tr></tbody></table>',
  				'<table class="calendar_table">',
  					'<thead><tr>',
  						'<td class="theader">{day1}</td>',
  						'<td class="theader">{day2}</td>',
  						'<td class="theader">{day3}</td>',
  						'<td class="theader">{day4}</td>',
  						'<td class="theader">{day5}</td>',
  						'<td class="theader">{day6}</td>',
  						'<td class="theader">{day7}</td>',
  					'</tr></thead>',
  					'<tbody>'
		);
		
		if( weekStart === 'Sun' ) {
			html.push( headerT.applyTemplate({
				'month': startDate.format('Y-m'),
				'day1': _('Sun'),
				'day2': _('Mon'),
				'day3': _('Tue'),
				'day4': _('Wed'),
				'day5': _('Thu'),
				'day6': _('Fri'),
				'day7': _('Sat')
			}) );
		}
		else {
			html.push( headerT.applyTemplate({
				'month': startDate.format('Y-m'),
				'day1': _('Mon'),
				'day2': _('Tue'),
				'day3': _('Wed'),
				'day4': _('Thu'),
				'day5': _('Fri'),
				'day6': _('Sat'),
				'day7': _('Sun')
			}) );
		}
		
		
		var blankDayT = new Ext.Template(
			'<td class="{dateCls}" id="date_{id}">{day}</td>'
		);
		
		var dayT = new Ext.Template(
			'<td class="{dateCls}" id="date_{id}">',
				'<a target="_blank" href="{url}">{day}</a>',
				'<img index="0" class="event" src="ext3/resources/images/default/s.gif">',
			'</td>'
		);
		
		var eventT = new Ext.Template(
			'<div class="eventCls"><h6>{title}   {start}-{end}</h6><p>{desc}</p></div>'
		);
		
		for( var i=0,len=days.length; i<len; ++i ) {
			if( (i%7) == 0 ) {
				html.push( '<tr>' );
			}
			
			var day = days[i];
			if( day == 0 ) {
				// padding
				html.push( '<td class="blank_day"></td>' );
			}
			else {
				var dt = startDate.add( Date.DAY, day-1 );
				var weekDay = dt.format('w');
				var isWeekend = false;
				if( weekDay==0 || weekDay==6 )
					isWeekend = true;
				
				var dayEvent = events[dt.format('Ymd')];
				var hasEvent = dayEvent && dayEvent.length;
				
				if( hasEvent ) {
					var dayStr = dt.format('Y/m/d');
					html.push( dayT.applyTemplate({
						dateCls: isWeekend ? 'weekend' : '',
						id: dt.format('Y_m_d'),
						day: day,
						url: this.portalUrl+'/search?'+this.stateStr+'start.query:record:list:date='+dayStr+'+23%3A59%3A59&amp;start.range:record=max&amp;end.query:record:list:date='+dayStr+'+00%3A00%3A00&amp;end.range:record=min'
					}) );
					
					// create tooltip
					var eventHtml = [];
					for( var j=0,eventLen=dayEvent.length; j<eventLen; ++j ) {
						var info = dayEvent[j];
						eventHtml.push( eventT.applyTemplate({
							title: info.title,
							start: info.start,
							end: info.end,
							desc: info.desc
						}) );
					}
					
					this.tipsCfg.push({
						target: 'date_'+dt.format('Y_m_d'),
						html: eventHtml.join('')
					});
				}
				else {
					html.push( blankDayT.applyTemplate({
						dateCls: isWeekend ? 'weekend' : '',
						id: dt.format('Y_m_d'),
						day: day
					}) );
				}
			}
			
			if( (i%7) == 6 ) {
				html.push( '</tr>' );
			}
		}
		
		html.push( '</tbody></table></div>' );
		
		return html.join( '' );
  	},
  	
  	buildWeekHtml: function() {
  		var events = this.eventsInfo;
  		var weekStart = this.weekStart;
  		var start = this.startDate;
  		var end = start.add( Date.DAY, 6 );
  		
  		var html = [];
  		var headerT = new Ext.Template(
  			'<div class="calendar_week_view">',
  				'<table class="calendar_header_table"><tbody><tr>',
  					'<td class="alignLeft"><a class="preTimeCycle">&lt;&lt;</a></td>',
  					'<td class="alignCenter">{range}</td>',
  					'<td class="alignRight"><a class="nextTimeCycle">&gt;&gt;</a></td>',
  				'</tr></tbody></table>',
  				'<table class="calendar_table">',
  					'<thead><tr>',
  						'<td class="theader">{day1}</td>',
  						'<td class="theader">{day2}</td>',
  						'<td class="theader">{day3}</td>',
  						'<td class="theader">{day4}</td>',
  						'<td class="theader">{day5}</td>',
  						'<td class="theader">{day6}</td>',
  						'<td class="theader">{day7}</td>',
  					'</tr></thead>',
  					'<tbody>'
		);
		
		if( weekStart === 'Sun' ) {
			html.push( headerT.applyTemplate({
				range: start.format('Y/m/d') + ' - ' + end.format('Y/m/d'),
				day1: _('Sun'),
				day2: _('Mon'),
				day3: _('Tue'),
				day4: _('Wed'),
				day5: _('Thu'),
				day6: _('Fri'),
				day7: _('Sat')
			}) );
		}
		else {
			html.push( headerT.applyTemplate({
				range: start.format('Y/m/d') + ' - ' + end.format('Y/m/d'),
				day1: _('Mon'),
				day2: _('Tue'),
				day3: _('Wed'),
				day4: _('Thu'),
				day5: _('Fri'),
				day6: _('Sat'),
				day7: _('Sun')
			}) );
		}
		
		var blankDayT = new Ext.Template(
			'<td class="weekDay {dateCls}" id="date_{id}">{day}</td>'
		);
		
		var dayT = new Ext.Template(
			'<td class="weekDay {dateCls}" id="date_{id}">',
				'<a target="_blank" href="{url}">{day}</a>',
				'<img index="0" class="event" src="ext3/resources/images/default/s.gif">',
			'</td>'
		);
		
		var eventT = new Ext.Template(
			'<div class="eventCls"><h6>{title}   {start}-{end}</h6><p>{desc}</p></div>'
		);
		
		for( var i=0; i<7; ++i ) {
			var dt = start.add( Date.DAY, i );
			var weekDay = dt.format('w');
			var isWeekend = false;
			if( weekDay==0 || weekDay==6 )
				isWeekend = true;
			
			var dayEvent = events[dt.format('Ymd')];
			var hasEvent = dayEvent && dayEvent.length;
			
			if( hasEvent ) {
				html.push( dayT.applyTemplate({
					dateCls: isWeekend ? 'weekend' : '',
					id: dt.format('Y_m_d'),
					day: dt.format('d'),
					url: ''
				}) );
			
				var eventHtml = [];
				for( var j=0,eventLen=dayEvent.length; j<eventLen; ++j ) {
					var info = dayEvent[j];
					eventHtml.push( eventT.applyTemplate({
						title: info.title,
						start: info.start,
						end: info.end,
						desc: info.desc
					}) );
				}
				
				this.tipsCfg.push({
					target: 'date_'+dt.format('Y_m_d'),
					html: eventHtml.join('')
				});
			}
			else {
				html.push( blankDayT.applyTemplate({
					dateCls: isWeekend ? 'weekend' : '',
					id: dt.format('Y_m_d'),
					day: dt.format('d')
				}) );
			}
		}
		
		html.push( '</tbody></table></div>' );
		
		return html.join( '' );
  	},
  	
  	buildAgendaHtml: function() {
  		var events = this.eventsInfo;
  		var weekStart = this.weekStart;
  		var start = this.startDate;
  		var end = start.add( Date.DAY, 6 );
  		
  		var html = [];
  		var headerT = new Ext.Template(
  			'<div class="calendar_week_view">',
  				'<table class="calendar_header_table"><tbody><tr>',
  					'<td class="alignLeft"><a class="preTimeCycle">&lt;&lt;</a></td>',
  					'<td class="alignCenter">{range}</td>',
  					'<td class="alignRight"><a class="nextTimeCycle">&gt;&gt;</a></td>',
  				'</tr></tbody></table>',
  				'<div class="">'
		);
		
		html.push( headerT.applyTemplate({
			range: start.format('Y/m/d') + ' - ' + end.format('Y/m/d')
		}) );
		
		var eventT = new Ext.Template(
			'<div class="{eventCls}">',
				'<span class="{dateCls}">{date}</span>',
				'<span class="dayCls">{day}</span>',
				'<a target="_blank" href="{url}" title="{desc}">{title}</a>',
			'</div>'
		);
		
		var noEventT = new Ext.Template(
			'<div class="{eventCls}">',
				'<span class="dateCls">{date}</span>',
				'<span class="dayCls">{day}</span>',
				'<span class="hint">{title}</span>',
			'</div>'
		);
		
		for( var i=0; i<7; ++i ) {
			var dt = start.add( Date.DAY, i );
			var weekDay = dt.format('w');
			var isWeekend = false;
			if( weekDay==0 || weekDay==6 )
				isWeekend = true;
			
			var dateStr = dt.format('Y/m/d');
			var dayStr = dt.format('D');
			
			var dayEvent = events[dt.format('Ymd')];
			var hasEvent = dayEvent && dayEvent.length;
			if( hasEvent ) {
				for( var j=0,eventLen=dayEvent.length; j<eventLen; ++j ) {
					var info = dayEvent[j];
					html.push( eventT.applyTemplate({
						eventCls: isWeekend ? 'eventItem weekend' : 'eventItem',
						dateCls: j==0 ? 'dateCls' : 'dateHidden',
						dayCls: j==0 ? 'dayCls' : 'dayHidden',
						date: dateStr,
						day: _(dayStr),
						url: info.url,
						title: info.title,
						desc: info.start + '-' + info.end + '    ' + info.title
					}) );
				}
			}
			else {
				html.push( noEventT.applyTemplate({
					eventCls: isWeekend ? 'eventItem weekend' : 'eventItem',
					date: dateStr,
					day: _(dayStr),
					title: _('No event today.')
				}) );
			}
		}
		
		html.push( '</div></div>' );
		
		return html.join( '' );
  	}
});

Ext.reg( 'widget_calendar', Anz.widget.calendar );
