# python
import re
import types
import cjson

# zope
from Products.Five import BrowserView
from zope.interface import implements
from Acquisition import aq_base, aq_parent, aq_inner

# cmf
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.utils import _checkPermission

# products
from anz.dashboard import MSG_FACTORY as _
from anz.dashboard.interfaces import IMergedRequestView

class MergedRequestView( BrowserView ):
    ''' Return multi-categories data in one request to improve performance. '''
    
    implements( IMergedRequestView )
    
    def getMergedData( self, requests=[], retJson=True ):
        ''' Execute multi-requests' in one request.
        
        @param requests
        a list contains requested view and method info, format like:
        [ 'requestId@@viewName/methodName?queryString',... ]
        
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
        context = self.context
        ret = {}
        
        pat = re.compile( r'([a-zA-Z_]\w*)@@([a-zA-Z_]\w*)/([a-zA-Z_]\w*)\??([a-zA-Z_].*)*' )
        for r in requests:
            result = pat.match( r )
            if result:
                id, viewName, methodName, queryStr = result.groups()
                success = True
                msg = ''
                data = {}
                
                view = context.restrictedTraverse( viewName, None )
                if view is not None:
                    params = {}
                    if queryStr:
                        pairs = queryStr.split( '&' )
                        for p in pairs:
                            k, v = p.split( '=' )
                            
                            # trip 'type converters'
                            if k.find(':') != -1:
                                k = k.split(':')[0]
                            
                            params[k] = v
                    
                    # todo
                    # support zope converter
                    
                    method = getattr( view, methodName, None )
                    if method and callable( method ):
                        data = method( **params )
                    else:
                        success = False
                        msg = _('No method %s found.' % methodName)
                else:
                    success = False
                    msg = _('Fail to get view %s' % viewName)
                
                if not isinstance( data, types.DictType ):
                    data = cjson.decode( data )
                
                ret[id] = { 'success': success, 'msg': msg }
                ret[id].update( data )
        
        return retJson and cjson.encode(ret) or ret
