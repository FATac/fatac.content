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

Anz.widget.base = Ext.extend( Ext.Panel, {
    draggable: true,
    
    // Flag of loaded data or not
    loaded: false,
    
    // Maximum retry times
    // If a widget display failure, then we'll keep retry untll reach the 'maxRetryTimes'.
    maxRetryTimes: 6,
    
    // Save widget preferences
    options: null,
    
    // Save retried times
    retried: 0,
    
    // default style
    cls: 'x-widget',
    frame: false,
    style: 'margin: 5px 0 0',
    
    // private
  	initComponent: function() {
		Anz.widget.base.superclass.initComponent.call( this );
 		
 		var initCfg = this.initialConfig;
 		this.options = initCfg.options;
 		this.portalUrl = initCfg.portalUrl;
 		this.contextUrl = initCfg.contextUrl;
 		
        this.on({
        	render: {
				scope: this,
				fn: function( panel ) {
					// do not display collapsed widget
					if( !this.collapsed )
						this.display();
				}
			},
			expand: {
				scope: this,
				fn: function( panel ) {
					// do not load repeatly
					if( !this.loaded )
						this.display();
				}
			}
        });
	},
	
   /**
    * Retrieves the widget's common preferences.
    * @return {Array} The common preferences array 
    */
	getCommonPreferences: function() {
		return [{
    		'xtype': 'textfield',
    		'name': 'title',
    		'fieldLabel': _('Title'),
    		'value': 'Widget title'
    	},{
    		'xtype': 'xcheckbox',
    		'name': 'showTitle',
    		'fieldLabel': _('Show title?'),
    		'submitOffValue': 0,
    		'submitOnValue': 1,
    		'value': 1,
    		'hiddenName': 'showTitle:int'
    	}]
	},
	
   /**
    * Retrieves the widget's customised preferences.
    * Subclasses must override this method to return comstomised preferences array.
    * @return {Array} The customised preferences array 
    */
	getCustomisePreferences: function() {
    	return [];
    },
	
   /**
    * Retrieves the widget's preferences, used to construct perference edit form.
    * Preferences are composed of common preferences and customised preferences. 
    * @return {Array} The preferences array
    */
	getPreferences: function() {
    	return this.getCommonPreferences().concat( this.getCustomisePreferences() );
    },
	
	/**
    * Update the widget's body contents, called after options changed.
    * Subclasses must override this method to update body contents after options change.
    * @param {Object} options The widget options
    */
	updateOptions: function( options ) {
    },
    
   /**
    * Construct widget body contents and display it.
    * Subclasses must override this method to construct their body contents.
    */
	display: function() {
	},
  	
  /**
    * Display retry mechanism. If a widget display failure, then we'll keep retry
    * untll reach the 'maxRetryTimes'.
    */
  	retryDisplay: function() {
    	if( !this.loaded ) {
    		if( this.retried < this.maxRetryTimes ) {
    			this.retried += 1;
    			this.display.defer( Math.pow(2,this.retried)*1000, this );
    		}
    		else {
    			this.body.update( _('Sorry, we can not get data successfully now, you should refresh the whole page later to try again.') );
    		}
    	}
    },
  
   /**
    * Retrieves the value of the specific preference.
    * @param {String} name The preference name
    *
    * @return {String} The value of specific preference
    */
    getValue: function( name ) {
    	var ret = this.options[name];
    	if( ret === undefined ) {
    		ret = this.getDefaultValues()[name];
    	}
    	
    	return ret;
    },
    
   /**
    * Retrieves the widget's default preferences.
    * Subclasses must override this method to return comstomised default preferences object.
    * @return {Object} The customised default preferences object 
    */
    getDefaultValues: function() {
    	return {};
    }
});
