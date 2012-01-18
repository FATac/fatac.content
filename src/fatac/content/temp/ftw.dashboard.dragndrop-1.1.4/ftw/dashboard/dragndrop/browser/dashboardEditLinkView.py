from Products.Five.browser import BrowserView
from zope.component import adapts, getMultiAdapter, queryMultiAdapter,getUtility
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from Products.CMFCore.utils import getToolByName

from plone.portlets.utils import unhashPortletInfo, hashPortletInfo

class DashboardEditLinkView(BrowserView):
    
    def __call__(self):
        
        
        hash = self.request.get("hash")
        portlet_info = unhashPortletInfo(hash)
        manager_name = portlet_info['manager']
        userid = portlet_info['key']
        name = portlet_info['name']
        referer = self.request.environ['HTTP_REFERER']
            
        baseUrl = '%s/++dashboard++%s+%s' % (self.context.portal_url(),manager_name,userid)
            
        url = '%s/%s/edit?referer=%s' % (baseUrl,name,referer)
        
        print(url)
        
        return self.request.RESPONSE.redirect(url)