# -*- coding: utf-8 -*-
from zope import schema

from plone.directives import form

from plone.app.textfield import RichText
from fatac.content import PlaylistMessageFactory as _

from five import grok
from plone.directives.dexterity import DisplayForm
from Products.CMFCore.utils import getToolByName


class InotaLlibre(form.Schema):
    """ Nota Pagina Llibre Schema
    """

    text = RichText(
        title=_(u"Text"),
        description=_(u"The displayed text"),
        required=False,
    )


class View(DisplayForm):
    grok.context(InotaLlibre)
    grok.require('cmf.ManagePortal')

    def getLlibre(self):  
        nota = self.context
        pagina = nota.__parent__
        llibre = pagina.__parent__
        id_llibre = llibre.id
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        llibre = portal.portal_catalog.searchResults(portal_type="fatac.dummy", path='/fatac/ac/'+id_llibre)   
        url_llibre = llibre[0].getURL() 
        return url_llibre + '/gestionarLlibre'