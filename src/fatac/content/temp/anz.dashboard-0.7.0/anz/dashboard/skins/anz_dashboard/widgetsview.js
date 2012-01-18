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

Anz.dashboard.WidgetsView = function( config ) {
	this.config = config;
}

Anz.dashboard.WidgetsView.prototype = {
    // cache data by widget id for easy lookup
    lookup: {},

	show: function( el, callback ){
		if( !this.win ) {
			this.initTemplates();

			this.store = new Ext.data.JsonStore({
		        url: this.config.url,
		        root: 'widgets',
		        fields: [ 'id', 'title', 'desc', 'icon' ]
		    });
			this.store.load();

			var formatData = function( data ) {
				data.iconCls = data.icon;
		    	data.icon = this.config.portalUrl + '/' + data.icon + '64.png';
		    	data.Widget_Name = _('Widget name');
		    	data.Description = _('Description');
		    	this.lookup[data.id] = data;
		    	return data;
		    };

		    this.view = new Ext.DataView({
				tpl: this.thumbTemplate,
				singleSelect: true,
				overClass: 'x-view-over',
				itemSelector: 'div.thumb-wrap',
				emptyText: '<div style="padding:10px;">No images match the specified filter</div>',
				store: this.store,
				listeners: {
					'selectionchange': {fn:this.showDetails, scope:this, buffer:100},
					'dblclick': {fn:this.doCallback, scope:this},
					'loadexception': {fn:this.onLoadException, scope:this},
					'beforeselect': {
						fn:function(view){
				        	return view.store.getRange().length > 0;
				    	}
				    }
				},
				prepareData: formatData.createDelegate(this)
			});

			var cfg = {
		    	title: _('Widgets list'),
		    	id: 'widgets-chooser-dlg',
		    	layout: 'border',
				minWidth: 500,
				minHeight: 300,
				modal: true,
				closeAction: 'hide',
				border: false,
				items:[{
					id: 'widget-chooser-view',
					region: 'center',
					autoScroll: true,
					items: this.view
				},{
					id: 'widget-detail-panel',
					region: 'east',
					split: true,
					width: 150,
					minWidth: 150,
					maxWidth: 250
				}],
				buttons: [{
					id: 'ok-btn',
					text: _('OK'),
					handler: this.doCallback,
					scope: this
				},{
					text: _('Cancel'),
					handler: function() {
						this.win.hide();
					},
					scope: this
				}],
				keys: {
					key: 27, // Esc key
					handler: function(){
						this.win.hide();
					},
					scope: this
				}
			};
			Ext.apply( cfg, this.config );
		    this.win = new Ext.Window( cfg );
		}

		this.reset();
	    this.win.show( el );
		this.callback = callback;
		this.animateTarget = el;
	},

	initTemplates: function(){
		this.thumbTemplate = new Ext.XTemplate(
			'<tpl for=".">',
				'<div class="thumb-wrap" id="{id}">',
				'<div class="thumb"><img src="{icon}" title="{title}"></div>',
				'<span>{title}</span></div>',
			'</tpl>'
		);
		this.thumbTemplate.compile();

		this.detailsTemplate = new Ext.XTemplate(
			'<div class="details">',
				'<tpl for=".">',
					'<div class="thumb"><img src="{icon}"></div>',
					'<div class="details-info">',
					'<div><b>{Widget_Name}: </b>',
					'<span>{title}</span></div>',
					'<div><b>{Description}: </b>',
					'<span>{desc}</span></div>',
					'</div>',
				'</tpl>',
			'</div>'
		);
		this.detailsTemplate.compile();
	},

	showDetails: function() {
	    var selNode = this.view.getSelectedNodes();
	    var detailEl = Ext.getCmp('widget-detail-panel').body;
		if( selNode && selNode.length > 0 ) {
			selNode = selNode[0];
			Ext.getCmp('ok-btn').enable();
		    var data = this.lookup[selNode.id];
            detailEl.hide();
            this.detailsTemplate.overwrite( detailEl, data );
            detailEl.slideIn( 'l', {stopFx:true,duration:.2} );
		} else {
		    Ext.getCmp('ok-btn').disable();
		    detailEl.update('');
		}
	},

	sortImages: function() {
		var v = Ext.getCmp('sortSelect').getValue();
    	this.view.store.sort(v, v == 'name' ? 'asc' : 'desc');
    	this.view.select(0);
    },

	reset: function() {
		this.view.select(0);
	},

	doCallback: function() {
        var selNode = this.view.getSelectedNodes()[0];
		var callback = this.callback;
		var lookup = this.lookup;
		this.win.hide( this.animateTarget, function() {
            if( selNode && callback ) {
				var data = lookup[selNode.id];
				callback( data );
			}
		});
    },

	onLoadException: function(v,o){
	    this.view.getEl().update('<div style="padding:10px;">Error loading images.</div>');
	}
};
