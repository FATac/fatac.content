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

Anz.dashboard.app = function() {
    return {
    	portalUrl: null,
    	contextUrl: null,
    	
    	// page container
    	container: null,
    	
    	// save current operated page
    	currentPage: null,
    	
    	pageLayout: null,
    	
    	// save current operated widget
    	currentWidget: null,
    	
    	pageTools: [],
    	columnTools: [],
    	widgetTools: [],
    	widgetContextMenu: null,
    	
    	// panel to show all registered widgets
    	widgetsPanel: null,
    	
    	init: function( portalUrl, contextUrl ) {
    		this.portalUrl = portalUrl;
    		this.contextUrl = contextUrl;
    		Ext.QuickTips.init();
    		
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
					
					this.pageLayout = ret.pageLayout.layout;
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
					
					this.constructPageTools();
					this.constructColumnTools();
					this.constructWidgetTools();
					
					this.constructPages( layoutCfg, widgetsCfg );
				},
				failure: function ( result, request ) {
					Ext.MessageBox.alert( 'failure', result.responseText );
				}
            });
    	},
    	
    	destroy: function() {
    		if( this.container ) {
	    		this.container.removeAll();
	    	}
    	},
    	
    	calcPageIndex: function( page ) {
    		var ret = null;
    		var pages = null;
    		if( this.pageLayout === 'tile' ) {
    			pages = this.container.items;
    			for( var i=0,len=pages.getCount(); i<len; ++i ) {
	    			if( page.getId() === pages.get(i).id ) {
	    				ret = i;
	    				break;
	    			}
	    		}
    		}
    		else {
    			var activeTab = this.container.getActiveTab();
    			var tabs = this.container.items;
    			for( var i=0; i<tabs.getCount(); i++ ) {
					if( activeTab == tabs.get(i) ) {
						ret = i;
						break;
					}
				}
    		}

    		return ret;
    	},
    	
    	calcColumnIndex: function( column ) {
    		var ret = null;
    		var cols = column.ownerCt.items;
    		for( var i=0,len=cols.getCount(); i<len; ++i ) {
    			if( column.getId() === cols.get(i).id ) {
    				ret = i;
    				break;
    			}
    		}
    		
    		return ret;
    	},
    	
    	calcWidgetPos: function( widget ) {
    		var page = widget.findParentByType( 'portal' );
    		var pageIndex = this.calcPageIndex( page );
    		var columnIndex = this.calcColumnIndex( widget.ownerCt );
    		
    		var widgetIndex = null;
    		var items = widget.ownerCt.items;
    		for( var i=0,len=items.getCount(); i<len; ++i ) {
    			if( widget.getId() === items.get(i).getId() ) {
    				widgetIndex = i;
    				break;
    			}
    		}
    		
    		return {
    			page: pageIndex,
    			col: columnIndex,
    			pos: widgetIndex,
    			pageCount: page.ownerCt.items.getCount(),
    			colCount: page.items.getCount()
    		};
    	},
    	
    	constructPageTools: function() {
    		this.pageTools = [{
	            id: 'add_widget',
			    qtip: _('Add widget'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
					this.showWidgetsView( panel );
				}
	        },{
	            id: 'add_page',
			    qtip: _('Add page'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
	            	this.addPage( this.calcPageIndex(panel)+1 );
	            }
	        },{
	        	id: 'save',
			    qtip: _('Edit page'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
	            	this.editPage( panel );
	            }
	        },{
	            id: 'up',
			    qtip: _('Move page up'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
	            	this.movePage( panel, 'up' );
	            }
	        },{
	            id: 'down',
			    qtip: _('Move page down'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
	            	this.movePage( panel, 'down' );
	            }
	        },{
	        	id: 'close',
			    qtip: _('Delete page'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
	            	this.delPage( panel );
	            }
	        }];
    	},
    	
    	constructColumnTools: function() {
    		this.columnTools = [{
			    id: 'add_column',
			    qtip: _('Add column'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
			        var page = panel.findParentByType( 'portal' );
			        var colIndex = this.calcColumnIndex( panel );
			        this.addColumn( page, colIndex+1 );
			    }
			},{
			    id: 'left',
			    qtip: _('Move column left'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
			    	this.moveColumn( panel, 'left' );
			    }
			},{
			    id: 'right',
			    qtip: _('Move column right'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
			    	this.moveColumn( panel, 'right' );
			    }
			},{
			    id: 'close',
			    qtip: _('Delete the column'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
			        this.delColumn( panel );
			    }
			}];
    	},
    	
    	constructWidgetTools: function() {
    		// create some widget tools using built in Ext tool ids
		    this.widgetTools = [{
			    id: 'toggle',
			    qtip: _('Collapse the widget'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
			        this.collapseWidget( panel );
			    }
			},{
			    id: 'gear',
			    qtip: _('Config the widget'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
			    	this.currentWidget = panel;
			    	
			    	if( !this.widgetContextMenu ) {
			    		this.widgetContextMenu = new Ext.menu.Menu({
							shadow: false,
							style: {
								background: 'white none repeat scroll 0 0',
								textAlign: 'left',
								border: '1px solid #999'
							},
							items: [{
								id: 'menuitem_color',
								text: _('color'),
								iconCls: 'color_widget',
								menu: {
									xtype: 'colormenu',
									colors: [ 'D96666', 'E67399', 'B373B3', '8C66D9', '668CB3', '668CD9', '59BFB3',
							                 '65AD89', '4CB052', '8CBF40', 'BFBF4D', 'E0C240', 'F2A640', 'E6804D',
							                 'BE9494', 'A992A9', '8997A5', '94A2BE', '85AAA5', 'A7A77D', 'C4A883' ],
							        scope: this,
							        handler: function( cm, color ) {
							        	this.changeWidgetColor( color );
							        }
								}
							}, {
								id: 'menuitem_up',
								text: _('up'),
								iconCls: 'move_up',
								scope: this,
								handler: function( menuItem, e ) {
									this.moveWidget( 'up' );
									e.stopEvent();
								}
							}, {
								id: 'menuitem_right',
								text: _('right'),
								iconCls: 'move_right',
								scope: this,
								handler: function( menuItem, e ) {
									this.moveWidget( 'right' );
									e.stopEvent();
								}
							}, {
								id: 'menuitem_down',
								text: _('down'),
								iconCls: 'move_down',
								scope: this,
								handler: function( menuItem, e ) {
									this.moveWidget( 'down' );
									e.stopEvent();
								}
							}, {
								id: 'menuitem_left',
								text: _('left'),
								iconCls: 'move_left',
								scope: this,
								handler: function( menuItem, e ) {
									this.moveWidget( 'left' );
									e.stopEvent();
								}
							}]
						});
					}
					
					this.widgetContextMenu.showAt( event.getPoint() );
			    }
			},{
			    id: 'refresh',
			    qtip: _('Refresh the widget'),
			    scope: this,
			    handler: function(event, toolEl, panel){
			        // whatever
			        var s = 1 + 2;
			    }
			},{
			    id: 'save',
			    qtip: _('Edit the widget'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
			        this.changeWidgetOptions( panel );
			    }
			},{
			    id: 'close',
			    qtip: _('Delete the widget'),
			    scope: this,
			    handler: function( event, toolEl, panel ) {
			        this.delWidget( panel );
			    }
			}];
    	},
    	
    	constructPages: function( layoutCfg, widgetsCfg ) {
    		var containerCfg = {};
		    
		    var contentRegionId = 'content';
		    if( this.pageLayout === 'tile' ) {
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
		    		minTabWidth: 115,
        			tabWidth: 135,
			        width: width,
			        autoHeight: true,
			        plain: true,
		        	//defaults: {autoScroll: false},
		        	enableTabScroll: true,
		    		plugins: [new Ext.ux.TabMoreMenu({
			        	menu: [{
							id: 'menuitem_edit_page',
							text: _('Edit page'),
							iconCls: 'edit_page',
							scope: this,
							handler: function( menuItem ) {
								var currentTab = this.container.getActiveTab();
								this.editPage( currentTab );
							}
						},{
							id: 'menuitem_left',
							text: _('left'),
							iconCls: 'move_left',
							scope: this,
							handler: function( menuItem ) {
								var currentTab = this.container.getActiveTab();
								var callBack = this.container.setActiveTab.createDelegate( this.container, [currentTab] );
								this.movePage( currentTab, 'left', callBack );
							}
						},{
							id: 'menuitem_right',
							text: _('right'),
							iconCls: 'move_right',
							scope: this,
							handler: function( menuItem ) {
								var currentTab = this.container.getActiveTab();
								var callBack = this.container.setActiveTab.createDelegate( this.container, [currentTab] );
								this.movePage( currentTab, 'right', callBack );
							}
						},{
				            id: 'menuitem_add_widget',
						    text: _('Add widget'),
							iconCls: 'x-tool-add_widget',
				    		scope: this,
						    handler: function( menuItem ) {
						    	var currentTab = this.container.getActiveTab();
								this.showWidgetsView( currentTab );
							}
				        },{
				            id: 'menuitem_add_page',
						    text: _('Add page'),
							iconCls: 'x-tool-add_page',
				    		scope: this,
						    handler: function( menuItem ) {
						    	var currentTab = this.container.getActiveTab();
				            	this.addPage( this.calcPageIndex(currentTab)+1 );
		            		}
				        },{
				            id: 'menuitem_delete_page',
						    text: _('Delete page'),
							iconCls: 'delete_page',
				    		scope: this,
						    handler: function( menuItem ) {
						    	var currentTab = this.container.getActiveTab();
				            	this.delPage( this.calcPageIndex(currentTab)+1 );
		            		}
				        }]
			        })]
		    	} );
		    }
		    
		    var containerItems = [];
		    
		    // pages
		    for( var i=0,len=layoutCfg.length; i<len; ++i ) {
		    	var page = layoutCfg[i];
		    	var colNum = page.columns.length;
		    	
		    	var pageItems = [];
		    	
		    	// columns
		    	for( var j=0; j<colNum; ++j ) {
		    		var column = page.columns[j];
		    		
		    		var colCfg = {};
		    		colCfg.title = _('column');
		    		colCfg.columnWidth = parseFloat(column.width);
		    		colCfg.style = column.style;
		    		colCfg.tools = this.columnTools;
		    		
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
		    			widgetCfg.title = Utf8.decode(widget.options.title);
		    			widgetCfg.collapsed = widget.collapse;
		    			
		    			if( widget.color ) {
		    				widgetCfg.baseCls = 'x-panel-green';
		    			}
		    			
		    			if( widgetsCfg[widget.id] ) {
		    				widgetCfg.iconCls = widgetsCfg[widget.id].icon;
		    			}
		    			
		    			widgetCfg.tools = this.widgetTools;
		    			items.push( widgetCfg );
		    		}
		    		
		    		colCfg.items = items;
		    		pageItems.push( colCfg );
		    	}
		    	
		    	var pageCfg = this._buildPortalCfg( pageItems, Utf8.decode(page.title) );
		    	
		    	containerItems.push( pageCfg );
		    }
		    
		    containerCfg.items = containerItems;
		    
		    // construct container
	        if( this.pageLayout === 'tile' ) {
			    this.container = new Ext.Panel( containerCfg );
	        }
	        else {
	        	this.container = new Ext.TabPanel( containerCfg );
	        }
    	},
    	
    	constructPage: function( pageItems, index ) {
	        var pageCfg = this._buildPortalCfg( pageItems, 'untitled page' );
	        
	        if( index ) {
	        	this.container.insert( index, pageCfg );
	        }
	        else {
	        	this.container.add( pageCfg );
	        }
    	},
    	
    	addPage: function( index ) {
    		Ext.Ajax.request({
        	    url: this.contextUrl + '/@@dashboardEdit/addPage',
        	    method: 'POST',
	        	params: {
	        		'pageIndex:int': index
				},
        	    scope: this,
        	    success: function ( result, request ) {
					var ret = Ext.decode( result.responseText );
					if( ret.success ) {
						// new page default has 2 columns
			    		var items = [{
			    			title: _('column'),
			    			columnWidth: 0.5,
							style: 'padding:5px 0 5px 5px',
							tools: this.columnTools,
							items:[]
						}, {
							title: _('column'),
							columnWidth: 0.5,
							style: 'padding:5px 0 5px 5px',
							tools: this.columnTools,
							items:[]
						}];
			    		
			    		this.constructPage( items, index );
			    		this.container.doLayout();
					}
					else {
						alert( ret.msg );
					}
				},
				failure: function ( result, request ) {
					Ext.MessageBox.alert( 'failure', result.responseText );
				}
            });
    	},
    	
    	editPage: function( page ) {
    		var formPanel = new Ext.FormPanel({
				labelWidth: 80,
				bodyStyle: 'padding:15px;',
				border: false,
				width: 500,
				autoHeight: true,
				defaults: { anchor: '100%' },
				defaultType: 'textfield',
				items: [{
		    		'name': 'title',
		    		'fieldLabel': 'title',
		    		'value': page.title
		    	},{
		    		'name': 'width',
		    		'fieldLabel': 'width',
		    		'value': ''
		    	},{
		    		'xtype': 'textarea',
		    		'name': 'style',
		    		'fieldLabel': 'style',
		    		'value': ''
		    	}]
			});
		
    		var win = new Ext.Window({
				layout: 'fit',
				title: _('Edit page'),
				width: 640,
				autoHeight: true,
				modal: true,
				items: formPanel,
				buttons: [{
					text: _('Save'),
					iconCls: 'icon-save',
					handler: function( button, e ) {
						var form = formPanel.getForm();
						button.disable();
						var cancelBtn = button.nextSibling();
						cancelBtn.disable();
						
						var values = form.getValues();
						if( form.isValid() ) {
							Ext.Ajax.request({
				        	    url: this.contextUrl + '/@@dashboardEdit/editPage',
				        	    method: 'POST',
					        	form: form.id,
					        	params: {
					        		'pageIndex:int': this.calcPageIndex( page )
								},
				        	    scope: this,
				        	    success: function ( result, request ) {
									var ret = Ext.decode( result.responseText );
									if( ret.success ) {
										page.setTitle( values.title );
									}
									else {
										alert( ret.msg );
									}
								},
								failure: function ( result, request ) {
									alert( result.responseText );
								}
				            });
						}
						else {
							button.enable();
							cancelBtn.enable();
						}
						
						win.close();
					},
					scope: this
				}, {
					text: _('Cancel'),
					scope: this,
					handler: function( button, e ) {
						win.close();
					}
				}]
			});
			
			win.show();
    	},
    	
    	movePage: function( page, dir, callback ) {
    		// calc old and new index
    		var container = this.container;
    		var maxIndex = this.container.items.length - 1;
    		var fromIndex = this.calcPageIndex( page );
    		var toIndex = null;
    		var doMove = false;
    		if( dir == 'up' ) {
    			if( fromIndex > 0 ) {
    				toIndex = fromIndex - 1;
    				doMove = true;
    			}
    		}
    		else if( dir == 'down' ) {
    			if( fromIndex < maxIndex ) {
    				toIndex = fromIndex + 1;
    				doMove = true;
    			}
    		}
    		else if( dir == 'left' ) {
    			if( fromIndex > 0 ) {
    				toIndex = fromIndex - 1;
    				doMove = true;
    			}
    		}
    		else if( dir == 'right' ) {
    			if( fromIndex < maxIndex ) {
    				toIndex = fromIndex + 1;
    				doMove = true;
    			}
    		}
    		
    		if( doMove ) {
	    		Ext.Ajax.request({
	        	    url: this.contextUrl + '/@@dashboardEdit/movePage',
	        	    method: 'POST',
		        	params: {
		        		'pageIndex:int': fromIndex,
		        		'toPage:int': toIndex
					},
	        	    scope: this,
	        	    success: function ( result, request ) {
						var ret = Ext.decode( result.responseText );
						if( ret.success ) {
							container.remove( page, false );
							var d = page.getPositionEl().dom;
							d.parentNode.removeChild( d );
							container.insert( toIndex, page );
							container.doLayout();
							
							// execute callback
							if( callback )
								callback();
						}
						else {
							alert( ret.msg );
						}
					},
					failure: function ( result, request ) {
						Ext.MessageBox.alert( 'failure', result.responseText );
					}
	            });
	        }
    	},
    	
    	delPage: function( page ) {
    		// prevent delete the last page
    		if( this.container.items.length == 1 ) {
    			alert( _('Can not delete the last page!') );
    			return;
    		}
    		
    		Ext.Msg.confirm( 'Confirm', _('Are you sure you want to delete this page?'), 
    			function( btn ) {
	                if( btn == 'yes' ) {
	                	var pageIndex = this.calcPageIndex( page );
	                	Ext.Ajax.request({
			        	    url: this.contextUrl + '/@@dashboardEdit/delPage',
			        	    method: 'POST',
				        	params: {
				        		'pageIndex:int': pageIndex
							},
			        	    scope: this,
			        	    success: function ( result, request ) {
								var ret = Ext.decode( result.responseText );
								if( ret.success ) {
									if( this.pageLayout === 'tile' ) {
										this.container.remove( page, true );
										//page.ownerCt.remove( page, true );
									}
									else {
										var tab = this.container.getActiveTab();
										this.container.remove( tab, true );
									}
								}
								else {
									alert( ret.msg );
								}
							},
							failure: function ( result, request ) {
								Ext.MessageBox.alert( 'failure', result.responseText );
							}
			            });
	                }
	            }, this
            );
    	},
    	
    	addColumn: function( page, colIndex ) {
    		var colIndex = colIndex ? colIndex : 0;
    		Ext.Ajax.request({
        	    url: this.contextUrl + '/@@dashboardEdit/addColumn',
        	    method: 'POST',
	        	params: {
	        		'pageIndex:int': this.calcPageIndex( page ),
	        		'columnIndex:int': colIndex
				},
        	    scope: this,
        	    success: function ( result, request ) {
					var ret = Ext.decode( result.responseText );
					if( ret.success ) {
						// default set column width to 1/cols
						// then recalc columns width and save to server
						var items = page.items;
						var colCount = items.getCount() + 1;
						var dftColWidth = 1 / colCount;
						var pw = null;
						
	                	var widths = [];
	                	for( var i=0,len=items.getCount(); i<len; ++i ) {
			                var c = items.get(i);
			                if( !pw ) {
			                	var target = c.container; 
								pw = target.getViewSize().width - target.getPadding('lr');
			                }
			                
			                var cel = c.getEl();
					    	var cw = c.getSize().width + cel.getMargins('lr');
					        var cwp = (cw/pw) * (1-dftColWidth);
					        c.columnWidth = cwp
					    	widths.push( cwp );
			            }
				        
						// add column to the left of page
			    		var col = {
			    			xtype: 'portalcolumn',
			    			title: _('column'),
			    			columnWidth: dftColWidth,
			    			style: 'padding:5px 0 5px 5px',
			    			tools: this.columnTools,
			    			items: []
			    		};
			    		widths.splice( colIndex, 0, dftColWidth );
			    		
			    		page.insert( colIndex, col );
			    		
			    		// adjust last column
			    		var lastCol = items.get( colCount-1 );
			    		this._adjustLastColumn( lastCol, widths );
			    		
			    		page.doLayout();
			    		this.changeColumnsWidth( page, widths );
					}
					else {
						alert( ret.msg );
					}
				},
				failure: function ( result, request ) {
					Ext.MessageBox.alert( 'failure', result.responseText );
				}
            });
    	},
    	
    	_adjustLastColumn: function( column, widths ) {
    		// remove 'margin-right' of the last column
			column.getEl().setStyle( 'margin-right', 0 );
			
			// adjust last column's width to takes all remaining width
			var widthCount = 0;
			for( var i=0,len=widths.length-1; i<len; ++i ) {
				widthCount += widths[i];
			}
			//var inaccuracy = 1 - widthCount;
			//column.columnWidth += inaccuracy;
			column.columnWidth = 1 - widthCount;
			
			//widths[widths.length-1] += inaccuracy;
			widths[widths.length-1] = 1 - widthCount;
    	},
    	
    	changeColumnsWidth: function( page, widths ) {
    		Ext.Ajax.request({
        	    url: this.contextUrl + '/@@dashboardEdit/changeColumnsWidth',
        	    method: 'POST',
	        	params: {
	        		'pageIndex:int': this.calcPageIndex(page),
	        		'widths:list': widths
				},
        	    scope: this,
        	    success: function ( result, request ) {
					var ret = Ext.decode( result.responseText );
					if( !ret.success ) {
						alert( ret.msg );
					}
				},
				failure: function ( result, request ) {
					Ext.MessageBox.alert( 'failure', result.responseText );
				}
            });
    	},
    	
    	moveColumn: function( column, dir ) {
    		// calc old and new index
    		var page = column.findParentByType( 'portal' );
    		var maxIndex = page.items.getCount() - 1;
    		var fromIndex = this.calcColumnIndex( column );
    		var toIndex = null;
    		var doMove = false;
    		if( dir == 'left' ) {
    			if( fromIndex > 0 ) {
    				toIndex = fromIndex - 1;
    				doMove = true;
    			}
    		}
    		else if( dir == 'right' ) {
    			if( fromIndex < maxIndex ) {
    				toIndex = fromIndex + 1;
    				doMove = true;
    			}
    		}
    		
    		if( doMove ) {
	    		Ext.Ajax.request({
	        	    url: this.contextUrl + '/@@dashboardEdit/moveColumn',
	        	    method: 'POST',
		        	params: {
		        		'pageIndex:int': this.calcPageIndex( page ),
		        		'columnIndex:int': fromIndex,
		        		'toColumn:int': toIndex
					},
	        	    scope: this,
	        	    success: function ( result, request ) {
						var ret = Ext.decode( result.responseText );
						if( ret.success ) {
							page.remove( column, false );
							var d = column.getPositionEl().dom;
							d.parentNode.removeChild( d );						
							page.insert( toIndex, column );
							
							// remove 'margin-right' of the last column
							var lastCol = page.items.get( maxIndex );
							lastCol.getEl().setStyle( 'margin-right', 0 );
							
							page.doLayout();
						}
						else {
							alert( ret.msg );
						}
					},
					failure: function ( result, request ) {
						Ext.MessageBox.alert( 'failure', result.responseText );
					}
	            });
	        }
    	},
    	
    	delColumn: function( column ) {
    		Ext.Msg.confirm( 'Confirm', _('Are you sure you want to delete this column?'), 
    			function( btn ) {
	                if( btn == 'yes' ) {
	                	var page = column.findParentByType( 'portal' );
	                	var colIndex = this.calcColumnIndex( column );
			    		Ext.Ajax.request({
			        	    url: this.contextUrl + '/@@dashboardEdit/delColumn',
			        	    method: 'POST',
				        	params: {
				        		'pageIndex:int': this.calcPageIndex( page ),
				        		'columnIndex:int': colIndex
							},
			        	    scope: this,
			        	    success: function ( result, request ) {
								var ret = Ext.decode( result.responseText );
								if( ret.success ) {
									var target = column.container; 
									var size = target.getViewSize();
									var pw = size.width - target.getPadding('lr');
									var colWidth = (column.getSize().width + column.getEl().getMargins('lr'))/pw;
									
				                	var widths = [];
				                	var items = page.items;
						            for( var i=0,len=items.getCount(); i<len; ++i ) {
						                var c = items.get(i);
						                if( i !== colIndex ) {
							                var cel = c.getEl();
						                	var cw = c.getSize().width + cel.getMargins('lr');
							                var cwp = (cw/pw) / (1-colWidth);
							                c.columnWidth = cwp
							            	widths.push( cwp );
							            }
						            }
							        
							        // remove column splitbar
							        var layout = page.getLayout();
							        if( layout.splitBars ) {
							        	layout.splitBars[colIndex].destroy( true );
							        }
							        
							        // remove column
							        column.ownerCt.remove( column, true );
							        
							        // adjust last column
						    		var lastCol = items.get( widths.length-1 );
						    		this._adjustLastColumn( lastCol, widths );
			    					
							        page.doLayout();
						    		
						    		// save to server
						    		this.changeColumnsWidth( page, widths );
								}
								else {
									alert( ret.msg );
								}
							},
							failure: function ( result, request ) {
								Ext.MessageBox.alert( 'failure', result.responseText );
							}
			            });
	                }
	            }, this
            );
    	},
    	
    	showWidgetsView: function( page ) {
    		if( !this.widgetsPanel ) {
	    		this.widgetsPanel = new Anz.dashboard.WidgetsView({
	    			portalUrl: this.portalUrl,
	    			url: this.contextUrl + '/@@widgetView/getWidgets',
	    			width: 515,
	    			height: 350
	    		});
    		}
    		
    		this.currentPage = page;
    		this.widgetsPanel.show( null, this.addWidget.createDelegate(this) );
    	},
    	
    	addWidget: function( widgetData ) {
    		Ext.Ajax.request({
        	    url: this.contextUrl + '/@@dashboardEdit/addWidget',
        	    method: 'POST',
	        	params: {
	        		'pageIndex:int': this.calcPageIndex( this.currentPage ),
	        		'columnIndex:int': 0,
	        		'widgetIndex:int': 0,
	        		'widgetId': widgetData.id
				},
        	    scope: this,
        	    success: function ( result, request ) {
					var ret = Ext.decode( result.responseText );
					if( ret.success ) {
						// add widget to the top of the first column
			    		var col = this.currentPage.getComponent( 0 );
			    		
			    		col.insert( 0, {
			    			xtype: widgetData.id,
			    			options: {},
			    			title: widgetData.title,
			    			iconCls: widgetData.iconCls,
			    			tools: this.widgetTools,
			    			contextUrl: this.contextUrl,
			    			portalUrl: this.portalUrl
			    		});
			    		
			    		col.doLayout();
					}
					else {
						alert( ret.msg );
					}
				},
				failure: function ( result, request ) {
					Ext.MessageBox.alert( 'failure', result.responseText );
				}
            });
    	},
    	
    	moveWidget: function( dir ) {
    		var widget = this.currentWidget;
    		var page = widget.findParentByType( 'portal' );
        	var lastPos = this.calcWidgetPos( widget );
        	var pageIndex = lastPos.page;
        	var oldColIndex = lastPos.col;
        	var oldWidgetIndex = lastPos.pos;
        	var newColIndex = null;
        	var newWidgetIndex = null;
        	if( dir == 'left' ) {
        		newColIndex = oldColIndex - 1;
        		newColIndex = newColIndex>0 ? newColIndex : 0;
        		
        		// prefer to keep the old widget index
        		var newCol = page.getComponent( newColIndex );
        		var widgetCount = newCol.items.getCount();
        		newWidgetIndex = oldWidgetIndex<widgetCount ? oldWidgetIndex : widgetCount;
        	}
        	else if( dir == 'right' ) {
        		newColIndex = oldColIndex + 1;
        		newColIndex = newColIndex<lastPos.colCount ? newColIndex : lastPos.colCount;
        		
        		// prefer to keep the old widget index
        		var newCol = page.getComponent( newColIndex );
        		var widgetCount = newCol.items.getCount();
        		newWidgetIndex = oldWidgetIndex<widgetCount ? oldWidgetIndex : widgetCount;
        	}
        	else if( dir == 'up' ) {
        		newColIndex = oldColIndex;
        		
        		newWidgetIndex = oldWidgetIndex - 1;
        		newWidgetIndex = newWidgetIndex>0 ? newWidgetIndex : 0;
        	}
        	else if( dir == 'down' ) {
        		newColIndex = oldColIndex;
        		
        		var newCol = page.getComponent( newColIndex );
        		var widgetCount = newCol.items.getCount();
        		newWidgetIndex = oldWidgetIndex + 1;
        		newWidgetIndex = newWidgetIndex<widgetCount ? newWidgetIndex : widgetCount;
        	}
        	
        	if( (oldColIndex!==newColIndex) || (oldWidgetIndex!==newWidgetIndex) ) {
	        	Ext.Ajax.request({
	        	    url: this.contextUrl + '/@@dashboardEdit/moveWidget',
	        	    method: 'POST',
		        	params: {
		        		'pageIndex:int': pageIndex,
		        		'columnIndex:int': oldColIndex,
		        		'widgetIndex:int': lastPos.pos,
		        		'toPage:int': pageIndex,
						'toColumn:int': newColIndex,
						'toWidget:int': newWidgetIndex
					},
	        	    scope: this,
	        	    success: function ( result, request ) {
						var ret = Ext.decode( result.responseText );
						if( ret.success ) {
							var oldCol = page.getComponent( oldColIndex );
							oldCol.remove( widget, false );
							var d = widget.getPositionEl().dom;
							d.parentNode.removeChild( d );
							
							var newCol = page.getComponent( newColIndex );
							newCol.insert( newWidgetIndex, widget );
							page.doLayout();
						} else {
							alert( 'move widget failure.' );
						}
					},
					failure: function ( result, request ) {
						Ext.MessageBox.alert( 'failure', result.responseText );
					}
	            });
	        }
    	},
    	
    	changeWidgetColor: function( color ) {
    		var widget = this.currentWidget;
    		var posInfo = this.calcWidgetPos( widget );
			
            Ext.Ajax.request({
        	    url: this.contextUrl + '/@@dashboardEdit/changeWidgetColor',
        	    method: 'POST',
	        	params: {
	        		'pageIndex:int': posInfo.page,
	        		'columnIndex:int': posInfo.col,
	        		'widgetIndex:int': posInfo.pos,
					'color': color
				},
        	    scope: this,
        	    success: function ( result, request ) {
					var ret = Ext.decode( result.responseText );
					if( ret.success ) {
						//panel.baseCls = 'x-panel-green';
						//panel.doLayout();
						
						// change base cls dynamicly
						var children = widget.getEl().query( '*[class*=x-panel]' );
						for( var i=0,len=children.length; i<len; ++i ) {
							var child = children[i];
							var cls = child.className;
							var parts = cls.split( widget.baseCls );
							child.className = parts.join( 'x-panel-green' );
						}
					} else {
						alert( 'change color failure' );
					}
				},
				failure: function ( result, request ) {
					Ext.MessageBox.alert( 'failure', result.responseText );
				}
            });
    	},
    	
    	changeWidgetOptions: function( panel ) {
    		var preferences = panel.getPreferences();
    		var options = panel.options;
    		var names = [];
    		var fields = [];
    		for( var i=0,len=preferences.length; i<len; ++i ) {
    			var preference = preferences[i];
    			var name = preference.name;
    			names.push( name );
    			var option = options[name];
    			
    			if( typeof option === 'string')
    				option = Utf8.decode( option );
    			
    			var field = {};
    			Ext.apply( field, preference );
    			field.value = (option!==undefined) ? option : preference.value;
    			
    			fields.push( field );
    		}
    		
    		// options form
    		var formPanel = new Ext.FormPanel({
				labelWidth: 80,
				bodyStyle: 'padding:15px;',
				border: false,
				width: 500,
				autoHeight: true,
				defaults: { anchor: '100%' },
				defaultType: 'textfield',
				items: fields
			});
		
    		var win = new Ext.Window({
				layout: 'fit',
				title: 'Edit ' + panel.title,
				width: 640,
				autoHeight: true,
				modal: true,
				items: formPanel,
				buttons: [{
					text: _('Save'),
					iconCls: 'icon-save',
					handler: function( button, e ) {
						var form = formPanel.getForm();
						button.disable();
						var cancelBtn = button.nextSibling();
						cancelBtn.disable();
						
						if( form.isValid() ) {
							var posInfo = this.calcWidgetPos( panel );
			            	
			            	Ext.Ajax.request({
				        	    url: this.contextUrl + '/@@dashboardEdit/changeWidgetOptions',
				        	    method: 'POST',
					        	form: form.id,
					        	params: {
					        		'pageIndex:int': posInfo.page,
					        		'columnIndex:int': posInfo.col,
					        		'widgetIndex:int': posInfo.pos,
					        		'names:list': names
								},
				        	    scope: this,
				        	    success: function ( result, request ) {
									var ret = Ext.decode( result.responseText );
									if( ret.success ) {
										panel.updateOptions( ret.options );
									}
									else {
										alert( ret.msg );
									}
								},
								failure: function ( result, request ) {
									Ext.MessageBox.alert( 'failure', result.responseText );
								}
				            });
						}
						else {
							button.enable();
							cancelBtn.enable();
						}
						
						win.close();
					},
					scope: this
				}, {
					text: _('Cancel'),
					scope: this,
					handler: function( button, e ) {
						win.close();
					}
				}]
			});
			
			win.show();
    	},
    	
    	collapseWidget: function( panel ) {
    		var newState = !panel.collapsed;
    		panel.toggleCollapse( true );
    		
    		// save collapse state to server
            var posInfo = this.calcWidgetPos( panel );		            
            Ext.Ajax.request({
        	    url: this.contextUrl + '/@@dashboardEdit/collapseWidget',
        	    method: 'POST',
	        	params: {
	        		'pageIndex:int': posInfo.page,
	        		'columnIndex:int': posInfo.col,
	        		'widgetIndex:int': posInfo.pos,
					'collapse:int': newState ? 1 : 0
				},
        	    scope: this,
        	    success: function ( result, request ) {
					var ret = Ext.decode( result.responseText );
					if( !ret.success ) {
						alert( ret.msg );
					}
				},
				failure: function ( result, request ) {
					Ext.MessageBox.alert( 'failure', result.responseText );
				}
            });
    	},
    	
    	delWidget: function( panel ) {
    		var win = new Ext.Window({
				layout: 'fit',
				title: panel.title,
				width: 300,
				autoHeight: true,
				modal: true,
				html: _('Are you sure to delete this widget?'),
				buttons: [{
					text: _('Delete'),
					width: 'auto',
					iconCls: 'icon-delete',
					handler: function( button, e ) {
						var posInfo = this.calcWidgetPos( panel );		            
			            Ext.Ajax.request({
			        	    url: this.contextUrl + '/@@dashboardEdit/delWidget',
			        	    method: 'POST',
				        	params: {
				        		'pageIndex:int': posInfo.page,
				        		'columnIndex:int': posInfo.col,
				        		'widgetIndex:int': posInfo.pos
							},
			        	    scope: this,
			        	    success: function ( result, request ) {
								var ret = Ext.decode( result.responseText );
								if( ret.success ) {
									panel.ownerCt.remove( panel, true );
								}
								else {
									alert( ret.msg );
								}
							},
							failure: function ( result, request ) {
								Ext.MessageBox.alert( 'failure', result.responseText );
							}
			            });

						win.close();
					},
					scope: this
				}, {
					text: _('Collapse'),
					scope: this,
					handler: function( button, e ) {
						this.collapseWidget( panel );
						win.close();
					}
				}, {
					text: _('Cancel'),
					scope: this,
					handler: function( button, e ) {
						win.close();
					}
				}]
			});
			
			win.show();
    	},
    	
    	//private
	    _buildPortalCfg: function( items, pageTitle ) {
	    	var portalCfg = {
				xtype: 'portal',
			    title: pageTitle,
				frame: false,
				autoHeight: true,
				style: 'padding: 10px 10px 0 10px;',
				bodyStyle: 'padding: 5px 5px 5px 0',
		        tools: this.pageTools,
		        toolscope: ['search','pin','gear'],
		        items: items,
	            listeners: {
	            	'validatedrop': {
	            		scope: this,
	            		fn: function( e ) {
		            		// save widget position info into panel
		            		var panel = e.panel;
		            		panel.lastPos = this.calcWidgetPos( panel );
		            	}
	            	},
	                'drop': {
	                	scope: this,
	                	fn: function( e ) {
		                	var panel = e.panel;
		                	var lastPos = panel.lastPos;
		                	var page = panel.findParentByType( 'portal' );
		                	Ext.Ajax.request({
				        	    url: this.contextUrl + '/@@dashboardEdit/moveWidget',
				        	    method: 'POST',
					        	params: {
					        		'pageIndex:int': lastPos.page,
					        		'columnIndex:int': lastPos.col,
					        		'widgetIndex:int': lastPos.pos,
					        		'toPage:int': this.calcPageIndex(page),
		    						'toColumn:int': e.columnIndex,
		    						'toWidget:int': e.position
		    					},
				        	    scope: this,
				        	    success: function ( result, request ) {
									var ret = Ext.decode( result.responseText );
									if( ret.success ) {
										delete panel.lastPos;
									} else {
										alert( 'move widget failure.' );
									}
								},
								failure: function ( result, request ) {
									Ext.MessageBox.alert( 'failure', result.responseText );
								}
				            });
				        }
	                },
	                'columnresize': {
	                	scope: this,
	                	fn: function( page ) {
		                	var pw = null;
		                	var widths = [];
		                	var items = page.items;
				            for( var i=0,len=items.getCount(); i<len; ++i ) {
				                var c = items.get(i);
				                if( !pw ) {
					                var target = c.container; 
									var size = target.getViewSize();
									pw = size.width - target.getPadding('lr');
					            }
				                var cw = c.el.getWidth();
				            	widths.push( cw/pw );
				            }
				            
				            // adjust last column
				    		var lastCol = items.get( widths.length-1 );
				    		this._adjustLastColumn( lastCol, widths );
						    
				            this.changeColumnsWidth( page, widths );
		                }
		            }
	            }
			};
			
		    return portalCfg;
		}
    }
}();
