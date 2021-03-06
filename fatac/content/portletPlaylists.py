from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.portlets.portlets import base
from zope.interface import implements
from zope.formlib import form
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from Products.CMFCore.utils import getToolByName

class IPlaylistsPortlet(IPortletDataProvider):
    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)


class Assignment(base.Assignment):
    implements(IPlaylistsPortlet)

    def __init__(self, count=5):
        self.count = count

    @property
    def title(self):
        return _(u"Playlists items")


class AddForm(base.AddForm):
    form_fields = form.Fields(IPlaylistsPortlet)
    label = _(u"Add Playlists Portlet")
    description = _(u"This portlet displays Playlists.")

    def create(self, data):
        return Assignment(count=data.get('count', 5))

class EditForm(base.EditForm):
    form_fields = form.Fields(IPlaylistsPortlet)
    label = _(u"Edit Playlists Portlet")
    description = _(u"This portlet displays Playlists.")

class Renderer(base.Renderer):
    _template = ViewPageTemplateFile('portlets/portletPlaylists.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()  # whether or not the current user is Anonymous
        self.portal_url = portal_state.portal_url()  # the URL of the portal object

        # a list of portal types considered "end user" types
        self.typesToShow = portal_state.friendly_types()

        plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.catalog = plone_tools.catalog()

    def render(self):
        return self._template()

    @property
    def available(self):
        """Show the portlet only if there are one or more elements."""
        return not self.anonymous and len(self._data())

    def recent_items(self):
        return self._data()

    def recently_modified_link(self):
        return '%s/recently_modified' % self.portal_url

    @memoize
    def _data(self):
        limit = self.data.count

        #Get the current member
        mt = getToolByName(self.context, 'portal_membership')
        if not mt.isAnonymousUser(): # the user has not logged in
            member = mt.getAuthenticatedMember()
            username = member.getUserName()

        return self.catalog(portal_type='fatac.playlist',
                            Creator=username,
                            sort_on='modified',
                            sort_order='reverse',
                            sort_limit=limit)[:limit]

    def playlists(self):
        for brain in self._data():
            playlist = brain.getObject()

            yield dict(title=playlist.Title(),
                       summary=playlist.Description(),
                       url=brain.getURL())


