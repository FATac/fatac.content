# zope
from zope.interface import Interface

#
# merged request view
#
class IMergedRequestView( Interface ):
    ''' Return multi-categories data in one request to improve performance. '''

    def getMergedData( requests=[], retJson=True ):
        ''' Execute multi-requests' in one request.

        @param requests
        a list contains requested view and method info, format like:
        [ 'requestName@@viewName/methodName?queryString',... ]

        note:
        queryString fit the valid http query string format:
        field1=value1&field2=value2&field3=value3...

        @param retJson
        format returned value to json format or not ( default True ) 

        @return a dict contains multi-requests' data or its json format
        {
        'request1': {
            'success': True,
            'msg': 'Get request1 information success.'
            'title': 'title',
            'description': 'desc',
            ...
            },
        'request2': {
            'success': True,
            'msg': 'Get request2 information success.'
            'tags': 'tag1,tag2,...',
            ...
            },
        }

        '''

#
# message catalog view
#
class IMessageCatalogView( Interface ):
    ''' Provide functions to return message catalog. '''

    def catalogMapping( domain, retJson=True ):
        ''' Return message catalog as a mapping.

        @param domain
        domain of the message catalog

        @param retJson
        format return value to json format or not( default True )

        @return
        a dict with the following format:
        {
            'success': True,
            'msg': 'Get message catalog mapping success.',
            'mapping': {
                u'text1': u'translated text1',
                u'text2': u'translated text2',
                ...
            }
        }

        '''

class IWidgetView( Interface ):
    ''' Widget query view. '''

    def getWidgets( check_visibility=True,
                    check_permissions=True,
                    check_condition=True,
                    retJson=True
                    ):
        ''' Return a sequence of registered widgets' information.

        @param check_visibility
        if True, return only actions whose "visible" flag is set.

        @param check_permissions
        if True, return only actions for whose permissions the current user is
        authorized.

        @param check_condition
        if True, return only actions whose condition expression evaluates True.

        @param retJson
        format return value to json format or not

        @return
        a dict with widgets' information, format like:
        {
            'success': True,
            'msg': 'Get widgets success.',
            'widgets': [{
                'id': '',
                'title': '',
                'desc': '',
                'icon': ''
                },
                ...
                ]
        }
        '''

    def getWidget( id,
                   check_visibility=True,
                   check_permissions=True,
                   check_condition=True,
                   retJson=True
                   ):
        ''' Return the specific widget's information.

        @param id
        id of the wanted widget

        @param check_visibility
        if True, return only action whose "visible" flag is set.

        @param check_permissions
        if True, return only action for whose permissions the current user is
        authorized.

        @param check_condition
        if True, return only action whose condition expression evaluates True.

        @param retJson
        format return value to json format or not( default True )

        @return
        a dict with the following format:
        {
            'success': True,
            'msg': 'Get widget success.',
            'id': '',
            'title': '',
            'description': '',
            'icon': ''
        }

        '''

#
# dashboard
#
class IDashboard( Interface ):
    ''' marker interface. '''

class IDashboardView( Interface ):
    ''' marker interface. '''

    def getPageLayout( retJson=True ):
        ''' Return page layout.

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains page layout, format like:
        {
            'success': True,
            'msg': 'Get page layout success.'
            'layout': 'tile'
        }

        '''

    def getPageConfig( pageIndex, retJson=True ):
        ''' Return layout config of specific page.

        @param pageIndex
        index of the page

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains page layout config, format like:
        {
            'success': True,
            'msg': 'Get page config success.'
            'config': {...}
        }

        '''

    def getLayoutConfig( retJson=True ):
        ''' Return layout configure of current object.

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains layout config, format like:
        {
            'success': True,
            'msg': 'Get layout config success.',
            'config': [{'style': '',
                'title': 'page title',
                'width': '100%',
                'columns': [{'style': '',
                    'width': '21%',
                    'portlets': [{'id': 'portlet_weather',
                        'options': {...}},
                        {'id': 'portlet_hot_contents',
                        'options': {}},
                        ...
                        ]
                      },
                      ...
                      ]
                      },
                      ...
                      ]
        }

        '''

