from Products.CMFCore.utils import getToolByName
from five import grok
from Products.CMFPlone.interfaces import IPloneSiteRoot
from AccessControl import getSecurityManager
from Products.CMFCore import permissions
from Products.Five.browser import BrowserView


class fatacUtils(BrowserView):
    """Helper view for fatac"""

    def shouldRenderContentViews(self):

        if not getSecurityManager().checkPermission(permissions.ModifyPortalContent, object):
            pass
