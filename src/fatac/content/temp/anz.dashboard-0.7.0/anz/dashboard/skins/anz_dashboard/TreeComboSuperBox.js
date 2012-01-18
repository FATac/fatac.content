/**
 * <p>TreeComboSuperBox is a ComboBox like component which displays select list as a tree and selected items as labelled boxes within the form field.</p>
 *
 * This extension are written by eastxing<eastxing@gmail.com>, some ideas and codes are come from the following threads:
 * http://www.extjs.com/forum/showthread.php?t=38654
 * http://www.extjs.com/forum/showthread.php?t=69307
 *
 * Kudos to Animal and Dan Humphrey<dan.humphrey@technomedia.co.uk>.
 * Thanks to the other contributors too, they are: Wedgie
 *
 * Test under extjs3.1, firefox3, ie6, ie8.
 */

Ext.namespace( 'Ext.ux', 'Ext.ux.form' );

Ext.ux.form.TreeComboSuperBox = Ext.extend( Ext.form.TriggerField, {

	/**
     * @cfg {String} displayField The underlying {@link Ext.data.Field#name data field name} to bind to this
     * TreeComboSuperBox (defaults to undefined).
     * See also {@link #valueField}.
     */
    displayField: null,
    
	/**
     * @cfg {String/XTemplate} displayFieldTpl A template for rendering the displayField in each selected item. Defaults to null.
     */
    displayFieldTpl: null,
    
    /**
     * @cfg {Boolean} forceFormValue When set to true, the component will always return a value to the parent form getValues method, and when the parent form is submitted manually. Defaults to false, meaning the component will only be included in the parent form submission (or getValues) if at least 1 item has been selected.  
     */
    forceFormValue: false,
    
	/**
     * @cfg {String} hiddenName If specified, a hidden form field with this name is dynamically generated to store the
     * field's data value (defaults to the underlying DOM element's name). Required for the field's value to automatically
     * post during a form submission.
     */
    hiddenName: null,
    
    /**
     * @cfg {Boolean} multiSelect
     * True to allow set more than one node, false to allow only a single node (defaults to true).
     */
	multiSelect: true,

    /**
     * @cfg {Boolean} navigateItemsWithTab When set to true the tab key will navigate between selected items. Defaults to true.
     */
    navigateItemsWithTab: true,
    
    /**
     * @cfg {Boolean} resizable true to add a resize handle to the bottom of the dropdown list
     * (creates an {@link Ext.Resizable} with 'se' {@link Ext.Resizable#pinned pinned} handles).
     * Defaults to false.
     */
    resizable: false,
    
    /**
     * @cfg {Object} treeConfig Config object for the underlying {@link Ext.tree.TreePanel}.
     * Defaults to
     * <pre>
     * {
     * &nbsp;  rootVisible: false,
     * &nbsp;  border: false,
     * &nbsp;  autoScroll: true,
     * &nbsp;  loaded: false,
     * &nbsp;  root:{
     * &nbsp;      nodeType: 'async',
     * &nbsp;      expanded: true,
     * &nbsp;      uiProvider: false,
     * &nbsp;  },
     * &nbsp;  loader:{
     * &nbsp;      url: 'request.php'
     * &nbsp;  }
     * }
     * </pre>
     */
    treeConfig: {
        rootVisible: false,
        border: false,
        autoScroll: true,
        loaded: false,
        root:{
            nodeType: 'async',
            expanded: true,
            uiProvider: false
        },
        loader: {
            url: 'request.php'
        }
    },
    
	/**
     * @cfg {String} valueDelimiter The delimiter to use when joining and splitting value arrays and strings.
     */
    valueDelimiter: ',',
    
	/**
     * @cfg {String} valueField The underlying {@link Ext.data.Field#name data value name} to bind to this
     * TreeComboSuperBox (defaults to undefined).
     * 

	Note: use of a valueField requires the user to make a selection in order for a value to be
     * mapped.  See also {@link #hiddenName}, {@link #hiddenValue}, and {@link #displayField}.
     */
    valueField: null,
    
    // private
    initComponent: function() {
        Ext.apply( this, {
        	editable: false,
        	triggerConfig: {
				cls: 'x-superboxselect-btns',
				children: [
			        { tag:'div', cls: 'x-superboxselect-btn-expand' }
			    ]
			},
            items: new Ext.util.MixedCollection(false)
        });
		
        Ext.ux.form.TreeComboSuperBox.superclass.initComponent.call( this );
        
        this.constructTree();
    },

	// private
	onRender: function( ct, position ) {
    	var h = this.hiddenName;
    	this.hiddenName = null;
        Ext.ux.form.TreeComboSuperBox.superclass.onRender.call(this, ct, position);
        
        this.hiddenName = h;
        this.el.removeClass('x-form-text').addClass('x-superboxselect-input-field');
        
        this.wrapEl = this.el.wrap({
            tag : 'ul'
        });
        
        this.outerWrapEl = this.wrapEl.wrap({
            tag : 'div',
            cls: 'x-form-text x-superboxselect'
        });
       
        this.inputEl = this.el.wrap({
            tag : 'li',
            cls : 'x-superboxselect-input'
        });
        
        this.setupFormInterception();
    },
    
    constructTree: function() {
        if( !this.treePanel ) {
            if( !this.treeWidth ) {
                this.treeWidth = Math.max( 200, this.width || 200 );
            }
            
            if( !this.treeHeight ) {
                this.treeHeight = 200;
            }
            
            Ext.apply( this.treeConfig, {
            	renderTo: Ext.getBody(),
            	floating: true,
                autoScroll: true,
                minWidth: 200,
                minHeight: 200,
                width: this.treeWidth,
                height: this.treeHeight
            });
            
            if( !this.treeConfig.listeners )
            	this.treeConfig.listeners = {};
            
            Ext.apply( this.treeConfig.listeners, {
            	hide: this.onTreeHide,
                show: this.onTreeShow,
                expandnode: this.onExpandOrCollapseNode,
                collapsenode: this.onExpandOrCollapseNode,
                resize: this.onTreeResize,
                scope: this
            });
            
            this.treePanel = new Ext.tree.TreePanel( this.treeConfig );
            
            this.treePanel.show();
            this.treePanel.hide();
            this.relayEvents( this.treePanel.loader, ['beforeload', 'load', 'loadexception'] );
            
            // add tree panel resizer
            if( this.resizable ) {
                this.resizer = new Ext.Resizable( this.treePanel.getEl(), {
                   pinned:true, handles:'se'
                });
                this.mon( this.resizer, 'resize', function(r, w, h) {
                    this.treePanel.setSize(w, h);
                }, this );
            }
        }
    },
	
	onTriggerClick: function() {
        this.treePanel.show();
        this.treePanel.getEl().alignTo( this.wrap, 'tl-bl?' );
    },

    onExpandOrCollapseNode: function() {
        if( !this.maxHeight || this.resizable )
            return;
        
        var treeEl = this.treePanel.getTreeEl();
        var heightPadding = treeEl.getHeight() - treeEl.dom.clientHeight;
        var ulEl = treeEl.child( 'ul' );
        var heightRequired = ulEl.getHeight() + heightPadding;
        if( heightRequired > this.maxHeight )
            heightRequired = this.maxHeight;
        
        this.treePanel.setHeight( heightRequired );
    },

    onTreeResize: function() {
        if( this.treePanel )
            this.treePanel.getEl().alignTo( this.wrap, 'tl-bl?' );
    },

    onTreeShow: function() {
        Ext.getDoc().on('mousewheel', this.collapseIf, this);
        Ext.getDoc().on('mousedown', this.collapseIf, this);
    },

    onTreeHide: function() {
        Ext.getDoc().un('mousewheel', this.collapseIf, this);
        Ext.getDoc().un('mousedown', this.collapseIf, this);
    },

    collapseIf : function(e){
        if( !e.within(this.wrap) && !e.within(this.treePanel.getEl()) ) {
            this.collapse();
        }
    },

    collapse: function() {
        this.treePanel.hide();
    },
    
    /**
     * Returns a String value containing a concatenated list of item values. The list is concatenated with the {@link #Ext.ux.form.TreeComboSuperBox-valueDelimiter}.
     * @methodOf Ext.ux.form.TreeComboSuperBox
     * @name getValue
     * @return {String} a String value containing a concatenated list of item values. 
     */
    getValue : function() {
        var ret = [];
        this.items.each( function(item) {
            ret.push( item.value );
        });
        return ret.join( this.valueDelimiter );
    },
    
    /**
     * Sets the value of the TreeComboSuperBox component.
     * @methodOf Ext.ux.form.TreeComboSuperBox
     * @name setValue
     * @param {String|Array} value An array of item values, or a String value containing a delimited list of item values. (The list should be delimited with the {@link #Ext.ux.form.TreeComboSuperBox-valueDelimiter) 
     */
    setValue: function( value ) {
        if( !this.rendered ) {
            this.value = value;
            return;
        }
            
        this.removeAllItems();
        
        if( Ext.isEmpty(value) ) {
        	return;
        }
        
        var values = value;
        if( !Ext.isArray(value) ) {
            value = '' + value;
            values = value.split( this.valueDelimiter ); 
        }
        
        if( this.multiSelect ) {
	        Ext.each( values, function( val ) {
            	var itemVal = val;
		        var itemDisplay = val;
		        var itemCaption = val;
		        var itemClass = '';
		        var itemStyle = '';
		        this.addItemBox( itemVal, itemDisplay, itemCaption, itemClass, itemStyle );
        	}, this );
    	}
    	else {
    		var val = values[0];
    		var itemVal = val;
	        var itemDisplay = val;
	        var itemCaption = val;
	        var itemClass = '';
	        var itemStyle = '';
	        this.addItemBox( itemVal, itemDisplay, itemCaption, itemClass, itemStyle );
    	}
    },
    
    // private
    removeAllItems: function(){
    	this.items.each( function(item) {
            item.preDestroy(true);
        }, this );
        return this;
    },
    
    // private
    getCaption: function( node ) {
        if( typeof this.displayFieldTpl === 'string' ) {
            this.displayFieldTpl = new Ext.XTemplate( this.displayFieldTpl );
        }
        
        var caption;
        if( this.displayFieldTpl ) {
            caption = this.displayFieldTpl.apply( node.attributes );
        }
        else if( this.displayField ) {
            caption = node.attributes[this.displayField];
        }
        
        return caption;
    },
    
    addItemBox: function( itemVal, itemDisplay, itemCaption, itemClass, itemStyle ) {
        // check duplication
        var items = this.items;
        for( var i=0,len=items.getCount(); i<len; ++i ) {
        	var box = items.get( i );
        	if( box.value === itemVal )
        		return;
        }
        
        if( !this.multiSelect )
    		this.removeAllItems();
        
        var hConfig;
        var itemKey = Ext.id( null, 'sbx-item' );
        var box = new Ext.ux.form.SuperBoxSelectItem({
            owner: this,
            renderTo: this.wrapEl,
            caption: itemCaption,
            display: itemDisplay,
            value: itemVal,
            key: itemKey,
            listeners: {
                'remove': function(item){
                    if( this.fireEvent('beforeremoveitem',this,item.value) === false ) {
                        return;
                    }
                    this.items.removeKey( item.key );
                },
                destroy: function(){
                    this.collapse();
                    this.autoSize().validateValue();
                },
                scope: this
            }
        });
        box.render();
        
        hConfig = {
            tag :'input', 
            type :'hidden', 
            value : itemVal,
            name : (this.hiddenName || this.name)
        };
        
        if(this.disabled){
        	Ext.apply(hConfig,{
        	   disabled : 'disabled'
        	})
        }
        box.hidden = this.el.insertSibling(hConfig,'before');

        this.items.add( itemKey, box );
        this.applyEmptyText().autoSize().validateValue();
        
        if( this.multiSelect )
        	this.treePanel.getEl().alignTo( this.wrap, 'tl-bl?' );
    	else
    		this.collapse();
    },
    
    // private
    applyEmptyText: function(){
		this.setRawValue('');
        if(this.items.getCount() > 0){
            this.el.removeClass(this.emptyClass);
            this.setRawValue('');
            return this;
        }
        if(this.rendered && this.emptyText && this.getRawValue().length < 1){
            this.setRawValue(this.emptyText);
            this.el.addClass(this.emptyClass);
        }
        return this;
    },
    
    // private
    validateValue: function( val ) {
        if( this.items.getCount() === 0 ) {
             if( this.allowBlank ) {
                 this.clearInvalid();
                 return true;
             } else {
                 this.markInvalid( this.blankText );
                 return false;
             }
        }
        this.clearInvalid();
        return true;
    },
    
    // private
    markInvalid: function(msg) {
        var elp, t;

        if( !this.rendered || this.preventMark ) {
            return;
        }
        this.outerWrapEl.addClass(this.invalidClass);
        msg = msg || this.invalidText;

        switch (this.msgTarget) {
            case 'qtip':
                Ext.apply(this.el.dom, {
                    qtip    : msg,
                    qclass  : 'x-form-invalid-tip'
                });
                Ext.apply(this.wrapEl.dom, {
                    qtip    : msg,
                    qclass  : 'x-form-invalid-tip'
                });
                if (Ext.QuickTips) { // fix for floating editors interacting with DND
                    Ext.QuickTips.enable();
                }
                break;
            case 'title':
                this.el.dom.title = msg;
                this.wrapEl.dom.title = msg;
                this.outerWrapEl.dom.title = msg;
                break;
            case 'under':
                if (!this.errorEl) {
                    elp = this.getErrorCt();
                    if (!elp) { // field has no container el
                        this.el.dom.title = msg;
                        break;
                    }
                    this.errorEl = elp.createChild({cls:'x-form-invalid-msg'});
                    this.errorEl.setWidth(elp.getWidth(true) - 20);
                }
                this.errorEl.update(msg);
                Ext.form.Field.msgFx[this.msgFx].show(this.errorEl, this);
                break;
            case 'side':
                if (!this.errorIcon) {
                    elp = this.getErrorCt();
                    if (!elp) { // field has no container el
                        this.el.dom.title = msg;
                        break;
                    }
                    this.errorIcon = elp.createChild({cls:'x-form-invalid-icon'});
                }
                this.alignErrorIcon();
                Ext.apply(this.errorIcon.dom, {
                    qtip    : msg,
                    qclass  : 'x-form-invalid-tip'
                });
                this.errorIcon.show();
                this.on('resize', this.alignErrorIcon, this);
                break;
            default:
                t = Ext.getDom(this.msgTarget);
                t.innerHTML = msg;
                t.style.display = this.msgDisplay;
                break;
        }
        this.fireEvent('invalid', this, msg);
    },
    
    clearInvalid: function(){
        if( !this.rendered || this.preventMark ) {
            return;
        }
        
        this.outerWrapEl.removeClass( this.invalidClass );
        switch( this.msgTarget ) {
            case 'qtip':
                this.el.dom.qtip = '';
                this.wrapEl.dom.qtip = '';
                break;
            case 'title':
                this.el.dom.title = '';
                this.wrapEl.dom.title = '';
                this.outerWrapEl.dom.title = '';
                break;
            case 'under':
                if( this.errorEl ) {
                    Ext.form.Field.msgFx[this.msgFx].hide(this.errorEl, this);
                }
                break;
            case 'side':
                if(this.errorIcon){
                    this.errorIcon.dom.qtip = '';
                    this.errorIcon.hide();
                    this.un('resize', this.alignErrorIcon, this);
                }
                break;
            default:
                var t = Ext.getDom(this.msgTarget);
                t.innerHTML = '';
                t.style.display = 'none';
                break;
        }
        this.fireEvent('valid', this);
    },
    
    alignErrorIcon : function(){
        if(this.wrap){
            this.errorIcon.alignTo( this.wrap, 'tl-tr', [Ext.isIE ? 5 : 2, 3] );
        }
    },
    
    clearCurrentFocus : function(){
        if( this.currentFocus ) {
            this.currentFocus.onLnkBlur();
            this.currentFocus = null;
        }  
        return this;        
    },
    
    // private
    setupFormInterception: function(){
        var form;
        this.findParentBy(function(p){ 
            if(p.getForm){
                form = p.getForm();
            }
        });
        if(form){
        	var formGet = form.getValues;
            form.getValues = function(asString){
                this.el.dom.disabled = true;
                var oldVal = this.el.dom.value;
                this.setRawValue('');
                var vals = formGet.call(form);
                this.el.dom.disabled = false;
                this.setRawValue(oldVal);
                if(this.forceFormValue && this.items.getCount() === 0){
                	vals[this.name] = '';
                }
                return asString ? Ext.urlEncode(vals) : vals ;
            }.createDelegate(this);
        }
    },
    
    onResize: function(w, h, rw, rh) {
        var reduce = Ext.isIE6 ? 4 : Ext.isIE7 ? 1 : Ext.isIE8 ? 1 : 0;
        if(this.wrapEl){
            this._width = w;
            this.outerWrapEl.setWidth(w - reduce);
        }
        Ext.ux.form.TreeComboSuperBox.superclass.onResize.call(this, w, h, rw, rh);
        this.autoSize();
    },
    
    autoSize: function(){
        if(!this.rendered){
            return this;
        }
        if(!this.metrics){
            this.metrics = Ext.util.TextMetrics.createInstance(this.el);
        }
        var el = this.el,
            v = el.dom.value,
            d = document.createElement('div');

        if(v === "" && this.emptyText && this.items.getCount() < 1){
            v = this.emptyText;
        }
        d.appendChild(document.createTextNode(v));
        v = d.innerHTML;
        d = null;
        v += "&#160;";
        var w = Math.max(this.metrics.getWidth(v) +  24, 24);
        if(typeof this._width != 'undefined'){
            w = Math.min(this._width, w);
        }
        this.el.setWidth(w);
        
        if(Ext.isIE){
            this.el.dom.style.top='0';
        }
        this.fireEvent('autosize', this, w);
        return this;
    }
});

