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

Anz.widget.weather = Ext.extend( Anz.widget.base, {
    iconCls: 'widget_weather_icon',
    
    getCustomisePreferences: function() {
    	return [{
    		'xtype': 'widget.weather.woeidfield',
    		'name': 'woeid',
    		'fieldLabel': _('City'),
    		'value': ''
    	},{
    		'xtype': 'combo',
    		'name': 'units',
    		'hiddenName': 'units',
    		'fieldLabel': _('Units'),
    		'value': 'c',
    		'mode': 'local',
    		'store': {
    			xtype: 'arraystore',
    			fields: ['id', 'name'],
    			data: [['c',_('Celsius')],['f',_('Fahrenheit')]]
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
    		'value': '',
    		'mode': 'local',
    		'store': {
    			xtype: 'arraystore',
    			fields: ['id', 'name'],
    			data: [['Compact',_('Compact')],['Today',_('Today')]]
    		},
    		'displayField': 'name',
    		'valueField': 'id',
    		'triggerAction': 'all',
			'editable': false
    	}]
    },
    
    updateOptions: function( options ) {
    	var oldOptions = this.options;
    	this.options = options;
    	
    	this.setTitle( Utf8.decode(options.title) );
    	
    	if( !this.collapsed ) {
    		var oldWoeid = oldOptions.woeid;
    		var oldUnits = oldOptions.units;
    		var oldView = oldOptions.view;
    		
	    	if( oldWoeid !== options.woeid ) {
		    	this.display();
		    }
		    else if( oldUnits !== options.units ) {
		    	this.display();
		    }
		    else if( oldView !== options.view ) {
		    	this.display();
		    }
		}
    },
    
    display: function() {
    	// show load indicator
    	this.body.update( '<div class="loading-indicator">Loading...</div>' );
    	
    	var feed = this.getValue( 'feed' );
        Ext.Ajax.request({
    	    url: this.contextUrl + '/@@weatherWidget/weather',
    	    method: 'POST',
        	params: {
        		'woeid': this.options.woeid,
        		'units': this.options.units
			},
			timeout: 5000,
    	    scope: this,
    	    success: function ( result, request ) {
				var ret = Ext.decode( result.responseText );
				if( ret.success ) {
					var info = ret.info;
					var view = this.options.view;
					var html = this.buildContents( info, view );
					this.body.update( html );
					
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
  	
  	buildContents: function( entries, view ) {
  		var html = null;
		switch( view ) {
			case 'Compact':
				html = this.buildCompactHtml( entries );
				break;
			case 'Today':
				html = this.buildTodayHtml( entries );
				break;
			default:
				html = this.buildTodayHtml( entries );
		}
		return html;
  	},
  	
  	buildTodayHtml: function( info ) {
  		var t = new Ext.Template(
			'<div class="yw-forecast">',
			    '<div class="yw-loc">',
  					'<a target="_blank" href="{link}">{location}</a>',
  				'</div>',
			    '<div class="yw-date">{time}</div>',
			    '<div class="yw-cond">{condition_text}</div>',
			    '<dl>',
			        '<dt>{Feels_Like}:</dt><dd>{temp}&deg;{temp_unit}</dd>',
			        '<dt>{Barometer}:</dt><dd>{pressure} {pressure_unit}</dd>',
			        '<dt>{Humidity}:</dt><dd>{humidity} %</dd>',
			        '<dt>{Visibility}:</dt><dd>{visibility} {visibility_unit}</dd>',
			        '<dt>{Wind}:</dt><dd>{wind_direction} {wind_speed} {speed_unit}</dd>',
			        '<dt>{Sunrise}:</dt><dd>{sunrise}</dd>',
			        '<dt>{Sunset}:</dt><dd>{sunset}</dd>',
			    '</dl>',
			    '<div class="forecast-icon" style="background: transparent url(weather/{code}d-s.png) no-repeat scroll 0% 0%;"></div>',
			    '<div class="forecast-temp">',
			        '<div class="yw-temp">{temp}&deg;</div>',
			        '<p>{High}: {high_temp}&deg; {Low}: {low_temp}&deg;</p>',
			    '</div>',
			'</div>'
		);
		
		return t.applyTemplate({
			Feels_Like: _('Feels Like'),
			Barometer: _('Barometer'),
			Humidity: _('Humidity'),
			Visibility: _('Visibility'),
			Wind: _('Wind'),
			Sunrise: _('Sunrise'),
			Sunset: _('Sunset'),
			High: _('High'),
			Low: _('Low'),
			location: info.location.city + ',' + info.location.country,
			time: info.condition.date,
			//condition_text: info.condition.text,
			condition_text: this._conditionMap()[info.condition.code],
			temp: info.condition.temp,
			temp_unit: info.units.temperature,
			pressure: info.atmosphere.pressure,
			pressure_unit: info.units.pressure,
			humidity: info.atmosphere.humidity,
			visibility: info.atmosphere.visibility,
			visibility_unit: info.units.distance,
			wind_direction: info.wind.direction,
			wind_speed: info.wind.speed,
			speed_unit: info.units.speed,
			sunrise: info.astronomy.sunrise,
			sunset: info.astronomy.sunset,
			high_temp: info.forecast[0].high,
			low_temp: info.forecast[0].low,
			code: info.condition.code,
			link: info.link,
			Detailed_Forecast: _('Detailed Forecast')
		});
  	},
  	
  	buildCompactHtml: function( info ) {
  		var t = new Ext.Template(
  			'<div class="weather-compact">',
  				'<div class="yw-loc">',
  					'<a target="_blank" href="{link}">{location}</a>',
  				'</div>',
				'<div class="today-weather">',
					'<div class="weather-icon">',
						'<img src="weather/{today_code}d-s.png" title="{today_code_text}" alt="{condition_text}">',
					'</div>',
					'<div class="weather-text">',
						'<span class="weather-day">{today_date}<br>{today_weekday}</span>',
						'<span class="weather-temp">{today_low_temp}/{today_high_temp}&deg;</span>',
					'</div>',
				'</div>',
				'<div class="tomorrow-weather">',
					'<div class="weather-icon">',
						'<img src="weather/{next_code}d-s.png" title="{next_code_text}" alt="{next_code_text}">',
					'</div>',
					'<div class="weather-text">',
						'<span class="weather-day">{next_weekday}</span>',
						'<span class="weather-temp">{next_low_temp}/{next_high_temp}&deg;</span>',
					'</div>',
				'</div>',
			'</div>'
		);
		
		return t.applyTemplate({
			link: info.link,
			location: info.location.city + ',' + info.location.country,
			today_code: info.forecast[0].code,
			today_code_text: this._conditionMap()[info.forecast[0].code],
			today_low_temp: info.forecast[0].low,
			today_high_temp: info.forecast[0].high,
			today_date: info.forecast[0].date,
			today_weekday: _(info.forecast[0].day),
			next_code: info.forecast[1].code,
			next_code_text: this._conditionMap()[info.forecast[1].code],
			next_low_temp: info.forecast[1].low,
			next_high_temp: info.forecast[1].high,
			next_date: info.forecast[1].date,
			next_weekday: _(info.forecast[1].day)
		});
  	},
  	
  	_conditionMap: function() {
  		return {
  			 '0': _('Tornado'),
			 '1': _('Tropical storm'),
			 '2': _('Hurricane'),
			 '3': _('Severe thunderstorms'),
			 '4': _('Thunderstorms'),
			 '5': _('Mixed rain and snow'),
			 '6': _('Mixed rain and sleet'),
			 '7': _('Mixed snow and sleet'),
			 '8': _('Freezing drizzle'),
			 '9': _('Drizzle'),
			'10':	_('Freezing rain'),
			'11':	_('Showers'),
			'12':	_('Showers'),
			'13':	_('Snow flurries'),
			'14':	_('Light snow showers'),
			'15':	_('Blowing snow'),
			'16':	_('Snow'),
			'17':	_('Hail'),
			'18':	_('Sleet'),
			'19':	_('Dust'),
			'20':	_('Foggy'),
			'21':	_('Haze'),
			'22':	_('Smoky'),
			'23':	_('Blustery'),
			'24':	_('Windy'),
			'25':	_('Cold'),
			'26':	_('Cloudy'),
			'27':	_('Mostly cloudy'),
			'28':	_('Mostly cloudy'),
			'29':	_('Partly cloudy'),
			'30':	_('Partly cloudy'),
			'31':	_('Clear'),
			'32':	_('Sunny'),
			'33':	_('Fair'),
			'34':	_('Fair'),
			'35':	_('Mixed rain and hail'),
			'36':	_('Hot'),
			'37':	_('Isolated thunderstorms'),
			'38':	_('Scattered thunderstorms'),
			'39':	_('Scattered thunderstorms'),
			'40':	_('Scattered showers'),
			'41':	_('Heavy snow'),
			'42':	_('Scattered snow showers'),
			'43':	_('Heavy snow'),
			'44':	_('Partly cloudy'),
			'45':	_('Thundershowers'),
			'46':	_('Snow showers'),
			'47':	_('Isolated thundershowers')
  		}
  	}
});
               
Ext.reg( 'widget_weather', Anz.widget.weather );
                
Anz.widget.weather.woeidfield = function( config ) {
	var ds = new Ext.data.Store({
        proxy: new Ext.data.ScriptTagProxy({
            url: 'http://where.yahooapis.com/v1',
        	listeners: {
		    	beforeload: {
		    		scope: this,
		    		fn: function( proxy, params ) {
		    			proxy.setApi( Ext.data.Api.actions.read, String.format('http://where.yahooapis.com/v1/places.q({0});count=0?format=json&appid=1dIus9DV34GjOFTpNt_pwV465FOtJItUDeDMDR2bLWox6hTqUHPrVtvCnvDBfYg-',params.query) );
		    		}
		    	}
		    }   
        }),     
        reader: new Ext.data.JsonReader({
            root: 'places.place',
            id: 'woeid'
        }, [    
            {name: 'woeid', mapping: 'woeid'},
            {name: 'name', mapping: 'name'}
        ])      
    });         
	            
	// Custom rendering Template
	var resultTpl = new Ext.XTemplate(
        '<tpl for="."><div class="search-item">',
            '<h3><span>{woeid}-{name}</span></h3>',
        '</div></tpl>'
    );          
	            
	var dftConfig = {
        store: ds,
        displayField:'title',
        typeAhead: false,
        loadingText: 'Searching...',
        width: 570,
        hideTrigger:true,
        tpl: resultTpl,
        itemSelector: 'div.search-item',
        listeners: {
        	select: {
        		scope: this,
        		fn: function( combo, record, index ) {
        			//combo.setValue( record.get('name') );
        			combo.setValue( record.get('woeid') );
        		}
        	}   
        }       
    };          
	            
	if( config ) {
		Ext.apply( dftConfig, config );
	}           
	            
	Ext.apply( this, dftConfig );
	            
	Anz.widget.weather.woeidfield.superclass.constructor.apply( this, arguments );
};              
                
Ext.extend( Anz.widget.weather.woeidfield, Ext.form.ComboBox, {} );
                
Ext.reg( 'widget.weather.woeidfield', Anz.widget.weather.woeidfield );
