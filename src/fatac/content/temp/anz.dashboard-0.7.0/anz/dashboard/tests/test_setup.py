# python
import os, sys

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestProductInstall( AnzDashBoardTestCase ):

    def test_skinLayersInstalled( self ):
        subIds = self.portal.portal_skins.objectIds()
        ids = [ 'anz_dashboard', 'anz_dashboard_resources' ]
        for id in ids:
            self.assert_( id in subIds )
    
    def test_typesInstalled( self ):
        subIds = self.portal.portal_types.objectIds()
        ids = [ 'Anz Dashboard' ]
        for id in ids:
            self.assert_( id in subIds )
    
    def test_modifyToDefaultPage( self ):
        properties = self.folder.portal_properties.site_properties
        self.assert_( 'Anz Dashboard' in properties.getProperty('default_page') )
    
    def test_ActionCategoryInstalled( self ):
        # dashboard_widgets
        subIds = self.portal.portal_actions.objectIds()
        
        self.assert_( 'dashboard_widgets' in subIds )
        dashboard_widgets = self.portal.portal_actions.dashboard_widgets
        self.assertEqual( dashboard_widgets.meta_type, 'CMF Action Category' )

    def test_i18nSetup( self ):
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
        
        view = self.folder.restrictedTraverse( '@@msgCatalog', None )
        ret = view.catalogMapping( 'anz.dashboard', retJson=False )
        self.assert_( ret['success'] )
        self.assert_( len(ret['texts'].keys()) > 1 )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestProductInstall) )
    return suite

if  __name__ == '__main__':
    framework()