# python
import re
import time
import cjson

# zope
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getUtility, queryUtility
from Acquisition import aq_parent, aq_inner, aq_base
from DateTime import DateTime
from zope.schema.interfaces import IVocabularyFactory
from zope.i18n import translate

# cmf
from Products.CMFCore.utils import getToolByName

# plone
from plone.memoize.interfaces import ICacheChooser

# products
from anz.dashboard.interfaces import IFolderContentsWidgetView
from anz.dashboard import MSG_FACTORY as _

class FolderContentsWidgetView( BrowserView ):
    ''' Folder contents widget functions interface. '''

    implements( IFolderContentsWidgetView )

    def getChildNodesData( self, path, query={}, retJsonFormat=True ):
        ''' See interfaces.IFolderContentsWidgetView. '''
        # convert from record to normal dict
        query = dict( query )

        query['path'] = { 'query': path, 'depth': 1 }
        query['is_folderish'] = True
        catalog = getToolByName( self.context, 'portal_catalog' )
        records = catalog.searchResults( query )
        ret = []

        for r in records:
            info = {}
            info['id'] = r.getId
            info['text'] = unicode( r.Title, 'utf-8' )
            info['url'] = r.getURL()

            path = ''
            if hasattr( r, 'getPath' ):
                path = r.getPath()
            else:
                path = '/'.join( r.getPhysicalPath() )
            info['path'] = path
            
            ret.append( info )

        if retJsonFormat:
            ret = cjson.encode( ret )

        return ret

    def items( self, paths=[], searchSub=False, portal_types=[], recentDays=0,
               sort_limit=0, sort_order='desc', sort_on='modified',
               cachetime=300, retJson=True ):
        ''' See interfaces.IFolderContentsWidgetView. '''
        context = self.context
        ret = {}

        try:
            query = {}

            # process paths list to format like: (('foo/bar',-1), ('bar/baz',-1))
            pathParam = []
            for p in paths:
                # filter blank path
                if p:
                    pathParam.append( (p,-1) )

            query['path'] = {
                'query': pathParam,
                'depth': searchSub and -1 or 1
            }

            # portal_type
            if portal_types:
                # convert 'Folder,Event' to list ['Folder','Event']
                if isinstance( portal_types, basestring ):
                    portal_types = portal_types.split( ',' )

                query['portal_type'] = portal_types

            # date
            if recentDays != 0:
                today = DateTime().earliestTime()
                endDate = today - recentDays
                query['modified'] = { 'query': endDate, 'range': 'min' }

            if sort_limit and sort_limit>0:
                query['sort_limit'] = sort_limit

            query['sort_order'] = sort_order
            query['sort_on'] = sort_on

            catalog = getToolByName( context, 'portal_catalog' )
            records = catalog.searchResults( query )

            # data process
            items = self._getBrainsInfo( records )

            ret['success'] = True
            ret['msg'] = translate( _(u'Get folder contents success.'),
                                    context=self.request )
            ret['items'] = items
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)

        return retJson and cjson.encode(ret) or ret

    def types( self, retJson=True ):
        ''' See interfaces.IFolderContentsWidgetView. '''
        ret = {}
        try:
            name = 'plone.app.vocabularies.ReallyUserFriendlyTypes'
            util = queryUtility( IVocabularyFactory, name )
            ret['success'] = True
            ret['msg'] = _(u'Get portal types success.')
            ret['types'] = [ {'id':t.value,'name':t.title} \
                             for t in util(self.context) ]
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)

        return retJson and cjson.encode(ret) or ret

    def _getBrainsInfo( self, items=[] ):
        # Convert list of catalog brain itmes to list of items' information.
        ret = []
        if items:
            mt = getToolByName( self.context, 'portal_membership' )
            for item in items:
                item_info = {}
                item_info['id'] = item.getId
                item_info['title'] = unicode( item.Title or item.getId, 'utf-8' )
                item_info['url'] = item.getURL()
                item_info['path'] = item.getPath()
                item_info['desc'] = item.Description
                item_info['modified'] = item.modified.strftime('%Y/%m/%d %H:%M:%S')

                # get user name by id
                userId = item.Creator
                userName = userId
                memberInfo = mt.getMemberInfo( userId )
                if memberInfo:
                    userName = memberInfo['fullname'] or memberInfo['username']
                    if not userName:
                        userName = userId

                item_info['author_id'] = userId
                item_info['author'] = unicode( userName, 'utf-8' )
                item_info['size'] = item.getObjSize
                item_info['icon'] = item.getIcon
                #item_info['review_state'] = item.review_state

                ret.append( item_info )

        return ret
