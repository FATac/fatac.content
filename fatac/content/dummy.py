from zope import schema
from plone.directives import form
from five import grok
from fatac.content import PlaylistMessageFactory as _
import json
from fatac.theme.browser.genericView import genericView
from Products.CMFCore.utils import getToolByName
import time
from AccessControl import getSecurityManager
from Products.CMFCore import permissions


class IDummy(form.Schema):
    """ Dummy Schema
    """

    tagList = schema.List(
        title=_(u"Tag List"),
        description=_(u"This is a list of tags that have this image"),
        default=[],
        value_type=schema.TextLine(),
        required=False,
        )


class View(grok.View, genericView):
    """ Main View
    """
    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('view')
    #grok.template("dummy_view")

    def __init__(self, context, request):
        super(grok.View, self).__init__(context, request)
        super(genericView, self).__init__(context, request)

    def jsonFixer(self, sections):
        result = {}
        for section in sections:
            result[section.get('nom')] = {key: section.get(key) for key in section.keys() if key != 'nom'}

        return result

    def sectionFontType(self, sectionName):
        if sectionName == 'header':
            return 'georgia13c333333'
        elif sectionName == 'content':
            return 'georgia11c666666'
        else:
            return 'arial13c666666'


class loadTags(grok.View):
    """ Metode que retorna els tags
    """
    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('loadTags')

    def render(self):
        request = self.request
        context = self.context

        request.response.setHeader("content-type", "application/json")

        if (len(context.tagList) > 0):
            tags = []
            for tag in context.tagList:
                tags.append(json.loads(tag))

            return json.dumps(tags)
        else:
            return json.dumps({"info": "No tags to load."})


class saveTag(grok.View):
    """ Metode que guarda els Tags
    """

    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('saveTag')

    def render(self):
        context = self.context
        request = self.request
        request.response.setHeader("content-type", "application/json")

        pm = getToolByName(context, "portal_membership")
        member = pm.getAuthenticatedMember().getId()

        tag = request.form
        tag['user'] = self.retNomCreator()
        tag['date'] = time.strftime("(%d/%m/%Y)", time.localtime())
        tag['id'] = str(time.time())
        tag['member'] = member

        tag_list = context.tagList
        tag_list.append(json.dumps(tag))
        context.tagList = tag_list

        return json.dumps({"info": self.context.translate("comentari_afegit",domain="fatac.theme"), "user": tag['user'], "member": tag['member'], "date": tag['date'], "id": tag['id']})

    def retNomCreator(self):
        """ retorna el Full name de l'usuari que ha creat la playlist.
        Copiada de fatac.content.playlists.py
        """
        pm = getToolByName(self.context, "portal_membership")
        member = pm.getAuthenticatedMember()
        fullname = member.getProperty('fullname')
        if not fullname:
            fullname = member.getUserName()
        return fullname


class deleteTag(grok.View):
    """ Metode que elimina el Tag
    """

    grok.context(IDummy)
    grok.require('zope2.View')
    grok.name('deleteTag')

    def render(self):
        context = self.context
        request = self.request
        request.response.setHeader("content-type", "application/json")

        tag_to_delete = request.form.get("id")

        pm = getToolByName(context, "portal_membership")
        member = pm.getAuthenticatedMember().getId()

        userIsManager = getSecurityManager().checkPermission(permissions.ManagePortal, context)

        for tag in context.tagList:
            if str(json.loads(tag).get("id")) == tag_to_delete:
                # Check if current user is allowed to delete this tag or user is Manager
                if json.loads(tag).get("member") == member or userIsManager:
                    context.tagList.remove(tag)
                    context._p_changed = 1
                    # return json.dumps({"info": "Comentari %s esborrat" % tag_to_delete})
                    return json.dumps({"info": self.context.translate("comentari_esborrat",domain="fatac.theme")})
                else:
                    # return json.dumps({"info": "No tens permissos per esborrar el comentari %s" % tag_to_delete})
                    return json.dumps({"info": self.context.translate("comentari_no_esborrat", domain="fatac.theme")})
