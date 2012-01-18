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

Anz.widget.staticText = Ext.extend( Anz.widget.base, {
    bodyStyle: 'padding: 5px',
    iconCls: 'widget_postit_icon',
    
    getCustomisePreferences: function() {
    	return [{
    		'xtype': 'htmleditor',
    		'name': 'text',
    		'fieldLabel': _('body'),
    		'value': _('Type text here')
    	}];
    },
    
    updateOptions: function( options ) {
    	this.options = options;
    	this.setTitle( Utf8.decode(options.title) );
    	this.display();
    },
  	
  	display: function() {
    	var text = this.getValue('text');
        if( !text ) {
            text = _('Type text here');
        }
        else {
        	text = Utf8.decode(text);
        }
        
        this.body.update( text );
    },
    
  	/* Method: convertTextToHTML

    convert a pure text string in "html" (convert < > to html equivalent,
    replace \n by <br> and double space by &nbsp; (??)
    
    Parameters:
    * String - s : pure text 

    Returns:
    * String

    */ 
    convertTextToHTML: function(s) {
        s = s.replace(/\&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br>").replace(/  /g, "&nbsp; ");
        return s;
    },

    /* Method: convertHTMLToText

    convert an "html" string to pure text (inverse of convertTextToHTML)
    
    Parameters:
    * String - s : html string

    Returns:
    * String

    */ 
    convertHTMLToText: function(s) {
        s = s.replace(/\&amp;/g,"&").replace(/\&lt;/g,"<").replace(/&gt;/g,">").replace(/<br>/g,"\n").replace(/\&nbsp;/g, " ");
        return s;
    }
});

Ext.reg( 'widget_static_text', Anz.widget.staticText );