Ext.reg( 'treecombosuperbox', Ext.ux.form.TreeComboSuperBox );


/* 
 * The following codes are copied from 'Ext.ux.form.SuperBoxSelect' written by Dan Humphrey<dan.humphrey@technomedia.co.uk>
 * and do not touch.
 * Please check the following thread for details: http://www.extjs.com/forum/showthread.php?t=69307
 */
Ext.ux.form.SuperBoxSelectItem = function(config){
    Ext.apply( this,config );
    Ext.ux.form.SuperBoxSelectItem.superclass.constructor.call( this ); 
};

Ext.ux.form.SuperBoxSelectItem = Ext.extend(Ext.ux.form.SuperBoxSelectItem,Ext.Component, {
    initComponent : function(){
        Ext.ux.form.SuperBoxSelectItem.superclass.initComponent.call( this ); 
    },
    onElClick : function(e){
        var o = this.owner;
        o.clearCurrentFocus().collapse();
        if(o.navigateItemsWithTab){
            this.focus();
        }else{
            o.el.dom.focus();
            var that = this;
            (function(){
                this.onLnkFocus();
                o.currentFocus = this;
            }).defer(10,this);
        }
    },
    
    onLnkClick : function(e){
        if(e) {
            e.stopEvent();
        }
        this.preDestroy();
        if(!this.owner.navigateItemsWithTab){
            this.owner.el.focus();
        }
    },
    onLnkFocus : function(){
        this.el.addClass("x-superboxselect-item-focus");
        this.owner.outerWrapEl.addClass("x-form-focus");
    },
    
    onLnkBlur : function(){
        this.el.removeClass("x-superboxselect-item-focus");
        this.owner.outerWrapEl.removeClass("x-form-focus");
    },
    
    enableElListeners : function() {
        this.el.on('click', this.onElClick, this, {stopEvent:true});
       
        this.el.addClassOnOver('x-superboxselect-item x-superboxselect-item-hover');
    },

    enableLnkListeners : function() {
        this.lnk.on({
            click: this.onLnkClick,
            focus: this.onLnkFocus,
            blur:  this.onLnkBlur,
            scope: this
        });
    },
    
    enableAllListeners : function() {
        this.enableElListeners();
        this.enableLnkListeners();
    },
    disableAllListeners : function() {
        this.el.removeAllListeners();
        this.lnk.un('click', this.onLnkClick, this);
        this.lnk.un('focus', this.onLnkFocus, this);
        this.lnk.un('blur', this.onLnkBlur, this);
    },
    onRender : function(ct, position){
        
        Ext.ux.form.SuperBoxSelectItem.superclass.onRender.call(this, ct, position);
        
        var el = this.el;
        if(el){
            el.remove();
        }
        
        this.el = el = ct.createChild({ tag: 'li' }, ct.last());
        el.addClass('x-superboxselect-item');
        
        var btnEl = this.owner.navigateItemsWithTab ? ( Ext.isSafari ? 'button' : 'a') : 'span';
        var itemKey = this.key;
        
        Ext.apply(el, {
            focus: function(){
                var c = this.down(btnEl +'.x-superboxselect-item-close');
                if(c){
                	c.focus();
                }
            },
            preDestroy: function(){
                this.preDestroy();
            }.createDelegate(this)
        });
        
        this.enableElListeners();

        el.update(this.caption);

        var cfg = {
            tag: btnEl,
            'class': 'x-superboxselect-item-close',
            tabIndex : this.owner.navigateItemsWithTab ? '0' : '-1'
        };
        if(btnEl === 'a'){
            cfg.href = '#';
        }
        this.lnk = el.createChild(cfg);
        
        
        if(!this.disabled) {
            this.enableLnkListeners();
        }else {
            this.disableAllListeners();
        }
        
        this.on({
            disable: this.disableAllListeners,
            enable: this.enableAllListeners,
            scope: this
        });

        this.setupKeyMap();
    },
    setupKeyMap : function(){
        this.keyMap = new Ext.KeyMap(this.lnk, [
            {
                key: [
                    Ext.EventObject.BACKSPACE, 
                    Ext.EventObject.DELETE, 
                    Ext.EventObject.SPACE
                ],
                fn: this.preDestroy,
                scope: this
            }, {
                key: [
                    Ext.EventObject.RIGHT,
                    Ext.EventObject.DOWN
                ],
                fn: function(){
                    this.moveFocus('right');
                },
                scope: this
            },
            {
                key: [Ext.EventObject.LEFT,Ext.EventObject.UP],
                fn: function(){
                    this.moveFocus('left');
                },
                scope: this
            },
            {
                key: [Ext.EventObject.HOME],
                fn: function(){
                    var l = this.owner.items.get(0).el.focus();
                    if(l){
                        l.el.focus();
                    }
                },
                scope: this
            },
            {
                key: [Ext.EventObject.END],
                fn: function(){
                    this.owner.el.focus();
                },
                scope: this
            },
            {
                key: Ext.EventObject.ENTER,
                fn: function(){
                }
            }
        ]);
        this.keyMap.stopEvent = true;
    },
    moveFocus : function(dir) {
        var el = this.el[dir == 'left' ? 'prev' : 'next']() || this.owner.el;
	    el.focus.defer(100,el);
    },

    preDestroy : function(supressEffect) {
    	if(this.fireEvent('remove', this) === false){
	    	return;
	    }	
    	var actionDestroy = function(){
            if(this.owner.navigateItemsWithTab){
                this.moveFocus('right');
            }
            this.hidden.remove();
            this.hidden = null;
            this.destroy();
        };
        
        if(supressEffect){
            actionDestroy.call(this);
        } else {
            this.el.hide({
                duration: 0.2,
                callback: actionDestroy,
                scope: this
            });
        }
        return this;
    },
    kill : function(){
    	this.hidden.remove();
        this.hidden = null;
        this.purgeListeners();
        this.destroy();
    },
    onDisable : function() {
    	if(this.hidden){
    	    this.hidden.dom.setAttribute('disabled', 'disabled');
    	}
    	this.keyMap.disable();
    	Ext.ux.form.SuperBoxSelectItem.superclass.onDisable.call(this);
    },
    onEnable : function() {
    	if(this.hidden){
    	    this.hidden.dom.removeAttribute('disabled');
    	}
    	this.keyMap.enable();
    	Ext.ux.form.SuperBoxSelectItem.superclass.onEnable.call(this);
    },
    onDestroy : function() {
        Ext.destroy(
            this.lnk,
            this.el
        );
        
        Ext.ux.form.SuperBoxSelectItem.superclass.onDestroy.call(this);
    }
});
