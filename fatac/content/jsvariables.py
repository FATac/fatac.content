from zope.i18n import translate
from zope.publisher.browser import BrowserView

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from five import grok
from Products.CMFPlone.interfaces import IPloneSiteRoot


TEMPLATE = """\
if (!window._FATAC) {window._FATAC = {}; }
_FATAC.authenticatedUser = '%(authenticatedUser)s';
"""

FORM_MODIFIED = _(u'text_form_modified_message',
    default=u'Your form has not been saved. All changes you have made will be lost.')

FORM_RESUBMIT = _(u'text_form_resubmit_message',
    default=u'You already clicked the submit button. Do you really want to submit this form again?')

AJAX_NORESPONSE = _(u'text_ajax_noresponse_message',
    default=u'No response from server. Please try again later.')

CLOSE_BOX_MESSAGE = _(u'text_ajax_close_box_message',
    default=u'Close this box.')


class JSVariables(grok.View):

    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('fatac_globals.js')

    def render(self):
        context = self.context
        response = self.request.response

        response.setHeader('content-type', 'text/javascript;;charset=utf-8')

        props = getToolByName(context, 'portal_properties').site_properties
        portal_url = getToolByName(context, 'portal_url')()
        pm = getToolByName(context, "portal_membership")
        authenticatedUser = pm.getAuthenticatedMember().getId()

        # the following are flags for mark_special_links.js
        # links get the target="_blank" attribute
        # open_links = props.getProperty('external_links_open_new_window', 'false')
        # mark_links = props.getProperty('mark_special_links', 'false')

        # form_modified = translate(FORM_MODIFIED, context=self.request)
        # form_resubmit = translate(FORM_RESUBMIT, context=self.request)
        # ajax_noresponse = translate(AJAX_NORESPONSE, context=self.request)
        # close_box_message = translate(CLOSE_BOX_MESSAGE, context=self.request)

        # # escape_for_js
        # form_modified = form_modified.replace("'", "\\'")
        # form_resubmit = form_resubmit.replace("'", "\\'")
        # ajax_noresponse = ajax_noresponse.replace("'", "\\'")
        # close_box_message = close_box_message.replace("'", "\\'")

        return TEMPLATE % dict(
            authenticatedUser=authenticatedUser,
        )
