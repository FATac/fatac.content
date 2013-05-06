# -*- coding: utf-8 -*-
from zope import schema

from plone.directives import form

from plone.namedfile.field import NamedImage
from fatac.content import PlaylistMessageFactory as _

from five import grok
from plone.directives.dexterity import DisplayForm
from Products.CMFCore.utils import getToolByName



class IdetallLlibre(form.Schema):
    """ Detall Pagina Llibre Schema
    """

    title = schema.TextLine(
        title = _(u'Title'),
        required = False,
        )
        
    description = schema.Text(
        title=_(u'Description'),
        description = _(u'help_description'),
        required = False,
        missing_value = u'',
        )   

    form.primary('picture') 
    picture = NamedImage(
        title=_(u"Picture"),
        description=_(u"Please upload an image"),
        required=True,
    )

class View(DisplayForm):
    grok.context(IdetallLlibre)
    grok.require('cmf.ManagePortal')

    def getLlibre(self):  
        detall = self.context
        pagina = detall.__parent__
        llibre = pagina.__parent__
        id_llibre = llibre.id
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        llibre = portal.portal_catalog.searchResults(portal_type="fatac.dummy", path='/fatac/ac/'+id_llibre)   
        url_llibre = llibre[0].getURL() 
        return url_llibre + '/gestionarLlibre'


# class Edit(DisplayForm):
#     grok.context(IdetallLlibre)
#     grok.require('cmf.ManagePortal')

#     def getLlibre(self):  
#         detall = self.context
#         pagina = detall.__parent__
#         llibre = pagina.__parent__
#         id_llibre = llibre.id
#         portal = getToolByName(self.context, 'portal_url').getPortalObject()
#         llibre = portal.portal_catalog.searchResults(portal_type="fatac.dummy", path='/fatac/ac/'+id_llibre)   
#         url_llibre = llibre[0].getURL() 
#         return url_llibre + '/gestionarLlibre'