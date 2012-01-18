

Ext.ux.TabMoreMenu = function(config){
	config = config || {};
	Ext.apply(this, config);
	Ext.ux.TabMoreMenu.superclass.constructor.call(this);
};


/**
 * 
 * @class Ext.ux.TabMoreMenu
 * @extends Ext.util.Observable
 */
Ext.extend(Ext.ux.TabMoreMenu, Ext.util.Observable, {
	
	menuAlign : 'tr-br?',
	
	menuOffsets: [0, -5],
	
	init: function(tab){
		tab.getTemplateArgs = this.getTemplateArgs.createDelegate(tab);
		tab.findTargets = this.findTargets.createDelegate(tab);
		tab.onStripMouseDown = this.onStripMouseDown.createDelegate(tab);
		tab.on('beforedestroy', this.beforedestroy, this);
		tab.on('more', this.onMore, this);
		this.tab = tab;
		
        if(this.menu){
            this.menu = Ext.menu.MenuMgr.get(this.menu);
            Ext.apply(this.menu, {
            	defaultOffsets: this.menuOffsets,
            	afterRender: function(){
            		Ext.menu.Menu.superclass.afterRender.call(this);
            		this.items.each(function(item){
            			item.un("click", item.handler, item.scope);
            		}, this);
            	}
            });
            
            this.menu.on('click', this.onMenuClick, this);
        }		
	},		

	onMenuClick: function(menu, item, e){
		e.stopEvent();
		if(item.handler){
			item.handler.call(item.scope || this, this.menu.tabItem);
		}
	},
	
	onMore: function(e, t, el){
		e.stopEvent();
		this.menu.tabItem = t.item;
		
		if(this.menu){
			this.menu.show(el, this.menuAlign);
		}
	},
	
	getTemplateArgs : function(item){
		var p = Ext.TabPanel.prototype.getTemplateArgs.call(this, item);
		p['cls'] = 'x-tab-strip-more';
		return p;
	},
	
	findTargets : function(e){
		var t = Ext.TabPanel.prototype.findTargets.call(this, e);
		t['close'] = false;
		t['more'] = e.getTarget('.x-tab-strip-close', this.strip);
		return t;
	},
	
	onStripMouseDown : function(e){	
		Ext.TabPanel.prototype.onStripMouseDown.call(this, e);
		var t = this.findTargets(e);
		if(t.more && t.item){
			this.fireEvent('more', e, t, t.el);
		}			
	},
	
	beforedestroy: function(){
		Ext.destroy(this.menu);
	}
});