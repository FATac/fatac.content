/*!
 * Ext JS Library 3.0.0
 * Copyright(c) 2006-2009 Ext JS, LLC
 * licensing@extjs.com
 * http://www.extjs.com/license
 */
Ext.ux.PortalColumn = Ext.extend(Ext.Panel, {
    layout : 'anchor',
    //autoEl : 'div',//already defined by Ext.Component
    frame: false,
    border: false,
    closable: true,
    defaultType: 'portlet',
    cls: 'x-column-portal'
});

Ext.reg('portalcolumn', Ext.ux.PortalColumn);
