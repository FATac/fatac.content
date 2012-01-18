# python
import time
import socket
import pprint
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
from anz.dashboard.interfaces import IWeatherWidgetView
from anz.dashboard import MSG_FACTORY as _

# hack feedparser to support yahoo weather rss format
_FeedParserMixin = feedparser._FeedParserMixin
_FeedParserMixin.namespaces['http://xml.weather.yahoo.com/ns/rss/1.0'] = \
                'yweather'

# use this method to avoid python closure tricky
def makeFunc( e ):
    def func( self, attrs ):
        context = self._getContext()
        elName = 'yweather_%s' % e
        context.setdefault( elName, [] )
        context[elName].append( attrs )
    
    return func

elements = [ 'location', 'units', 'wind', 'atmosphere', 'astronomy', \
             'condition', 'forecast' ]
for e in elements:
    funcName = '_start_yweather_%s' % e
    setattr( _FeedParserMixin, funcName, makeFunc(e) )

class WeatherWidgetView( BrowserView ):
    ''' Provide Weather information. '''
    
    implements( IWeatherWidgetView )
    
    endPoint = 'http://weather.yahooapis.com/forecastrss'
    appId = '1dIus9DV34GjOFTpNt_pwV465FOtJItUDeDMDR2bLWox6hTqUHPrVtvCnvDBfYg-'
    
    def weather( self, woeid, units='c', cachetime=3600, retJson=True ):
        ''' Return weather info of specific city from weather.yahooapis.com.
        
        @param woeid
        where on earth identifiers of the city( get from yahoo geoplanet )
        
        @param units
        units for temperature, f for Fahrenheit and c for Celsius( default c )
        
        @param cachetime
        time to keep the result in cache( in second, default is 3600 )
        
        @retJson
        format return value to json format or not( default True )
        
        @return status of create process
        json data:
        {
            success: True,
            msg: 'Get weather info success.',
            info: {
                title: '',
                link: '',
                updated: '',
                codition: {'code': u'34',
                           'date': u'Fri, 29 Jan 2010 1:30 pm CST',
                           'temp': u'6',
                           'text': u'Fair'},
                forecast: [{'code': u'32',
                            'date': u'29 Jan 2010',
                            'day': u'Fri',
                            'high': u'4',
                            'low': u'-7',
                            'text': u'Sunny'},
                           {'code': u'32',
                            'date': u'30 Jan 2010',
                            'day': u'Sat',
                            'high': u'6',
                            'low': u'-7',
                            'text': u'Sunny'}]}],
                astronomy: {'sunrise': u'7:25 am',
                            'sunset': u'5:28 pm'},
                atmosphere: {'humidity': u'9',
                             'pressure': u'1015.92',
                             'rising': u'2',
                             'visibility': u'9.99'},
                location: {'city': u'Beijing',
                           'country': u'China',
                           'region': u''},
                units: {'distance': u'km',
                        'pressure': u'mb',
                        'speed': u'km/h',
                        'temperature': u'C'},
                wind: {'chill': u'2',
                       'direction': u'300',
                       'speed': u'20.92'}
            }
        }
        
        '''
        ret = {}
        
        try:
            items = []
            
            feed = self._fetchFeed( woeid, units, cachetime )
            if feed.has_key( 'bozo_exception' ):
                ret['success'] = False
                ret['msg'] = str( feed['bozo_exception'] )
            else:
                toLocalizedTime = self.context.restrictedTraverse('@@plone').\
                                toLocalizedTime
                
                if feed.feed.subtitle != 'Yahoo! Weather Error':
                    info = {
                        'astronomy': feed.feed.yweather_astronomy[0],
                        'atmosphere': feed.feed.yweather_atmosphere[0],
                        'location': feed.feed.yweather_location[0],
                        'units': feed.feed.yweather_units[0],
                        'wind': feed.feed.yweather_wind[0]
                    }
                    
                    if len(feed.entries):
                        entry = feed.entries[0]
                        info['title'] = entry.title
                        info['link'] = entry.link
                        info['updated'] = toLocalizedTime( entry.updated,
                                                           long_format=1 )
                        info['condition'] = entry.yweather_condition[0]
                        info['forecast'] = entry.yweather_forecast
                    
                    ret['success'] = True
                    ret['msg'] = translate( _(u'Get weather info success.'),
                                            context=self.request )
                    ret['info'] = info
                else:
                    ret['success'] = False
                    ret['msg'] = feed.entries[0].title
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)
        
        return retJson and cjson.encode(ret) or ret
    
    def _fetchFeed( self, woeid, units, cachetime=3600 ):
        now = time.time()
        url = self.endPoint + '?w=' + woeid + '&u=' + units
        
        chooser = getUtility( ICacheChooser )
        cache = chooser( 'anz.dashboard.weather_rss.feedcache' )
        
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
