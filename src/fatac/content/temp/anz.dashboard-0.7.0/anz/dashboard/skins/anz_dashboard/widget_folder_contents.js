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

Anz.widget.folderContents = Ext.extend( Anz.widget.base, {
    iconCls: 'widget_folder_contents_icon',
    
    // contents entries
    entries: [],
    
    // current page number
    page: 0,
    
    // total page count
    pageCount: 1,
    
    // entries count per page
    count: null,
    
    getCustomisePreferences: function() {
    	// calc portal id
    	var portal = this.portalUrl.split('/').pop();
    	
    	return [{
    		'xtype': 'treecombosuperbox',
    		'name': 'paths',
    		'fieldLabel': _('Paths'),
			'hiddenName': 'paths:list',
			'navigateItemsWithTab': true,
			'resizable': true,
			'allowBlank': false,
			'msgTarget': 'under',
			'displayFieldTpl': '{text}',
			'value': '/' + portal,
			'multiSelect': true,
			'treeWidth': 353,
			
			'treeConfig': {
				height: 110,
				rootVisible: true,
				autoScroll: true,
				root: {
	                nodeType: 'async',
	                text: _('Root'),
	                id: 'root',
	                expanded: true,
	                path: '/' + portal
	            },
	            loader: {
	            	url: this.contextUrl + '/@@folderContentsWidget/getChildNodesData'
	            },
	            listeners: {
	            	beforeload: {
	            		fn: function( node ) {
							var loader = node.getOwnerTree().getLoader();
							loader.baseParams.path = node.attributes.path;
						}
	            	},
	            	click: {
	            		fn: function( node, e ) {
					        var itemVal = node.attributes.path;
					        var itemDisplay = node.text;
					        var itemCaption = this.getCaption( node );
					        var itemClass = '';
					        var itemStyle = '';
					        this.addItemBox( itemVal, itemDisplay, itemCaption, itemClass, itemStyle );
					    }
	            	}
	            }
			}
    	},{
    		'xtype': 'xcheckbox',
    		'name': 'searchSub',
    		'fieldLabel': _('Search sub-directory?'),
    		'submitOffValue': 0,
    		'submitOnValue': 1,
    		'value': 0,
    		'hiddenName': 'searchSub:int'
    	},{
            xtype: 'multiselect',
            fieldLabel: _('Types'),
            name: 'types',
            width: 360,
            height: 'auto',
            allowBlank: true,
            displayField: 'name',
            valueField: 'id',
            store: new Ext.data.JsonStore({
			    autoDestroy: true,
			    autoLoad: true,
			    url: this.contextUrl + '/@@folderContentsWidget/types',
			    root: 'types',
			    fields: ['id','name']
			})
        },{
    		'xtype': 'numberfield',
    		'name': 'recentDays',
    		'fieldLabel': _('Recent days'),
    		'value': 0,
    		'allowBlank': false,
    		'allowDecimals': false,
    		'allowNegative': false
    	},{
    		'xtype': 'numberfield',
    		'name': 'sort_limit',
    		'fieldLabel': _('Max count'),
    		'value': 0,
    		'allowBlank': false,
    		'allowDecimals': false,
    		'allowNegative': false
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
    		searchSub: 0,
    		recentDays: 0,
    		sort_limit: 0,
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
    		var oldPaths = oldOptions.paths;
    		var oldTypes = oldOptions.types;
    		var oldSearchSub = oldOptions.searchSub;
    		var oldRecentDays = oldOptions.recentDays;
    		var oldSortLimit = oldOptions.sort_limit;
    		var oldView = oldOptions.view;
    		var oldPaging = oldOptions.paging;
    		
	    	if( (oldPaths!==this.getValue('paths')) ||
	    		(oldTypes!==this.getValue('types')) ||
	    		(oldSearchSub!==this.getValue('searchSub')) ||
	    		(oldRecentDays!==this.getValue('recentDays')) ||
	    		(oldSortLimit!==this.getValue('sort_limit')) ) {
		    	this.display();
		    }
		    else if( (oldView!==this.getValue('view')) ||
		    		 (oldPaging!==this.getValue('paging')) ) {
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
    	
    	var paths = this.getValue( 'paths' );
    	var types = this.getValue( 'types' );
    	var searchSub = this.getValue( 'searchSub' );
    	var recentDays = this.getValue( 'recentDays' );
    	var sort_limit = this.getValue( 'sort_limit' );
        Ext.Ajax.request({
    	    url: this.contextUrl + '/@@folderContentsWidget/items',
    	    method: 'POST',
        	params: {
        		'paths:list': paths,
        		'searchSub': searchSub,
        		'portal_types': types,
        		'recentDays:int': recentDays,
        		'sort_limit:int': sort_limit
			},
			timeout: 5000,
    	    scope: this,
    	    success: function ( result, request ) {
				var ret = Ext.decode( result.responseText );
				if( ret.success ) {
					this.entries = ret.items;
					this.count = parseInt( this.getValue('count') );
					this.pageCount = Math.ceil( this.entries.length/this.count );
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
  		
  		var html = '<ul class="itemList">';
		var itemT = new Ext.Template(
			'<li>',
				'<img width="16" height="16" src="{iconSrc}">',
				'<a href="{link}" title="{desc}" target="_blank">',
					'{title}',
				'</a>',
				'<span class="byline">',
                	' - <a href="{authorLink}" target="_blank">',
						'{author}',
					'</a>',
					'<span title="{date}" class="itemDate"> - {shortDate}</span>',
                '</span>',
			'</li>'
		);
		
		for( var i=0,len=entries.length; i<len; ++i ) {
			var entry = entries[i];
			
			var iconSrc = '';
			if(entry.icon)
			    iconSrc = this.portalUrl + '/' + entry.icon;
			
			html += itemT.applyTemplate({
				iconSrc: iconSrc,
				title: entry.title,
				desc: entry.desc,
				link: entry.url,
				authorLink: this.portalUrl + '/author/' + entry.author_id,
				author: entry.author,
				date: entry.modified,
				shortDate: new Date(entry.modified).format('Y/m/d')
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
					'<img height="234" width="234" src="{img}"/>',
				'</div>',
				'<div class="article">',
					'<h3><a href="{link}" target="_blank">{title}</a></h3>',
					'<span class="byline">',
	                	' - <a href="{authorLink}" target="_blank">',
							'{author}',
						'</a>',
						'<span title="{date}" class="itemDate"> - {shortDate}</span>',
	                '</span>',
					'<p>{desc}</p>',
				'</div>',
			'</div>'
		);
		
		var first = entries[0];
		html.push( firstItemT.applyTemplate({
			title: first.title,
			desc: first.desc,
			img: this.portalUrl + '/default_news.png',
			link: first.link,
			authorLink: this.portalUrl + '/author/' + first.author_id,
			author: first.author,
			date: first.modified,
			shortDate: new Date(first.modified).format('Y/m/d')
		}) );
		
		html.push( '<div class="right">' );
		
		var	otherItemT = new Ext.Template(
			'<div class="item">',
				'<div class="thumbnail">',
					'<img height="50" width="50" src="{img}"/>',
				'</div>',
				'<div class="title">',
					'<h3><a href="{link}" target="_blank">{title}</a></h3>',
					'<span class="byline">',
	                	' - <a href="{authorLink}" target="_blank">',
							'{author}',
						'</a>',
						'<span title="{date}" class="itemDate"> - {shortDate}</span>',
	                '</span>',
				'</div>',
				'<p>{desc}</p>',
			'</div>'
		);
		
		for( var i=1,len=entries.length; i<len; ++i ) {
			var entry = entries[i];
			html.push( otherItemT.applyTemplate({
				title: entry.title,
				desc: entry.desc,
				img: this.portalUrl + '/default_news.png',
				link: entry.link,
				authorLink: portalUrl + '/author/' + entry.author_id,
				author: entry.author,
				date: entry.modified,
				shortDate: new Date(entry.modified).format('Y/m/d')
			}) );
		}
		
		html.push( '</div></div>' );
		
		return html.join('');
  	},
  	
  	buildSlideshowHtml: function( entries ) {
  		var entries = this.entries;
  		
  		var slideshowEId = this.getId() + '_slideshow';
  		var html = [String.format('<div class="slideshowView" id="{0}">',slideshowEId)];
		var itemT = new Ext.Template(
			'<div class="item">',
				'<div class="crop">',
					'<img src="{img}">',
				'</div>',
				'<div class="content">',
					'<div class="title">',
						'<h3><a href="{link}" target="_blank">{title}</a></h3>',
					'</div>',
					'<span class="byline">',
	                	' - <a href="{authorLink}" target="_blank">',
							'{author}',
						'</a>',
						'<span title="{date}" class="itemDate"> - {shortDate}</span>',
	                '</span>',
					'<p>{desc}</p>',
				'</div>',
			'</div>'
		);
		
		for( var i=0,len=entries.length; i<len; ++i ) {
			var entry = entries[i];
			html.push( itemT.applyTemplate({
				img: this.portalUrl + '/default_news.png',
				title: entry.title,
				desc: entry.desc,
				link: entry.link,
				authorLink: this.portalUrl + '/author/' + entry.author_id,
				author: entry.author,
				date: entry.modified,
				shortDate: new Date(entry.modified).format('Y/m/d')
			}) );
		}
		html.push( '</div>' );
		
		return html.join('');
  	},
  	
  	buildHeadlineHtml: function( entries ) {
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
					'<span class="byline">',
	                	' - <a href="{authorLink}" target="_blank">',
							'{author}',
						'</a>',
						'<span title="{date}" class="itemDate"> - {shortDate}</span>',
	                '</span>',
				'</div>',
			'</div>',
			'<div class="middle odd">',
				'<p>{desc}</p>',
			'</div>'
		);
		
		var first = entries[0];
		html.push( firstItemT.applyTemplate({
			img: this.portalUrl + '/default_news.png',
			title: first.title,
			desc: first.desc,
			link: first.link,
			authorLink: this.portalUrl + '/author/' + first.author_id,
			author: first.author,
			date: first.modified,
			shortDate: new Date(first.modified).format('Y/m/d')
		}) );
		
		html.push( '<ul class="bottom">' );
		
		var	otherItemT = new Ext.Template(
			'<li class="item {cls}">',
				'<div class="thumbnail">',
					'<img height="50" width="50" src="{img}">',
				'</div>',
				'<h3><a href="{link}" target="_blank">{title}</a></h3>',
				'<span class="byline">',
                	' - <a href="{authorLink}" target="_blank">',
						'{author}',
					'</a>',
					'<span title="{date}" class="itemDate"> - {shortDate}</span>',
                '</span>',
				'<p>{desc}</p>',
			'</li>'
		);
		
		for( var i=1,len=entries.length; i<len; ++i ) {
			var entry = entries[i];
			html.push( otherItemT.applyTemplate({
				cls: i%2 ? 'even' : 'odd',
				img: this.portalUrl + '/default_news.png',
				title: entry.title,
				desc: entry.desc,
				link: entry.link,
				authorLink: this.portalUrl + '/author/' + entry.author_id,
				author: entry.author,
				date: entry.modified,
				shortDate: new Date(entry.modified).format('Y/m/d')
			}) );
		}
		
		html.push( '</ul></div>' );
		
		return html.join('');
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
			returnStr = days + 'days before';
		}
		else if( hours > 0 ) {
			returnStr = hours + 'hours before';
		}
		else if( minutes > 0 ) {
			returnStr = minutes + 'minutes before';
		}
	
		return returnStr;
	}
});

Ext.reg( 'widget_folder_contents', Anz.widget.folderContents );
