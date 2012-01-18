# python
import os, sys
from time import sleep

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestRssWidgetView( AnzDashBoardTestCase ):

    def afterSetUp( self ):
        self.folder.invokeFactory( type_name='Document',
                                   id='doc1', title='doc 1' )
        self.folder.doc1.indexObject()
        
        self.folder.invokeFactory( type_name='Anz Dashboard',
                                   id='dashboard1', title='dashboard 1' )
        self.folder.dashboard1.indexObject()
    
    def test_viewApplied( self ):
        view = self.folder.doc1.restrictedTraverse( '@@rssWidget', None )
        self.assert_( view is None )
        
        view = self.folder.dashboard1.restrictedTraverse( '@@rssWidget', None )
        self.assert_( view is not None )
    
    def test_entries( self ):
        view = self.folder.dashboard1.restrictedTraverse( '@@rssWidget', None )
        
        # fine url
        ret = view.entries( 'http://www.spiegel.de/schlagzeilen/tops/index.rss',
                            cachetime=1, retJson=False )
        self.assert_( ret['success'] == True )
        
        ret = view.entries( 'http://www.spiegel.de/schlagzeilen/tops/index.rss',
                            cachetime=1, retJson=False )
        self.assert_( ret['success'] == True )
        
        sleep( 3 )
        
        ret = view.entries( 'http://www.spiegel.de/schlagzeilen/tops/index.rss',
                            cachetime=1, retJson=False )
        self.assert_( ret['success'] == True )
        
        # wrong url
        ret = view.entries( 'http://wrong url', retJson=False )
        self.assert_( ret['success'] == False )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestRssWidgetView) )
    return suite

if  __name__ == '__main__':
    framework()
