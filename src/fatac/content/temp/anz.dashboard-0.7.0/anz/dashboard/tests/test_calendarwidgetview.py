# python
import os, sys

# zope
from DateTime import DateTime

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from anz.dashboard.tests.base import AnzDashBoardTestCase

class TestCalendarWidgetView( AnzDashBoardTestCase ):

    def afterSetUp( self ):
        self.wf = self.portal.portal_workflow
        
        self.folder.invokeFactory( type_name='Document',
                                   id='doc1', title='doc 1' )
        self.folder.doc1.indexObject()
        
        self.folder.invokeFactory( type_name='Anz Dashboard',
                                   id='dashboard1', title='dashboard 1' )
        self.folder.dashboard1.indexObject()
    
    def test_viewApplied( self ):
        view = self.folder.doc1.restrictedTraverse( '@@calendarWidget', None )
        self.assert_( view is None )
        
        view = self.folder.dashboard1.restrictedTraverse( '@@calendarWidget',
                                                          None )
        self.assert_( view is not None )
    
    def test_getReviewStateString( self ):
        view = self.folder.dashboard1.restrictedTraverse( '@@calendarWidget', None )
        
        # default workflow states that will show in the calendar is 'published'
        result = 'review_state=published&amp;'
        self.assertEqual( result,
                          view.getReviewStateString(False)['stateStr'] )
        
        # change to 'visible,published'
        self.portal.portal_calendar.calendar_states = ('visible','published')
        result = 'review_state=visible&amp;review_state=published&amp;'
        self.assertEqual( result,
                          view.getReviewStateString(False)['stateStr'] )
    
    def test_events( self ):
        self.setRoles( ['Manager'] )
        
        # add 2 normal events
        self._addEvent( '1', DateTime('2010/02/01 10:00:00'),
                        DateTime('2010/02/01 12:00:00') )
        self._addEvent( '2', DateTime('2010/02/02 11:00:00'),
                        DateTime('2010/02/02 12:00:00') )
        
        # add 3 cross-days events
        self._addEvent( '3', DateTime('2010/01/28 10:00:00'),
                        DateTime('2010/02/04 12:00:00') )
        self._addEvent( '4', DateTime('2010/02/02 10:00:00'),
                        DateTime('2010/02/05 12:00:00') )
        self._addEvent( '5', DateTime('2010/02/05 10:00:00'),
                        DateTime('2010/02/15 12:00:00') )
        
        view = self.folder.dashboard1.restrictedTraverse( '@@calendarWidget',
                                                          None )
        
        # get events in a week
        start = '2010/02/01 10:00:00'
        end = '2010/02/07 10:00:00'
        ret = view.events( start, end, retJson=False )
        self.assertEqual( ret['success'], True )
        self.assertEqual( len(ret['events'].keys()), 7 )
        
        events = ret['events']
        
        # 20100201
        self.assertEqual( len(events['20100201']), 2 )
        
        # 20100202
        self.assertEqual( len(events['20100202']), 3 )
        
        # 20100203
        self.assertEqual( len(events['20100203']), 2 )
        
        # 20100204
        self.assertEqual( len(events['20100204']), 2 )
        
        # 20100205
        self.assertEqual( len(events['20100205']), 2 )
        
        # 20100206
        self.assertEqual( len(events['20100206']), 1 )
        
        # 20100207
        self.assertEqual( len(events['20100207']), 1 )
        
        # test excerption
        start = 'wrong start date'
        end = DateTime('2010/02/07 10:00:00')
        ret = view.events( start, end, retJson=False )
        self.assertEqual( ret['success'], False )
        self.assert_( ret['msg'] != None )
    
    def _addEvent( self, id, start, end ):
        self.folder.invokeFactory( type_name='Event',
                                   id=id,
                                   title='event %s'%id,
                                   startDate=start,
                                   endDate=end )
        event = getattr( self.folder, id )
        event.indexObject()
        
        # publish
        self.wf.doActionFor( event, 'publish' )

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest( makeSuite(TestCalendarWidgetView) )
    return suite

if  __name__ == '__main__':
    framework()
