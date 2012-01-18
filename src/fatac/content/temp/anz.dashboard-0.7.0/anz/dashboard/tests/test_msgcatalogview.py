# python
import os
import sys

# products
from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestMsgCatalogView( AnzDashBoardTestCase ):

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
    
    def test_viewRetrieve( self ):
        view = self.folder.restrictedTraverse( '@@msgCatalog', None )
        self.assert_( view is not None )
        
        view = self.folder.doc1.restrictedTraverse( '@@msgCatalog', None )
        self.assert_( view is not None )
        
        view = self.folder.news1.restrictedTraverse( '@@msgCatalog', None )
        self.assert_( view is not None )
        
        view = self.folder.folder1.restrictedTraverse( '@@msgCatalog', None )
        self.assert_( view is not None )
    
    def test_catalogMapping( self ):
        view = self.folder.restrictedTraverse( '@@msgCatalog', None )
        ret = view.catalogMapping( 'anz.dashboard', retJson=False )
        self.assert_( ret['success'] )
        self.assert_( len(ret['texts'].keys()) > 1 )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestMsgCatalogView) )
    return suite