class IDashboardEditView( Interface ):
    ''' Dashboard edit functions interface. '''

    def addPage( pageIndex=-1, retJson=True ):
        ''' Add a new page to dashboard at position pageIndex.
        The page has two columns as default, if pageIndex is -1 then add the
        page at the end of the dashboard.

        @param pageIndex
        index of the page( default is -1, append to the end)

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Add page success.'
            'pageIndex': new page index (from 0)
        }

        '''

    def editPage( pageIndex, title='Untitled page', width=100,
                  style='', retJson=True ):
        ''' Edit page layout config.

        @param pageIndex
        index of the page to be edit

        @param title
        title of the page( default is 'Untitled page' )

        @param width
        width of the page in percentage( default is 100 )

        @param style
        style of the page( default is '' )

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Edit page success.'
        }

        '''

    def movePage( pageIndex, toPage, retJson=True ):
        ''' Move a page from pageIndex to toIndex.

        @param pageIndex
        index of the page be moved

        @param toPage
        index of the page moved to

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Move page success.'
        }

        '''

    def delPage( pageIndex, retJson=True ):
        ''' Delete specific page.
        Note: If there is only one page left, can not delete the page.

        @param pageIndex
        index of the page to be deleted

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Delete page success.'
        }

        '''

    def addColumn( pageIndex=0, columnIndex=-1, retJson=True ):
        ''' Add a new column.

        @param pageIndex
        index of the page( default is 0, first page )

        @param columnIndex
        index of the column( default is -1, append to the end )

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Add column success.'
            'columnIndex': new column index(from 0)
        }

        '''

    def changeColumnsWidth( pageIndex, widths=[], retJson=True ):
        ''' Change width of the columns.

        @param pageIndex
        index of the page

        @param widths
        list of column width( width in percentage with string format )

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Change columns width success.'
        }

        '''

    def moveColumn( pageIndex, columnIndex, toColumn, retJson=True ):
        ''' Move a widget to specific position.

        @param pageIndex
        index of page the column lies on( start from 0 )

        @param columnIndex
        index of column( start from 0 )

        @param toColumn
        index of new column

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Move column success.'
        }

        '''

    def delColumn( pageIndex, columnIndex, retJson=True ):
        ''' Delete specific column.

        @param pageIndex
        index of the page the column belongs to

        @param columnIndex
        index of the column to be deleted

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Delete column success.'
        }

        '''

    def addWidget( widgetId, pageIndex, columnIndex,
                   widgetIndex=0, retJson=True ):
        ''' Add a widget to a specific position.

        @param widgetId
        id of widget

        @param pageIndex
        index of page the widget lies on( start from 0 )

        @param columnIndex
        index of column the widget lies on( start from 0 )

        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Add widget success.'
        }

        '''

    def changeWidgetColor( pageIndex, columnIndex, widgetIndex,
                           color, retJson=True ):
        ''' change color of widget.

        @param pageIndex
        index of page the widget lies on( start from 0 )

        @param columnIndex
        index of column the widget lies on( start from 0 )

        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )

        @param color
        widget color

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Change widget color success.'
        }

        '''

    def changeWidgetOptions( pageIndex, columnIndex, widgetIndex,
                             names=[], retJson=True, **kw ):
        ''' Change options of widget.

        @param pageIndex
        index of page the widget lies on( start from 0 )

        @param columnIndex
        index of column the widget lies on( start from 0 )

        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )

        @param names
        list contains widget options name

        @param retJson
        format return value to json format or not( default True )

        @param **kw
        widget options( default is request )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Change widget options success.',
            'options': {...}
        }

        '''

    def collapseWidget( pageIndex, columnIndex, widgetIndex,
                        collapse, retJson=True ):
        ''' Collapse or expand specific widget.

        @param pageIndex
        index of page the widget lies on( start from 0 )

        @param columnIndex
        index of column the widget lies on( start from 0 )

        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )

        @param collapse
        widget collapse status, True means collapse, False means expand

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Change widget collapse state success.'
        }

        '''

    def moveWidget( pageIndex, columnIndex, widgetIndex,
                    toPage, toColumn, toWidget, retJson=True ):
        ''' Move a widget to specific position.

        @param pageIndex
        index of page the widget lies on( start from 0 )

        @param columnIndex
        index of column the widget lies on( start from 0 )

        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )

        @param toPage
        index of new page

        @param toColumn
        index of new column

        @param toWidget
        index of new widget position

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Move widget success.'
        }

        '''

    def delWidget( pageIndex, columnIndex, widgetIndex, retJson=True ):
        ''' Delete specific widget from current dashboard.

        @param pageIndex
        index of page the widget lies on( start from 0 )

        @param columnIndex
        index of column the widget lies on( start from 0 )

        @param widgetIndex
        index of the widget, count from top to bottom( start from 0 )

        @retJson
        format return value to json format or not( default True )

        @return
        a dict contains state of process, format like:
        {
            'success': True,
            'msg': 'Delete widget success.'
        }

        '''

