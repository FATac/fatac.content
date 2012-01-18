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

Anz.widget.rss = Ext.extend( Anz.widget.base, {
    bodyStyle: 'padding: 5px',
    iconCls: 'widget_rss_icon',
    
    // feed entries
    entries: [],
    
    // current page number
    page: 0,
    
    // total page count
    pageCount: 1,
    
    // entries count per page
    count: null,
    
    getCustomisePreferences: function() {
    	return [{
    		'xtype': 'textfield',
    		'name': 'feed',
    		'fieldLabel': _('Feed'),
    		'value': ''
    	},{
    		'xtype': 'xcheckbox',
    		'name': 'paging',
    		'fieldLabel': _('Paging?'),
    		'submitOffValue': 0,
    		'submitOnValue': 1,
    		'value': 1,
    		'hiddenName': 'paging:int'
    	},{
    		'xtype': 'numberfield',
    		'name': 'count',
    		'fieldLabel': _('Count'),
    		'value': 5,
    		'allowBlank': false,
    		'allowDecimals': false,
    		'allowNegative': false
    	},{
    		'xtype': 'combo',
    		'name': 'view',
    		'hiddenName': 'view',
    		'fieldLabel': _('View'),
    		'value': 'Normal',
    		'mode': 'local',
    		'store': {
    			xtype: 'arraystore',
    			fields: ['id', 'name'],
    			data: [['Normal',_('Normal')],['Magazine',_('Magazine')],
    					['Slideshow',_('Slideshow')],['Headline',_('Headline')]]
    		},
    		'displayField': 'name',
    		'valueField': 'id',
    		'triggerAction': 'all',
			'editable': false
    	}]
    },
    
    getDefaultValues: function() {
    	return {
    		count: 5,
    		paging: 1,
    		view: 'Normal'
    	};
    },
    
    updateOptions: function( options ) {
    	var oldOptions = this.options;
    	this.options = options;
    	this.count = parseInt( this.getValue('count') );
    	
    	this.setTitle( Utf8.decode(this.getValue('title')) );
    	
    	if( !this.collapsed ) {
    		var oldFeed = oldOptions.feed;
    		var oldView = oldOptions.view;
    		var oldPaging = oldOptions.paging;
    		
	    	if( oldFeed !== this.getValue('feed') ) {
		    	this.display();
		    }
		    else if( oldView!==this.getValue('view') || oldPaging!==this.getValue('paging') ) {
		    	if( this.loaded ) {
		    		this.buildContents();
		    	}
		    	else {
			    	this.display();
			    }
		    }
		}
    },
    
    display: function() {
    	this.body.update( '<div class="loading-indicator">Loading...</div>' );
    	
    	// reset loaded flag
    	this.loaded = false;
    	
    	var feed = this.getValue( 'feed' );
    	var count = this.getValue( 'count' );
        Ext.Ajax.request({
    	    url: this.initialConfig.contextUrl + '/@@rssWidget/entries',
    	    method: 'POST',
        	params: {
        		'url': feed,
        		'count:int': count
			},
			timeout: 5000,
    	    scope: this,
    	    success: function ( result, request ) {
				var ret = Ext.decode( result.responseText );
				if( ret.success ) {
					this.entries = ret.entries;
					this.count = parseInt( this.getValue('count') );
					this.pageCount = Math.ceil( ret.entries.length/this.count );
					this.buildContents();
					this.loaded = true;
				}
				else {
					if( ret.msg ) {
						this.body.update( ret.msg );
					}
					else {
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
					this.body.update( _('Sorry, get data fail, rettry later.') );
				}
				
				this.retryDisplay();
			}
        });
    },
  	
  	attachPagingHandler: function() {
		var prePageE = this.body.child( 'a[class=prePage]' );
		if( prePageE )
			prePageE.on( 'click', this.prePage, this );

  		var nextPageE = this.body.child( 'a[class=nextPage]' );
  		if( nextPageE )
  			nextPageE.on( 'click', this.nextPage, this );
  	},
  	
  	prePage: function() {
  		this.page -= 1;
  		this.buildContents();
  	},
  	
  	nextPage: function() {
  		this.page += 1;
  		this.buildContents();
  	},
  	
  	buildContents: function() {
  		var html = '';
  		
  		// feed list
  		var view = this.getValue('view');
		switch( view ) {
			case 'Normal':
				html = this.buildNormalHtml();
				break;
			case 'Magazine':
				html = this.buildMagazineHtml();
				break;
			case 'Slideshow':
				html = this.buildSlideshowHtml();
				break;
			case 'Headline':
				html = this.buildHeadlineHtml();
				break;
			default:
				html = this.buildNormalHtml();
		}
		
		// paging
		var showPaging = this.getValue('paging') && (this.pageCount>1) && (view!=='Slideshow');
		if( showPaging ) {
			html += '<div class="paging-bottom">';
	  		if( this.page !== 0 ) {
	  			html +=	String.format('<a class="prePage" href="javascript:;">{0}</a>',_('prev'));
	  		}
	  		if( this.page < this.pageCount-1 ) {
		  		html +=	String.format('<a class="nextPage" href="javascript:;">{0}</a>',_('next'));
		  	}
		  	html +=	'<div>';
	  	}
	  	
  		this.body.update( html );
  		
  		// handle slideshow specially
		if( view === 'Slideshow' ) {
			var slideshowEId = this.getId() + '_slideshow';
		    new Ext.ux.Carousel( slideshowEId, {
	            itemSelector: 'div.item',
	            interval: 10,
	            autoPlay: true,
	            transitionEasing: 'easeIn'                 
	        });
		}
  		
  		if( showPaging ) {
  			this.attachPagingHandler();
  		}
  	},
  	
  	buildNormalHtml: function() {
  		var start = this.page * this.count;
  		var entries = this.entries.slice( start, start+this.count );
  		
  		var html = '<ul class="feedList">';
		var itemT = new Ext.Template(
			'<li>',
				'<a href="{link}" title="{desc}" target="_blank">',
					'{title}<span class="feedItemDate"> - {date}</span>',
				'</a>',
			'</li>'
		);
		
		for( var i=0,len=entries.length; i<len; ++i ) {
			var entry = entries[i];
			var newStr = this.convertDate( entry.updated );
			html += itemT.applyTemplate({
				title: entry.title,
				desc: entry.summary,
				link: entry.link,
				date: this.getTimeDiff( newStr )
			});
		}
		
		html += '</ul>'
		
		return html;
  	},
  	
  	buildMagazineHtml: function() {
  		var start = this.page * this.count;
  		var entries = this.entries.slice( start, start+this.count );
  		
  		var html = ['<div class="magazineView">'];
		var firstItemT = new Ext.Template(
			'<div class="left">',
				'<div class="crop">',
					'<img height="234" width="234" src="{img}">',
				'</div>',
				'<div class="article">',
					'<h3><a href="{link}" target="_blank">{title}</a></h3>',
					'<small class="feedItemDate">{date}</small>',
					'<p>{desc}</p>',
				'</div>',
			'</div>'
		);
		
		var first = entries[0];
		var newStr = this.convertDate( first.updated );
		html.push( firstItemT.applyTemplate({
			title: first.title,
			desc: first.summary,
			img: this.portalUrl + '/default_news.png',
			link: first.link,
			date: this.getTimeDiff( newStr )
		}) );
		
		html.push( '<div class="right">' );
		
		var	otherItemT = new Ext.Template(
			'<div class="item">',
				'<div class="thumbnail">',
					'<img height="50" width="50" src="{img}"/>',
				'</div>',
				'<div class="title">',
					'<h3><a href="{link}" target="_blank">{title}</a></h3>',
					'<small class="feedItemDate">{date}</small>',
				'</div>',
				'<div class="description">',
					'<p>{desc}</p>',
				'</div>',
			'</div>'
		);
		
		for( var i=1,len=entries.length; i<len; ++i ) {
			var entry = entries[i];
			
			var newStr = this.convertDate( entry.updated );
			html.push( otherItemT.applyTemplate({
				title: entry.title,
				desc: entry.summary,
				img: this.portalUrl + '/default_news.png',
				link: entry.link,
				date: this.getTimeDiff( newStr )
			}) );
		}
		
		html.push( '</div></div>' );
		
		return html.join('');
  	},
  	
  	buildSlideshowHtml: function() {
  		var entries = this.entries;
  		
  		var slideshowEId = this.getId() + '_slideshow';
  		var html = [String.format('<div class="slideshowView" id="{0}">',slideshowEId)];
		var itemT = new Ext.Template(
			'<div class="item">',
				'<div class="crop">',
					'<img height="234" width="234" src="{img}">',
				'</div>',
				'<div class="content">',
					'<div class="title">',
						'<h3><a href="{link}" target="_blank">{title}</a></h3>',
					'</div>',
					'<div class="description">',
						'<small class="feedItemDate">{date}</small>',
						'<p>{desc}</p>',
					'</div>',
				'</div>',
			'</div>'
		);
		
		for( var i=0,len=entries.length; i<len; ++i ) {
			var entry = entries[i];
			
			var newStr = this.convertDate( entry.updated );
			html.push( itemT.applyTemplate({
				img: this.portalUrl + '/default_news.png',
				title: entry.title,
				desc: entry.summary,
				link: entry.link,
				date: this.getTimeDiff( newStr )
			}) );
		}
		
		html.push( '</div>' );
		
		return html.join('');
  	},
  	
  	buildHeadlineHtml: function() {
  		var start = this.page * this.count;
  		var entries = this.entries.slice( start, start+this.count );
  		
  		var html = ['<div class="headlineView">'];
		var firstItemT = new Ext.Template(
			'<div class="top">',
				'<div class="crop">',
					'<img height="234" width="234" src="{img}">',
				'</div>',
				'<div class="title">',
					'<h3><a href="{link}" target="_blank">{title}</a></h3>',
					'<small class="feedItemDate">{date}</small>',
				'</div>',
			'</div>',
			'<div class="middle odd">',
				'<div class="description">{desc}</div>',
			'</div>'
		);
		
		var first = entries[0];
		var newStr = this.convertDate( first.updated );
		html.push( firstItemT.applyTemplate({
			img: this.portalUrl + '/default_news.png',
			title: first.title,
			desc: first.summary,
			link: first.link,
			date: this.getTimeDiff( newStr )
		}) );
		
		html.push( '<ul class="bottom">' );
		
		var	otherItemT = new Ext.Template(
			'<li class="item {cls}">',
				'<div class="thumbnail">',
					'<img height="50" width="50" src="{img}">',
				'</div>',
				'<h3><a href="{link}" target="_blank">{title}<small class="feedItemDate">{date}</small></a></h3>',
				'<p class="description">{desc}</p>',
			'</li>'
		);
		
		for( var i=1,len=entries.length; i<len; ++i ) {
			var entry = entries[i];
			
			var newStr = this.convertDate( entry.updated );
			html.push( otherItemT.applyTemplate({
				cls: i%2 ? 'even' : 'odd',
				img: this.portalUrl + '/default_news.png',
				title: entry.title,
				desc: entry.summary,
				link: entry.link,
				date: this.getTimeDiff( newStr )
			}) );
		}
		
		html.push( '</ul></div>' );
		
		return html.join('');
  	},
    
    convertDate: function( origStr ) {
  		// convert date format from '2010-1-5 12:32' to '2010/1/5 12:32'
		var ret = null;
		if( origStr ) {
			ret = origStr.split('-').join('/');
		}
		
		return ret
  	},
  	
    getTimeDiff: function( str ) {
		if( !str )
			return '';
		
		var pubDate = new Date( str );
		var nowDate = new Date();
		var diffMilSeconds = nowDate.valueOf()-pubDate.valueOf();
		var days = diffMilSeconds/86400000;
		days = parseInt(days);
	
		diffMilSeconds = diffMilSeconds-(days*86400000);
		var hours = diffMilSeconds/3600000;
		hours = parseInt(hours);
	
		diffMilSeconds = diffMilSeconds-(hours*3600000);
		var minutes = diffMilSeconds/60000;
		minutes = parseInt(minutes);
	
		diffMilSeconds = diffMilSeconds-(minutes*60000);
		var seconds = diffMilSeconds/1000;
		seconds = parseInt(seconds);
		
		var returnStr = '';
	
		if( days > 0 ) {
			returnStr = days + _('days before');
		}
		else if( hours > 0 ) {
			returnStr = hours + _('hours before');
		}
		else if( minutes > 0 ) {
			returnStr = minutes + _('minutes before');
		}
	
		return returnStr;
	}
});

Ext.reg( 'widget_rss', Anz.widget.rss );
