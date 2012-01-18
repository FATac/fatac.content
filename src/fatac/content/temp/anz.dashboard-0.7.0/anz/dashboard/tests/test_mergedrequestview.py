# python
import os, sys

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestMergedRequestView( AnzDashBoardTestCase ):

    def test_viewRetrieve( self ):
        view = self.folder.restrictedTraverse( '@@mergedRequest', None )
        self.assert_( view is not None )
    
    def test_getMergedData( self ):
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
        
        view = self.folder.restrictedTraverse( '@@mergedRequest', None )
        
        requests = ['widgets@@widgetView/getWidgets',
                    'i18n@@msgCatalog/catalogMapping?domain=anz.dashboard']
        ret = view.getMergedData( requests=requests, retJson=False )
        self.assertEqual( ret['i18n']['success'], True )
        self.assertEqual( ret['widgets']['success'], True )
        
        # wrong view name
        requests = ['wrong@@wrongView/dummy',
                    'i18n@@msgCatalog/catalogMapping?domain=anz.dashboard']
        ret = view.getMergedData( requests=requests, retJson=False )
        self.assertEqual( ret['i18n']['success'], True )
        self.assertEqual( ret['wrong']['success'], False )
        
        # wrong method name
        requests = ['widgets@@widgetView/wrongMethod',
                    'i18n@@msgCatalog/catalogMapping?domain=anz.dashboard']
        ret = view.getMergedData( requests=requests, retJson=False )
        self.assertEqual( ret['i18n']['success'], True )
        self.assertEqual( ret['widgets']['success'], False )
        
        # test query string contains 'type converters'
        requests = ['widgets@@widgetView/getWidgets',
                    'i18n@@msgCatalog/catalogMapping?domain:list=anz.dashboard']
        ret = view.getMergedData( requests=requests, retJson=False )
        self.assertEqual( ret['i18n']['success'], True )
        self.assertEqual( ret['widgets']['success'], True )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestMergedRequestView) )
    return suite


if  __name__ == '__main__':
    framework()
