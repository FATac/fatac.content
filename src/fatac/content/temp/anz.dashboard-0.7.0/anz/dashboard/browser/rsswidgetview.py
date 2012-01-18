# python
import time
import socket
import cjson
import feedparser

# zope
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getUtility
from Acquisition import aq_parent, aq_inner, aq_base
from zope.i18n import translate

# cmf
from Products.CMFCore.utils import getToolByName

# plone
from plone.memoize.interfaces import ICacheChooser

# products
from anz.dashboard.interfaces import IRssWidgetView
from anz.dashboard import MSG_FACTORY as _

class RssWidgetView( BrowserView ):
    ''' Provide RSS widget functions. '''
    
    implements( IRssWidgetView )
    
    def entries( self, url, cachetime=900, retJson=True ):
        ''' Return fetched rss entries.
        
        @param url
        url of the rss feed
        
        @param cachetime
        time to keep the result in cache( in second, default is 900 )
        
        @retJson
        format return value to json format or not( default True )
        
        @return status of create process
        json data:
        {
            success: True,
            msg: 'Fetch rss entries success.',
            entries: [...]
        }
        
        '''
        ret = {}
        
        try:
            items = []
            
            feed = self._fetchFeed( url, cachetime )
            if feed.has_key( 'bozo_exception' ):
                ret['success'] = False
                ret['msg'] = str( feed['bozo_exception'] )
            else:
                toLocalizedTime = self.context.restrictedTraverse('@@plone').\
                                toLocalizedTime
                for entry in feed.entries:
                    item = {}
                    item['title'] = entry.title
                    item['link'] = entry.link
                    item['summary'] = entry.summary
                    item['updated'] = toLocalizedTime( entry.updated,
                                                       long_format=1 )
                    items.append( item )
                
                ret['success'] = True
                ret['msg'] = translate( _(u'Fetch RSS entries success.'),
                                        context=self.request )
                ret['entries'] = items
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def _fetchFeed( self, url, cachetime=900 ):
        now = time.time()
        
        chooser = getUtility( ICacheChooser )
        cache = chooser( 'anz.dashboard.widget_rss.feedcache' )
        
        cached_data = cache.get( url, None )
        if cached_data is not None:
            ( timestamp, feed ) = cached_data
            if now-timestamp < cachetime:
                return feed
            
            socket.setdefaulttimeout( 5 )
            newfeed = feedparser.parse( url,
                                        etag=getattr(feed,'etag',None),
                                        modified=getattr(feed,'modified',None) )
            if newfeed.status == 304:
                cache[url] = ( now+cachetime, feed )
                return feed
        
        socket.setdefaulttimeout( 5 )
        feed = feedparser.parse( url )
        cache[url] = ( now+cachetime, feed )
        
        return feed
