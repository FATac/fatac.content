from Products.Five import BrowserView
from zope.component import getUtility

from plone.portlets.utils import unhashPortletInfo
from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import USER_CATEGORY

class RemovePortlet(BrowserView):

    def __call__(self, *args, **kwargs):
        hash = self.request.get('hash')
        portlet_info = unhashPortletInfo(hash)
        column, portlet = self.get_column_and_portlet(portlet_info)

        if portlet_info['name'] in column.keys():
            del column[portlet_info['name']]
        return ''

    def get_column_and_portlet(self, portlet_info):
        # get column
        column_manager = getUtility(IPortletManager, name=portlet_info['manager'])
        userid = self.context.portal_membership.getAuthenticatedMember().getId()
        column = column_manager.get(USER_CATEGORY, {}).get(userid, {})

        # get portlet
        portlet = column.get(portlet_info['name'])
        return column, portlet
 
