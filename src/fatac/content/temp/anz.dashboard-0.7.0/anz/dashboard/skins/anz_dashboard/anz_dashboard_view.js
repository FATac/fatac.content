/*
 * SameSpace 4.0
 * Copyright(c) 2006-2009, Anzsoft
 * eastxing@gmail.com
 * 
 */

// reference local blank image
Ext.BLANK_IMAGE_URL = 'ext3/resources/images/default/s.gif';

// create namespace
Ext.namespace( 'Anz', 'Anz.dashboard' );

Anz.dashboard.view = function() {
    return {
    	portalUrl: null,
    	contextUrl: null,
    	
    	// portal container
    	container: null,
    	
    	init: function( portalUrl, contextUrl ) {
    		Ext.QuickTips.init();
    		
    		this.portalUrl = portalUrl;
    		this.contextUrl = contextUrl;
    		
			Ext.Ajax.request({
        	    url: this.contextUrl + '/@@mergedRequest/getMergedData',
        	    method: 'POST',
	        	params: { 'requests:list': [
	        		'pageLayout@@dashboardView/getPageLayout',
	        		'layoutCfg@@dashboardView/getLayoutConfig',
	        		'widgets@@widgetView/getWidgets',
	        		'i18n@@msgCatalog/catalogMapping?domain=anz.dashboard'
	        	] },
        	    scope: this,
        	    success: function ( result, request ) {
					var ret = Ext.decode( result.responseText );
					
					var pageLayout = ret.pageLayout.layout;
					var layoutCfg = ret.layoutCfg.config;
					
					// update global i18n object
					Anz.i18n = ret.i18n.texts;
					
					// build widgets config
					var widgets = ret.widgets.widgets;
					var widgetsCfg = {};
					for( var i=0,len=widgets.length; i<len; ++i ) {
						var widget = widgets[i];
						widgetsCfg[widget.id] = widget;
					}
					
					this.constructPortal( pageLayout, layoutCfg, widgetsCfg );
				},
				failure: function ( result, request ) {
					alert( result.responseText );
				}
            });
    	},
    	
    	destroy: function() {
    		if( this.container ) {
	    		this.container.removeAll();
	    		//this.container.update( '' );
	    	}
    	},
    	
    	constructPortal: function( pageLayout, layoutCfg, widgetsCfg ) {
		    var containerCfg = {};
		    
		    var contentRegionId = 'content';
		    if( pageLayout === 'tile' ) {
	            Ext.apply( containerCfg, {
	            	renderTo: contentRegionId
		    	} );
		    }
		    else {
		    	// calc parent width
		    	var parent = Ext.get( contentRegionId );
		    	var width = parent.getWidth( true );
        		
		    	Ext.apply( containerCfg, {
		    		renderTo: contentRegionId,
		    		activeTab: 0,
			        width: width,
			        plain: true,
		        	defaults: {autoScroll: true}
		    	} );
		    }
		    
	    	var containerItems = [];
		    
		    // pages
		    for( var i=0,len=layoutCfg.length; i<len; ++i ) {
		    	var page = layoutCfg[i];
		    	var colNum = page.columns.length;
		    	
		    	var pageCfg = {};
		    	pageCfg.xtype = 'container';
		    	pageCfg.title = Utf8.decode(page.title);
		    	pageCfg.layout = 'column';
		    	pageCfg.border = false;
		    	pageCfg.autoHeight = true;
    			
		    	var pageItems = [];
		    	
		    	// columns
		    	for( var j=0; j<colNum; ++j ) {
		    		var column = page.columns[j];
		    		
		    		var colCfg = {};
		    		colCfg.xtype = 'container',
		    		colCfg.border = false;
		    		colCfg.columnWidth = parseFloat(column.width);
		    		colCfg.style = column.style;
		    		
		    		var items = [];
		    		var widgets = column.widgets;
		    		var portletNum = widgets.length;
		    		
		    		// widgets
		    		for( var k=0; k<portletNum; ++k ) {
		    			var widget = widgets[k];
		    			
		    			var widgetCfg = {};
		    			widgetCfg.portalUrl = this.portalUrl;
		    			widgetCfg.contextUrl = this.contextUrl;
		    			widgetCfg.xtype = widget.id;
		    			widgetCfg.options = widget.options;
		    			
		    			// show title or not
		    			if( !(widget.options.showTitle!==undefined && widget.options.showTitle===0) ) {
		    				widgetCfg.title = Utf8.decode( widget.options.title );
		    			}
		    			
		    			// do not show collapsed widget
		    			if( !widget.collapse ) {
			    			widgetCfg.collapsed = widget.collapse;
			    			widgetCfg.draggable = false;
			    			
			    			if( widget.color ) {
			    				widgetCfg.baseCls = 'x-panel-green';
			    			}
			    			
			    			if( widgetsCfg[widget.id] ) {
			    				widgetCfg.iconCls = widgetsCfg[widget.id].icon;
			    			}
			    			
			    			items.push( widgetCfg );
			    		}
		    		}
		    		
		    		colCfg.items = items;
		    		pageItems.push( colCfg );
		    	}
		    	
		    	pageCfg.items = pageItems;
		    	
		    	containerItems.push( pageCfg );
		    }
		    
		    containerCfg.items = containerItems;
		    
		    // construct container
	        if( pageLayout === 'tile' ) {
			    this.container = new Ext.Container( containerCfg );
	        }
	        else {
	        	this.container = new Ext.TabPanel( containerCfg );
	        }
    	}
    }
}();
