from zope.component import adapts, queryMultiAdapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.manager import DashboardPortletManagerRenderer
from plone.app.portlets.interfaces import IDashboard
from zope.interface import implements
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.layout.navigation.interfaces import INavigationRoot

class FtwDashboardPortletManagerRenderer(DashboardPortletManagerRenderer):
    """Render a column of the dashboard
    """
    
    adapts(INavigationRoot, IDefaultBrowserLayer, IBrowserView, IDashboard)
    template = ViewPageTemplateFile('templates/dashboard-column.pt')
    
    def isEditable(self, portlet):
        
        if queryMultiAdapter((portlet, self.request), name='edit', default=None):
            return True
        else:
            return False