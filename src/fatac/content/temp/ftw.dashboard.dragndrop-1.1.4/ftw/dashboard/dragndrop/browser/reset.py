from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import queryUtility
from plone.app.portlets.storage import UserPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.portlets.constants import USER_CATEGORY

class ResetView(BrowserView):

    def __call__(self,  *args, **kwargs):
        user = self.context.portal_membership.getAuthenticatedMember()
        numbers = self.context.portal_properties.get('ftw.dashboard').getProperty('columnNumber', 4)
        for number in range(numbers):
            name = "plone.dashboard"+ str(number+1);
            column = queryUtility(IPortletManager, name=name)
            if column is not None:
                category = column.get(USER_CATEGORY, None)
                if category is not None:
                    manager = category.get(user.getId(), None)
                    if manager is None:
                        manager = category[user.getId()] = UserPortletAssignmentMapping(manager=name,
                                                                                        category=USER_CATEGORY,
                                                                                        name=user.getId())
                        if manager is None:
                            IStatusMessage(self.request).addStatusMessage("can't reset the Dashboard", type="error")
                            break
                    for portlet in manager.keys():
                        del manager[portlet]

        IStatusMessage(self.request).addStatusMessage("Dashboard reseted", type="info")                    
        return self.request.RESPONSE.redirect(self.context.portal_url() + '/dashboard')