class IDashboardCreateView( Interface ):
    ''' Provide 'Anz Dashboard' type create functions. '''

    def create( title='Untitled object', layout='tile', retJson=True ):
        ''' Create 'Anz Dashboard' instance

        @param title
        title of the new instance( default 'Untitled object' )

        @param layout
        layout of dashboard pages, one of 'tab' and 'tile'( default 'tile' )

        @retJson
        format return value to json format or not( default True )

        @return status of create process
        json data:
        {
            success: True,
            msg: 'Create "Anz Dashboard" instance success.',
            id: 'id1',
            title: 'title',
            url: 'url',
            path: 'path'
        }

        '''

#
# widgets
#
class IRssWidgetView( Interface ):
    ''' RSS widget functions interface. '''

    def entries( url, cachetime=900, retJson=True ):
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

class IWeatherWidgetView( Interface ):
    ''' Weather widget functions interface. '''

    def weather( woeid, units='c', cachetime=3600, retJson=True ):
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

class ICalendarWidgetView( Interface ):
    ''' Calendar widget functions interface. '''

    def getReviewStateString( retJson=True ):
        ''' Return event review state query string.

        @retJson
        format return value to json format or not( default True )

        @return a dict contains review state string:
        {
            success: True,
            msg: 'Get review state string success.',
            stateStr: '...'
        }

        '''

    def events( start, end, cachetime=300, retJson=True ):
        ''' Return events involved in specific date range( [start,end) ).

        involved means event's time range overlapped with specific date range,
        greater and equal the start date and less then the end date.

        @param start
        start date of the time range( DateTime object or its string format )

        @param end
        end date of the time range( DateTime object or its string format )

        @retJson
        format return value to json format or not( default True )

        @return status of create process
        json data:
        {
            success: True,
            msg: 'Get events success.',
            events: {
                '20100201': [{
                    'title': 'event title',
                    'desc': 'event desc',
                    'start': 'start date',
                    'end': 'end date',
                    'url': 'event url',
                    'location': 'event location'
                },...],
                '20100202': [...],
                ...
                '20100207': [...]
            }
        }

        '''

class IFolderContentsWidgetView( Interface ):
    ''' Folder contents widget functions interface. '''

    def getChildNodesData( path, query={}, retJsonFormat=True ):
        ''' Return first level sub-objects under specific object,
        specify by path.

        @param path
        path of the folder which sub-objects's data will be returned 

        @param query
        more query conditions to customize your search ( default {} )

        @param retJsonFormat
        format return value to json format or not { default True }

        @return
        searched items' info, usually used by js, format like:
        [{
        	id: 1,
        	text: 'A leaf Node',
        	leaf: true
        },{
        	id: 2,
        	text: 'A folder Node',
        	leaf: false
        }]

        '''

    def items( paths=[], searchSub=False, portal_types=[], recentDays=0,
               sort_limit=0, sort_order='desc', sort_on='modified',
               cachetime=300, retJson=True ):
        ''' Return searched content items.

        @param paths
        paths to search items in it

        @param searchSub
        search all sub-objects or not( default is False )

        @param portal_types
        portal types to search, [] means all( default is [] )

        @param recentDays
        only return recent n days modified objects.
        0 means no time limit( default is 0 ),
        1 means recent 1 day( from begin of today )
        2 means recent 2 day( from begin of yesterday )
        ...

        @param sort_limit
        max returned objects number, 0 means no limit( default is 0 )

        @param sort_order
        sort order of returned objects( default is desc )

        @param sort_on
        sort on( default is modified date )

        @param cachetime
        time to keep the result in cache( in second, default is 300 )

        @retJson
        format return value to json format or not( default True )

        @return status of create process
        json data:
        {
            success: True,
            msg: 'Get folder contents success.',
            items: [...]
        }

        '''

    def types( retJson=True ):
        ''' Return friendly searchable portal types.

        @retJson
        format return value to json format or not( default True )

        @return status of create process
        json data:
        {
            success: True,
            msg: 'Get portal types success.',
            types: [{
                'id': 'type1',
                'name': 'type1 name'
            },{
                'id': 'type2',
                'name': 'type2 name'
            }]
        }

        '''
