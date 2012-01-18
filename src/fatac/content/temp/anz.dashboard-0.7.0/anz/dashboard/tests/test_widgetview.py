# python
import os, sys

# zope
from zope.i18n import translate

# cmf
from Products.CMFCore.ActionInformation import ActionCategory, Action

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.dashboard import MSG_FACTORY as _
from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestWidgetView( AnzDashBoardTestCase ):

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
        
        # Setup site langauge settings
        ltool = self.portal.portal_languages
        defaultLanguage = 'zh-cn'
        supportedLanguages = ['en','zh-cn']
        ltool.manage_setLanguageSettings( defaultLanguage,
                                          supportedLanguages,
                                          setUseCombinedLanguageCodes=False )
        
        # THIS IS FOR UNIT TESTING ONLY
        # Normally called by pretraverse hook,
        # but must be called manually for the unit tests
        # Goes only for the current request
        ltool.setLanguageBindings()
    
    def test_viewApplied( self ):
        view = self.folder.doc1.restrictedTraverse( '@@widgetView', None )
        self.assert_( view is not None )
        
        view = self.folder.news1.restrictedTraverse( '@@widgetView', None )
        self.assert_( view is not None )
        
        view = self.folder.folder1.restrictedTraverse( '@@widgetView', None )
        self.assert_( view is not None )
    
    def test_getWidgets( self ):
        request = self.app.REQUEST
        self._registerWidgets()
        view = self.folder.doc1.restrictedTraverse( '@@widgetView', None )
        
        # no check
        data = [{
                'id': 'widget_static_text',
                'title': translate( _(u'Static text widget'), context=request ),
                'desc': translate( _(u'This widget is used to render static HTML contents.'),
                                   context=request ),
                'icon': ''
            },{
                'id': 'widget2',
                'title': 'widget 2',
                'desc': 'widget 2 desc',
                'icon': ''
            },{
                'id': 'widget3',
                'title': 'widget 3',
                'desc': 'widget 3 desc',
                'icon': ''
            },{
                'id': 'widget4',
                'title': 'widget 4',
                'desc': 'widget 4 desc',
                'icon': ''
            }]
        self.assertEqual( data, view.getWidgets( check_visibility=False,
                                                 check_permissions=False,
                                                 check_condition=False,
                                                 retJson=False
                                                 )['widgets'] )
        
        # check visibility
        data = [{
                'id': 'widget_static_text',
                'title': translate( _(u'Static text widget'), context=request ),
                'desc': translate( _(u'This widget is used to render static HTML contents.'),
                                   context=request ),
                'icon': ''
            },{
                'id': 'widget2',
                'title': 'widget 2',
                'desc': 'widget 2 desc',
                'icon': ''
            },{
                'id': 'widget4',
                'title': 'widget 4',
                'desc': 'widget 4 desc',
                'icon': ''
            }]
        self.assertEqual( data, view.getWidgets( check_visibility=True,
                                                 check_permissions=False,
                                                 check_condition=False,
                                                 retJson=False
                                                 )['widgets'] )
        
        # check permissions
        data = [{
                'id': 'widget_static_text',
                'title': translate( _(u'Static text widget'), context=request ),
                'desc': translate( _(u'This widget is used to render static HTML contents.'),
                                   context=request ),
                'icon': ''
            },{
                'id': 'widget2',
                'title': 'widget 2',
                'desc': 'widget 2 desc',
                'icon': ''
            },{
                'id': 'widget3',
                'title': 'widget 3',
                'desc': 'widget 3 desc',
                'icon': ''
            }]
        self.assertEqual( data, view.getWidgets( check_visibility=False,
                                                 check_permissions=True,
                                                 check_condition=False,
                                                 retJson=False
                                                 )['widgets'] )
        
        # check condition
        data = [{
                'id': 'widget_static_text',
                'title': translate( _(u'Static text widget'), context=request ),
                'desc': translate( _(u'This widget is used to render static HTML contents.'),
                                   context=request ),
                'icon': ''
            },{
                'id': 'widget3',
                'title': 'widget 3',
                'desc': 'widget 3 desc',
                'icon': ''
            },{
                'id': 'widget4',
                'title': 'widget 4',
                'desc': 'widget 4 desc',
                'icon': ''
            }]
        self.assertEqual( data, view.getWidgets( check_visibility=False,
                                                 check_permissions=False,
                                                 check_condition=True,
                                                 retJson=False
                                                 )['widgets'] )
    
    def test_getWidget( self ):
        request = self.app.REQUEST
        self._registerWidgets()
        view = self.folder.doc1.restrictedTraverse( '@@widgetView', None )
        
        # no check
        data = {
            'success': True,
            'msg': translate( _(u'Get widget success.'), context=request ),
            'id': 'widget_static_text',
            'title': translate( _(u'Static text widget'), context=request ),
            'desc': translate( _(u'This widget is used to render static HTML contents.'),
                               context=request ),
            'icon': ''
            }
        self.assertEqual( data, view.getWidget( 'widget_static_text',
                                                check_visibility=False,
                                                check_permissions=False,
                                                check_condition=False,
                                                retJson=False
                                                ) )
        
        # check visibility
        data = {
            'success': False,
            'msg': translate( _(u'No widget with id "${id}" found.'),
                              mapping={'id':'widget3'},
                              context=request )
            }
        self.assertEqual( data, view.getWidget( 'widget3',
                                                check_visibility=True,
                                                check_permissions=False,
                                                check_condition=False,
                                                retJson=False
                                                ) )
        
        data = {
            'success': True,
            'msg': translate( _(u'Get widget success.'), context=request ),
            'id': 'widget3',
            'title': 'widget 3',
            'desc': 'widget 3 desc',
            'icon': ''
            }
        self.assertEqual( data, view.getWidget( 'widget3',
                                                check_visibility=False,
                                                check_permissions=False,
                                                check_condition=False,
                                                retJson=False
                                                ) )
        
        # check permissions
        data = {
            'success': False,
            'msg': translate( _(u'No widget with id "${id}" found.'),
                              mapping={'id':'widget4'},
                              context=request )
            }
        self.assertEqual( data, view.getWidget( 'widget4',
                                                check_visibility=False,
                                                check_permissions=True,
                                                check_condition=False,
                                                retJson=False
                                                ) )
        
        data = {
            'success': True,
            'msg': translate( _(u'Get widget success.'), context=request ),
            'id': 'widget4',
            'title': 'widget 4',
            'desc': 'widget 4 desc',
            'icon': ''
            }
        self.assertEqual( data, view.getWidget( 'widget4',
                                                check_visibility=False,
                                                check_permissions=False,
                                                check_condition=False,
                                                retJson=False
                                                ) )
        
        # check condition
        data = {
            'success': False,
            'msg': translate( _(u'No widget with id "${id}" found.'),
                              mapping={'id':'widget2'},
                              context=request )
            }
        self.assertEqual( data, view.getWidget( 'widget2',
                                                check_visibility=False,
                                                check_permissions=False,
                                                check_condition=True,
                                                retJson=False
                                                ) )
        
        data = {
            'success': True,
            'msg': translate( _(u'Get widget success.'), context=request ),
            'id': 'widget2',
            'title': 'widget 2',
            'desc': 'widget 2 desc',
            'icon': ''
            }
        self.assertEqual( data, view.getWidget( 'widget2',
                                                check_visibility=False,
                                                check_permissions=False,
                                                check_condition=False,
                                                retJson=False
                                                ) )
        
        # get not existent widget
        wrongId = 'wrong_id'
        data = {
            'success': False,
            'msg': translate( _(u'No widget with id "${id}" found.'),
                              mapping={'id':wrongId},
                              context=request )
            }
        self.assertEqual( data, view.getWidget( wrongId,
                                                check_visibility=False,
                                                check_permissions=False,
                                                check_condition=False,
                                                retJson=False
                                                ) )
    
    def _registerWidgets( self ):
        widgets = self.portal.portal_actions.dashboard_widgets
        
        # clear anz.dashboard installed widgets
        ids = widgets.objectIds()
        for id in ids:
            widgets._delObject( id )
        
        # create actions
        # dashboard_widgets
        #  |_ widget1
        #  |_ widget2
        #  |_ widget3
        #  |_ widget4
        #  ...
        widget1 = self._makeAction( 'widget_static_text',
                                    title='Static text widget',
                                    description='This widget is used to render static HTML contents.',
                                    i18n_domain='anz.dashboard',
                                    available_expr='python:True',
                                    permissions=('View',),
                                    visible=True
                                    )
        widgets._setObject( 'widget_static_text', widget1 )
        
        widget2 = self._makeAction( 'widget2',
                                    title='widget 2',
                                    description='widget 2 desc',
                                    available_expr='python:False',
                                    permissions=('View',),
                                    visible=True
                                    )
        widgets._setObject( 'widget2', widget2 )
        
        widget3 = self._makeAction( 'widget3',
                                    title='widget 3',
                                    description='widget 3 desc',
                                    available_expr='python:True',
                                    permissions=('View',),
                                    visible=False
                                    )
        widgets._setObject( 'widget3', widget3 )
        
        widget4 = self._makeAction( 'widget4',
                                    title='widget 4',
                                    description='widget 4 desc',
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
    suite.addTest( makeSuite(TestWidgetView) )
    return suite

if  __name__ == '__main__':
    framework()
