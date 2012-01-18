# python
import os, sys
from copy import deepcopy

# cmf
from Products.CMFCore.ActionInformation import ActionCategory, Action

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestDashboardView( AnzDashBoardTestCase ):

    def afterSetUp( self ):
        self.folder.invokeFactory( type_name='Document',
                                   id='doc1', title='doc 1' )
        self.folder.doc1.indexObject()
        
        self.folder.invokeFactory( type_name='Anz Dashboard',
                                   id='dashboard1', title='dashboard 1' )
        self.folder.dashboard1.indexObject()
    
    def test_viewApplied( self ):
        view = self.folder.doc1.restrictedTraverse( '@@dashboardView', None )
        self.assert_( view is None )
        
        view = self.folder.dashboard1.restrictedTraverse( '@@dashboardView', None )
        self.assert_( view is not None )
    
    def test_getPageLayout( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardView', None )
        
        # test default
        ret = view.getPageLayout( retJson=False )
        self.assertEqual( ret['success'], True )
        self.assertEqual( ret['layout'], 'tile' )
        
        # edit layout
        dashboard.setPageLayout( 'tab' )
        
        ret = view.getPageLayout( retJson=False )
        self.assertEqual( ret['success'], True )
        self.assertEqual( ret['layout'], 'tab' )
    
    def test_getPageConfig( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardView', None )
        
        # test default page config
        ret = view.getPageConfig( pageIndex=0, retJson=False )
        self.assertEqual( ret['success'], True )
        
        pageCfg = deepcopy( dashboard.defaultPageConfig )
        pageCfg['columns'].append( dashboard.defaultColumnConfig )
        pageCfg['columns'].append( dashboard.defaultColumnConfig )
        self.assertEqual( ret['config'], pageCfg )
        
        # test wrong page index
        ret = view.getPageConfig( pageIndex=1, retJson=False )
        self.assertEqual( ret['success'], False )
    
    def test_getLayoutConfig( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardView', None )
        
        # test default layout config
        layoutCfg = deepcopy( dashboard.defaultPageConfig )
        layoutCfg['columns'].append( dashboard.defaultColumnConfig )
        layoutCfg['columns'].append( dashboard.defaultColumnConfig )
        
        ret = view.getLayoutConfig( retJson=False )
        self.assertEqual( ret['success'], True )
        self.assertEqual( ret['config'], [layoutCfg] )
    
class TestDashboardEditView( AnzDashBoardTestCase ):

    def afterSetUp( self ):
        self.folder.invokeFactory( type_name='Document',
                                   id='doc1', title='doc 1' )
        self.folder.doc1.indexObject()
        
        self.folder.invokeFactory( type_name='Anz Dashboard',
                                   id='dashboard1', title='dashboard 1' )
        self.folder.dashboard1.indexObject()
    
    def test_viewApplied( self ):
        view = self.folder.doc1.restrictedTraverse( '@@dashboardEdit', None )
        self.assert_( view is None )
        
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        self.assert_( view is not None )
    
    def test_addPage( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # default dashboard contains 1 page
        self.assert_( len(dashboard._layoutCfg) == 1 )
        
        ret = view.addPage( retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( len(dashboard._layoutCfg) == 2 )
    
    def test_editPage( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # edit title
        ret = view.editPage( 0, title='page 1', retJson=False )
        self.assertEqual( ret['success'], True )
        self.assertEqual( dashboard._layoutCfg[0]['title'], 'page 1' )
        
        # wrong page index
        ret = view.editPage( 1, title='page 2', retJson=False )
        self.assertEqual( ret['success'], False )
    
    def test_delPage( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # default dashboard contains 1 page
        self.assert_( len(dashboard._layoutCfg) == 1 )
        
        ret = view.addPage( retJson=False )
        ret = view.addPage( retJson=False )
        ret = view.addPage( retJson=False )
        self.assert_( len(dashboard._layoutCfg) == 4 )
        
        ret = view.delPage( 0, retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( len(dashboard._layoutCfg) == 3 )
        
        ret = view.delPage( 0, retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( len(dashboard._layoutCfg) == 2 )
        
        ret = view.delPage( 0, retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( len(dashboard._layoutCfg) == 1 )
        
        # del last page failure
        ret = view.delPage( 0, retJson=False )
        self.assert_( ret['success'] == False )
        self.assert_( len(dashboard._layoutCfg) == 1 )
    
    def test_movePage( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # add a page
        view.addPage( retJson=False )
        
        # move page 0 to 1
        ret = view.movePage( 0, 1, retJson=False )
        self.assertEqual( ret['success'], True )
        
        # wrong page index
        ret = view.movePage( 2, 1, retJson=False )
        self.assertEqual( ret['success'], False )
        
        # wrong to page index
        ret = view.movePage( 0, 2, retJson=False )
        self.assertEqual( ret['success'], False )
    
    def test_addColumn( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # default page contains 2 column
        pageCfg = dashboard._layoutCfg[0]
        self.assert_( len(pageCfg['columns']) == 2 )
        
        view.addColumn()
        self.assert_( len(pageCfg['columns']) == 3 )
        
        view.addColumn()
        self.assert_( len(pageCfg['columns']) == 4 )
    
    def test_changeColumnsWidth( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        pageCfg = dashboard._layoutCfg[0]
        ret = view.changeColumnsWidth( 0, ['0.6','0.4'], retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( pageCfg['columns'][0]['width'] == '0.6' )
        self.assert_( pageCfg['columns'][1]['width'] == '0.4' )
        
        ret = view.changeColumnsWidth( 0, ['0.7','0.3'], retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( pageCfg['columns'][0]['width'] == '0.7' )
        self.assert_( pageCfg['columns'][1]['width'] == '0.3' )
    
    def test_moveColumn( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        pageCfg = dashboard._layoutCfg[0]
        ret = view.changeColumnsWidth( 0, ['0.6','0.4'], retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( pageCfg['columns'][0]['width'] == '0.6' )
        self.assert_( pageCfg['columns'][1]['width'] == '0.4' )
        
        # move col 0 to index 1
        ret = view.moveColumn( 0, 0, 1, retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( pageCfg['columns'][0]['width'] == '0.4' )
        self.assert_( pageCfg['columns'][1]['width'] == '0.6' )
        
        # move col 0 to index 1
        ret = view.moveColumn( 0, 0, 1, retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( pageCfg['columns'][0]['width'] == '0.6' )
        self.assert_( pageCfg['columns'][1]['width'] == '0.4' )
        
        # wrong col index
        ret = view.moveColumn( 0, 2, 1, retJson=False )
        self.assert_( ret['success'] == False )
        
        # wrong to col index
        ret = view.moveColumn( 0, 0, 2, retJson=False )
        self.assert_( ret['success'] == False )
    
    def test_delColumn( self ):
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # default page contains 2 column
        pageCfg = dashboard._layoutCfg[0]
        view.addColumn()
        view.addColumn()
        self.assert_( len(pageCfg['columns']) == 4 )
        
        view.delColumn( 0, 0 )
        self.assert_( len(pageCfg['columns']) == 3 )
        
        view.delColumn( 0, 0 )
        self.assert_( len(pageCfg['columns']) == 2 )
        
        view.delColumn( 0, 0 )
        self.assert_( len(pageCfg['columns']) == 1 )
        
        # del last column failure
        ret = view.delColumn( 0, 0, retJson=False )
        self.assertEqual( ret['success'], False )
        self.assert_( len(pageCfg['columns']) == 1 )
    
    def test_addWidget( self ):
        self._registerWidgets()
        
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        widgets = dashboard._layoutCfg[0]['columns'][0]['widgets']
        self.assert_( len(widgets) == 0 )
        
        view.addWidget( 'widget1', 0, 0 )
        self.assert_( len(widgets) == 1 )
        
        view.addWidget( 'widget2', 0, 0 )
        self.assert_( len(widgets) == 2 )
    
    def test_changeWidgetColor( self ):
        self._registerWidgets()
        
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # add 2 widgets in first column
        widgets = dashboard._layoutCfg[0]['columns'][0]['widgets']
        view.addWidget( 'widget1', 0, 0 )
        view.addWidget( 'widget2', 0, 0 )
        
        self.assert_( widgets[0]['color'] == '' )
        self.assert_( widgets[1]['color'] == '' )
        
        ret = view.changeWidgetColor( 0, 0, 0, 'AAA', retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( widgets[0]['color'] == 'AAA' )
        self.assert_( widgets[1]['color'] == '' )
    
    def test_changeWidgetOptions( self ):
        self._registerWidgets()
        
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # add 2 widgets in first column
        widgets = dashboard._layoutCfg[0]['columns'][0]['widgets']
        view.addWidget( 'widget1', 0, 0 )
        view.addWidget( 'widget2', 0, 0 )
        
        self.assert_( widgets[0]['options'] == {'title': 'Un-titled widget'} )
        self.assert_( widgets[1]['options'] == {'title': 'Un-titled widget'} )
        
        #ret = view.changeWidgetOptions( 0, 0, 0,
        #                                {'title':'title 1'}, retJson=False )
        request = self.app.REQUEST
        request.set( 'title', 'title 1' )
        ret = view.changeWidgetOptions( 0, 0, 0,
                                        ['title',], retJson=False )
        
        self.assert_( ret['success'] == True )
        self.assert_( widgets[0]['options'] == {'title':'title 1'} )
        self.assert_( widgets[1]['options'] == {'title': 'Un-titled widget'} )
    
    def test_collapseWidget( self ):
        self._registerWidgets()
        
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        # add 2 widgets in first column
        widgets = dashboard._layoutCfg[0]['columns'][0]['widgets']
        view.addWidget( 'widget1', 0, 0 )
        view.addWidget( 'widget2', 0, 0 )
        
        self.assert_( widgets[0]['collapse'] == 0 )
        self.assert_( widgets[1]['collapse'] == 0 )
        
        ret = view.collapseWidget( 0, 0, 0, 1, retJson=False )
        self.assert_( ret['success'] == True )
        self.assert_( widgets[0]['collapse'] == 1 )
        self.assert_( widgets[1]['collapse'] == 0 )
    
    def test_moveWidget( self ):
        self._registerWidgets()
        
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        pageCfg = dashboard._layoutCfg[0]
        widgets1 = pageCfg['columns'][0]['widgets']
        widgets2 = pageCfg['columns'][1]['widgets']
        
        # add 2 widgets to column 0
        view.addWidget( 'widget1', 0, 0 )
        view.addWidget( 'widget2', 0, 0 )
        self.assert_( len(widgets1) == 2 )
        self.assert_( len(widgets2) == 0 )
        
        # move 0,0,0 to 0,1,0
        view.moveWidget( 0, 0, 0, 0, 1, 0 )
        self.assert_( len(widgets1) == 1 )
        self.assert_( len(widgets2) == 1 )
        
        # move 0,0,0 to 0,1,0
        view.moveWidget( 0, 0, 0, 0, 1, 0 )
        self.assert_( len(widgets1) == 0 )
        self.assert_( len(widgets2) == 2 )
        
        # add another page
        view.addPage( retJson=False )
        pageCfg2 = dashboard._layoutCfg[1]
        widgets3 = pageCfg2['columns'][0]['widgets']
        widgets4 = pageCfg2['columns'][1]['widgets']
        
        # move 0,1,0 to 1,0,0
        view.moveWidget( 0, 1, 0, 1, 0, 0 )
        self.assert_( len(widgets2) == 1 )
        self.assert_( len(widgets3) == 1 )
        
        # move 0,1,0 to 1,0,0
        view.moveWidget( 0, 1, 0, 1, 0, 0 )
        self.assert_( len(widgets2) == 0 )
        self.assert_( len(widgets3) == 2 )

    def test_delWidget( self ):
        self._registerWidgets()
        
        dashboard = self.folder.dashboard1
        view = dashboard.restrictedTraverse( '@@dashboardEdit', None )
        
        pageCfg = dashboard._layoutCfg[0]
        widgets1 = pageCfg['columns'][0]['widgets']
        
        # add 2 widgets to column 0
        view.addWidget( 'widget1', 0, 0 )
        view.addWidget( 'widget2', 0, 0 )
        self.assert_( len(widgets1) == 2 )
        
        view.delWidget( 0, 0, 0 )
        self.assert_( len(widgets1) == 1 )
        
        view.delWidget( 0, 0, 0 )
        self.assert_( len(widgets1) == 0 )
    
    def _registerWidgets( self ):
        widgets = self.portal.portal_actions.dashboard_widgets
        
        # create actions
        # dashboard_widgets
        #  |_ widget1
        #  |_ widget2
        #  |_ widget3
        #  |_ widget4
        #  ...
        widget1 = self._makeAction( 'widget1',
                                    title='widget 1',
                                    description='widget 1 desc',
                                    url_expr='string:widget1::jsMethod::none',
                                    available_expr='python:True',
                                    permissions=('View',),
                                    visible=True
                                    )
        widgets._setObject( 'widget1', widget1 )
        
        widget2 = self._makeAction( 'widget2',
                                    title='widget 2',
                                    description='widget 2 desc',
                                    url_expr='string:widget2::jsMethod::none',
                                    available_expr='python:False',
                                    permissions=('View',),
                                    visible=True
                                    )
        widgets._setObject( 'widget2', widget2 )
        
        widget3 = self._makeAction( 'widget3',
                                    title='widget 3',
                                    description='widget 3 desc',
                                    url_expr='string:widget3::jsMethod::none',
                                    available_expr='python:True',
                                    permissions=('View',),
                                    visible=False
                                    )
        widgets._setObject( 'widget3', widget3 )
        
        widget4 = self._makeAction( 'widget4',
                                    title='widget 4',
                                    description='widget 4 desc',
                                    url_expr='string:widget4::jsMethod::none',
                                    available_expr='python:True',
                                    permissions=('Manage portal',),
                                    visible=True
                                    )
        widgets._setObject( 'widget4', widget4 )
    
    def _makeAction( self, *args, **kw ):
        return Action( *args, **kw )
    
class TestDashboardCreateView( AnzDashBoardTestCase ):

    def afterSetUp( self ):
        self.folder.invokeFactory( type_name='Document',
                                   id='doc1', title='doc 1' )
        self.folder.doc1.indexObject()
        
        self.folder.invokeFactory( type_name='News Item',
                                   id='news1', title='news 1' )
        self.folder.news1.indexObject()
        
        self.folder.invokeFactory( type_name='Folder',
                                   id='folder1', title='folder 1' )
        self.folder.folder1.indexObject()
    
    def test_viewApplied( self ):
        view = self.folder.doc1.restrictedTraverse( '@@dashboardCreate', None )
        self.assert_( view is None )
        
        view = self.folder.news1.restrictedTraverse( '@@dashboardCreate', None )
        self.assert_( view is None )
        
        view = self.folder.folder1.restrictedTraverse( '@@dashboardCreate', None )
        self.assert_( view is not None )
        
        self.setRoles( ['Manager',] )
        view = self.portal.restrictedTraverse( '@@dashboardCreate', None )
        self.assert_( view is not None )
    
    def test_normalCreate( self ):
        self.folder.invokeFactory( type_name='Anz Dashboard',
                                   id='dashboard1', title='dashboard 1' )
        self.assert_( 'dashboard1' in self.folder.objectIds() )
    
    def test_create( self ):
        view = self.folder.restrictedTraverse( '@@dashboardCreate', None )
        self.assert_( view is not None )
        ret = view.create( title='dashboard 1', layout='tab', retJson=False )
        objs = self.folder.objectValues( spec=['Anz Dashboard',] )
        self.assertEqual( len(objs), 1 )
        
        dashboard = objs[0]
        self.assertEqual( 'dashboard 1', dashboard.Title() )
        self.assertEqual( 'tab', dashboard.getLayout() )
    
    def _registerWidgets( self ):
        widgets = self.portal.portal_actions.dashboard_widgets
        
        # create actions
        # dashboard_widgets
        #  |_ widget1
        #  |_ widget2
        #  |_ widget3
        #  |_ widget4
        #  ...
        widget1 = self._makeAction( 'widget1',
                                    title='widget 1',
                                    description='widget 1 desc',
                                    url_expr='string:widget1::jsMethod::none',
                                    available_expr='python:True',
                                    permissions=('View',),
                                    visible=True
                                    )
        widgets._setObject( 'widget1', widget1 )
        
        widget2 = self._makeAction( 'widget2',
                                    title='widget 2',
                                    description='widget 2 desc',
                                    url_expr='string:widget2::jsMethod::none',
                                    available_expr='python:False',
                                    permissions=('View',),
                                    visible=True
                                    )
        widgets._setObject( 'widget2', widget2 )
        
        widget3 = self._makeAction( 'widget3',
                                    title='widget 3',
                                    description='widget 3 desc',
                                    url_expr='string:widget3::jsMethod::none',
                                    available_expr='python:True',
                                    permissions=('View',),
                                    visible=False
                                    )
        widgets._setObject( 'widget3', widget3 )
        
        widget4 = self._makeAction( 'widget4',
                                    title='widget 4',
                                    description='widget 4 desc',
                                    url_expr='string:widget4::jsMethod::none',
                                    available_expr='python:True',
                                    permissions=('Manage portal',),
                                    visible=True
                                    )
        widgets._setObject( 'widget4', widget4 )
    
    def _makeAction( self, *args, **kw ):
        return Action( *args, **kw )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestDashboardView) )
    suite.addTest( makeSuite(TestDashboardEditView) )
    suite.addTest( makeSuite(TestDashboardCreateView) )
    return suite

if  __name__ == '__main__':
    framework()
