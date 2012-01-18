# python
import os, sys
from time import sleep

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestWeatherWidgetView( AnzDashBoardTestCase ):

    def afterSetUp( self ):
        self.folder.invokeFactory( type_name='Document',
                                   id='doc1', title='doc 1' )
        self.folder.doc1.indexObject()
        
        self.folder.invokeFactory( type_name='Anz Dashboard',
                                   id='dashboard1', title='dashboard 1' )
        self.folder.dashboard1.indexObject()
    
    def test_viewApplied( self ):
        view = self.folder.doc1.restrictedTraverse( '@@weatherWidget', None )
        self.assert_( view is None )
        
        view = self.folder.dashboard1.restrictedTraverse( '@@weatherWidget', None )
        self.assert_( view is not None )
    
    def test_weather( self ):
        view = self.folder.dashboard1.restrictedTraverse( '@@weatherWidget', None )
        
        # get weather data
        ret = view.weather( '2142703', 'c', cachetime=1, retJson=False )
        self.assertEqual( ret['success'], True )
        
        # get weather data again to test cache
        ret = view.weather( '2142703', 'c', cachetime=1, retJson=False )
        self.assertEqual( ret['success'], True )
        
        sleep( 3 )
        
        # test cache timeout
        ret = view.weather( '2142703', 'c', cachetime=1, retJson=False )
        self.assertEqual( ret['success'], True )
        
        # wrong city
        ret = view.weather( '00000', 'c', retJson=False )
        self.assertEqual( ret['success'], False )
        self.assertEqual( ret['msg'], 'City not found' )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestWeatherWidgetView) )
    return suite

if  __name__ == '__main__':
    framework()
