# python
import cjson
from copy import deepcopy

# zope
from Products.Five import BrowserView
from zope.interface import implements

# products
from anz.dashboard.interfaces import IDashboardView, IDashboardEditView, \
     IDashboardCreateView
from anz.dashboard import MSG_FACTORY as _

class DashboardView( BrowserView ):
    ''' Provide 'Anz Dashboard' functions. '''
    
    implements( IDashboardView )
    
    def getPageLayout( self, retJson=True ):
        ''' Return page layout.
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains page layout, format like:
        {
            'success': True,
            'msg': 'Get page layout success.'
            'layout': 'tile'
        }
        
        '''
        ret = {}
        ret['success'] = True
        ret['msg'] = _(u'Get page layout success.')
        ret['layout'] = self.context.getPageLayout()
        
        return retJson and cjson.encode(ret) or ret
    
    def getPageConfig( self, pageIndex, retJson=True ):
        ''' Return layout config of specific page.
        
        @param pageIndex
        index of the page
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains page layout config, format like:
        {
            'success': True,
            'msg': 'Get page config success.'
            'config': {...}
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            if pageIndex in range(len(context._layoutCfg)):
                ret['success'] = True
                ret['msg'] = _(u'Add page success.')
                ret['config'] = context._layoutCfg[pageIndex]
            else:
                ret['success'] = False
                ret['msg'] = _(u'Wrong page index.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def getLayoutConfig( self, retJson=True ):
        ''' Return layout configure of current object.
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains layout config, format like:
        {
            'success': True,
            'msg': 'Get layout config success.',
            'config': [{'style': '',
                'title': 'page title',
                'width': '100%',
                'columns': [{'style': '',
                    'width': '21%',
                    'portlets': [{'id': 'portlet_weather',
                        'options': {...}},
                        {'id': 'portlet_hot_contents',
                        'options': {}},
                        ...
                        ]
                      },
                      ...
                      ]
                      },
                      ...
                      ]
        }
        
        '''
        context = self.context
        ret = {}
        ret['success'] = True
        ret['msg'] = _(u'Get layout config success.')
        ret['config'] = context.getConfig( retStr=False )
        
        return retJson and cjson.encode(ret) or ret

class DashboardEditView( BrowserView ):
    ''' Dashboard edit functions interface. '''
    
    implements( IDashboardEditView )
    
    #
    # page
    #
    def addPage( self, pageIndex=-1, retJson=True ):
        ''' Add a new page to dashboard at position pageIndex.
        The page has two columns as default, if pageIndex is -1 then add the
        page at the end of the dashboard.
        
        @param pageIndex
        index of the page( default is -1, append to the end)
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Add page success.'
            'pageIndex': new page index (from 0)
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            if pageIndex == -1:
                pageIndex = len( context._layoutCfg )
            
            context._layoutCfg.insert( pageIndex,
                                       deepcopy(context.defaultPageConfig) )
            
            # add two default columns for the new page
            self.addColumn( pageIndex=pageIndex )
            self.addColumn( pageIndex=pageIndex )
            
            # notify change
            context._p_changed = True
            
            ret['success'] = True
            ret['msg'] = _(u'Add page success.')
            ret['pageIndex'] = pageIndex
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def editPage( self, pageIndex, title='Untitled page', width=100,
                  style='', retJson=True ):
        ''' Edit page layout config.
        
        @param pageIndex
        index of the page to be edit
        
        @param title
        title of the page( default is 'Untitled page' )
        
        @param width
        width of the page in percentage( default is 100 )
        
        @param style
        style of the page( default is '' )
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Edit page success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            if pageIndex in range(len(context._layoutCfg)):
                context._layoutCfg[pageIndex]['title']= title
                context._layoutCfg[pageIndex]['width']= width
                context._layoutCfg[pageIndex]['style']= style
                
                # notify change
                context._p_changed = True
                
                ret['success'] = True
                ret['msg'] = _(u'Edit page success.')
            else:
                ret['success'] = False
                ret['msg'] = _(u'Wrong page index.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def movePage( self, pageIndex, toPage, retJson=True ):
        ''' Move a page from pageIndex to toIndex.
        
        @param pageIndex
        index of the page be moved
        
        @param toPage
        index of the page moved to
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Move page success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            indexRange = range( len(context._layoutCfg) )
            if pageIndex not in indexRange:
                ret['success'] = False
                ret['msg'] = _(u'Wrong page index.')
            elif toPage not in indexRange:
                ret['success'] = False
                ret['msg'] = _(u'Wrong to page index.')
            else:
                page = context._layoutCfg.pop( pageIndex )
                context._layoutCfg.insert( toPage, page )
                
                # notify change
                context._p_changed = True
                
                ret['success'] = True
                ret['msg'] = _(u'Move page success.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def delPage( self, pageIndex, retJson=True ):
        ''' Delete specific page.
        Note: If there is only one page left, can not delete the page.
        
        @param pageIndex
        index of the page to be deleted
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Delete page success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            if len(context._layoutCfg) > 1:
                del context._layoutCfg[pageIndex]
                context._p_changed = True
                
                ret['success'] = True
                ret['msg'] = _(u'Delete page success.')
            else:
                # can't delete the last page!
                ret['success'] = False
                ret['msg'] = _(u'Can not delete the last page!')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    #
    # column
    #
    def addColumn( self, pageIndex=0, columnIndex=-1, retJson=True ):
        ''' Add a new column.
        
        @param pageIndex
        index of the page( default is 0, first page )
        
        @param columnIndex
        index of the column( default is -1, append to the end )
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Add column success.'
            'columnIndex': new column index(from 0)
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            if columnIndex == -1:
                columnIndex = len( context._layoutCfg[pageIndex]['columns'] )
            
            context._layoutCfg[pageIndex]['columns'].insert(
                columnIndex, deepcopy(context.defaultColumnConfig) )
            
            context._p_changed = True
            
            ret['success'] = True
            ret['msg'] = _(u'Add column success.')
            ret['columnIndex'] = columnIndex
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def changeColumnsWidth( self, pageIndex, widths=[], retJson=True ):
        ''' Change width of the columns.
        
        @param pageIndex
        index of the page
        
        @param widths
        list of column width( width in percentage with string format )
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Change columns width success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            columns = context._layoutCfg[pageIndex]['columns']
            assert len(widths)==len(columns), 'Wrong width number!'
            
            for i in range(len(columns)):
                columns[i]['width'] = str(widths[i])
            
            context._p_changed = True
            
            ret['success'] = True
            ret['msg'] = _(u'Change columns width success.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def moveColumn( self, pageIndex, columnIndex, toColumn, retJson=True ):
        ''' Move a widget to specific position.
        
        @param pageIndex
        index of page the column lies on( start from 0 )
        
        @param columnIndex
        index of column( start from 0 )
        
        @param toColumn
        index of new column
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Move column success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            columns = context._layoutCfg[pageIndex]['columns']
            indexRange = range( len(columns) )
            if columnIndex not in indexRange:
                ret['success'] = False
                ret['msg'] = _(u'Wrong column index.')
            elif toColumn not in indexRange:
                ret['success'] = False
                ret['msg'] = _(u'Wrong to column index.')
            else:
                column = columns.pop( columnIndex )
                columns.insert( toColumn, column )
                
                # notify change
                context._p_changed = True
                
                ret['success'] = True
                ret['msg'] = _(u'Move column success.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def delColumn( self, pageIndex, columnIndex, retJson=True ):
        ''' Delete specific column.
        
        @param pageIndex
        index of the page the column belongs to
        
        @param columnIndex
        index of the column to be deleted
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Delete column success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            if len(context._layoutCfg[pageIndex]['columns']) > 1:
                del context._layoutCfg[pageIndex]['columns'][columnIndex]
                context._p_changed = True
                
                ret['success'] = True
                ret['msg'] = _(u'Delete column success.')
            else:
                # can't delete the last column!
                ret['success'] = False
                ret['msg'] = _(u'Can not delete the last column!')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    #
    # widget
    #
    def addWidget( self, widgetId, pageIndex, columnIndex,
                   widgetIndex=0, retJson=True ):
        ''' Add a widget to a specific position.
        
        @param widgetId
        id of widget
        
        @param pageIndex
        index of page the widget lies on( start from 0 )
        
        @param columnIndex
        index of column the widget lies on( start from 0 )
        
        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Add widget success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            widgetCfg = deepcopy( context.defaultWidgetCfg )
            widgetCfg['id'] = widgetId
            context._layoutCfg[pageIndex]['columns'][columnIndex]['widgets'].\
                   insert( widgetIndex, widgetCfg )
            
            context._p_changed = True
            
            ret['success'] = True
            ret['msg'] = _(u'Add widget success.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def changeWidgetColor( self, pageIndex, columnIndex, widgetIndex,
                           color, retJson=True ):
        ''' change color of widget.
        
        @param pageIndex
        index of page the widget lies on( start from 0 )
        
        @param columnIndex
        index of column the widget lies on( start from 0 )
        
        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )
        
        @param color
        widget color
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Change widget color success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            pageCfg = context._layoutCfg[pageIndex]
            widgetCfg = pageCfg['columns'][columnIndex]['widgets'][widgetIndex]
            if 'color' in widgetCfg.keys():
                widgetCfg['color'] = color
                context._p_changed = True
                
                ret['success'] = True
                ret['msg'] = _(u'Change widget color success.')
            else:
                ret['success'] = False
                ret['msg'] = _(u'No color attribute found.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def changeWidgetOptions( self, pageIndex, columnIndex, widgetIndex,
                             names=[], retJson=True, **kw ):
        ''' Change options of widget.
        
        @param pageIndex
        index of page the widget lies on( start from 0 )
        
        @param columnIndex
        index of column the widget lies on( start from 0 )
        
        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )
        
        @param names
        list contains widget options name
        
        @param retJson
        format return value to json format or not( default True )
        
        @param **kw
        widget options( default is request )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Change widget options success.',
            'options': {...}
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            if not kw:
                kw = dict( self.request )
            
            pageCfg = context._layoutCfg[pageIndex]
            widgetCfg = pageCfg['columns'][columnIndex]['widgets'][widgetIndex]
            if 'options' in widgetCfg.keys():
                # build options
                options = {}
                for name in names:
                    options[name] = kw[name]
                
                widgetCfg['options'] = options
                context._p_changed = True
                
                ret['success'] = True
                ret['msg'] = _(u'Change widget options success.')
                ret['options'] = options
            else:
                ret['success'] = False
                ret['msg'] = _(u'No options attribute found.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def collapseWidget( self, pageIndex, columnIndex, widgetIndex,
                        collapse, retJson=True ):
        ''' Collapse or expand specific widget.
        
        @param pageIndex
        index of page the widget lies on( start from 0 )
        
        @param columnIndex
        index of column the widget lies on( start from 0 )
        
        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )
        
        @param collapse
        widget collapse status, True means collapse, False means expand
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Change widget collapse state success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            pageCfg = context._layoutCfg[pageIndex]
            widgetCfg = pageCfg['columns'][columnIndex]['widgets'][widgetIndex]
            if 'collapse' in widgetCfg.keys():
                widgetCfg['collapse'] = collapse
                context._p_changed = True
                
                ret['success'] = True
                ret['msg'] = _(u'Change widget collapse state success.')
            else:
                ret['success'] = False
                ret['msg'] = _(u'No collapse attribute found.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def moveWidget( self, pageIndex, columnIndex, widgetIndex,
                    toPage, toColumn, toWidget, retJson=True ):
        ''' Move a widget to specific position.
        
        @param pageIndex
        index of page the widget lies on( start from 0 )
        
        @param columnIndex
        index of column the widget lies on( start from 0 )
        
        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )
        
        @param toPage
        index of new page
        
        @param toColumn
        index of new column
        
        @param toWidget
        index of new widget position
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Move widget success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            # remove from old position
            pageCfg = context._layoutCfg[pageIndex]
            widgets = pageCfg['columns'][columnIndex]['widgets']
            widgetCfg = widgets.pop( widgetIndex )
            
            # insert into new position
            newPageCfg = context._layoutCfg[toPage]
            newWidgets = newPageCfg['columns'][toColumn]['widgets']
            newWidgets.insert( toWidget, widgetCfg )
            
            # notify change
            context._p_changed = True
            
            ret['success'] = True
            ret['msg'] = _(u'Move widget success.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def delWidget( self, pageIndex, columnIndex, widgetIndex, retJson=True ):
        ''' Delete specific widget from current dashboard.
        
        @param pageIndex
        index of page the widget lies on( start from 0 )
        
        @param columnIndex
        index of column the widget lies on( start from 0 )
        
        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )
        
        @retJson
        format return value to json format or not( default True )
        
        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Delete widget success.'
        }
        
        '''
        context = self.context
        ret = {}
        
        try:
            colCfg = context._layoutCfg[pageIndex]['columns'][columnIndex]
            del colCfg['widgets'][widgetIndex]
            context._p_changed = True
            
            ret['success'] = True
            ret['msg'] = _(u'Delete widget success.')
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
class DashboardCreateView( BrowserView ):
    ''' Provide 'Anz Dashboard' type create functions. '''
    
    implements( IDashboardCreateView )
    
    def create( self, title='Untitled object', layout='tile', retJson=True ):
        ''' Create 'Anz Dashboard' instance
        
        @param title
        title of the new instance( default 'Untitled object' )
        
        @param layout
        layout of dashboard pages, one of 'tab' and 'tile'( default 'tile' )
        
        @retJson
        format return value to json format or not( default True )
        
        @return status of create process
        json data:
        {
            success: True,
            msg: 'Create "Anz Dashboard" instance success.',
            id: 'id1',
            title: 'title',
            url: 'url',
            path: 'path'
        }
        
        '''
        context = self.context
        ret = {}
        success = True
        msg = _(u'Create "Anz Dashboard" instance success.')
        
        try:
            instance = self._createInstance( title, layout )
            ret['id'] = instance.getId()
            ret['title'] = unicode( instance.Title() )
            ret['url'] = instance.absolute_url()
            ret['path'] = '/'.join(instance.getPhysicalPath())
        except Exception, e:
            success = False
            msg = str(e)
        
        ret['success'] = success
        ret['msg'] = msg
        
        return retJson and cjson.encode(ret) or ret
    
    # private help func
    def _createInstance( self, title, layout ):
        context = self.context
        type_name = 'Anz Dashboard'
        id = context.generateUniqueId( type_name )
        id = id.replace( '.', '-' )
        id = context.invokeFactory( id=id, type_name=type_name )
        obj = getattr( context, id, None )
        obj.setTitle( title )
        obj.setLayout( layout )
        obj.reindexObject()
        
        return obj
