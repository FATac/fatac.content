from zope import schema
from plone.directives import form
from five import grok
from fatac.content import PlaylistMessageFactory as _
import json
from Products.CMFCore.utils import getToolByName
import time
from AccessControl import getSecurityManager
from Products.CMFCore import permissions

from plone.namedfile.field import NamedImage

from plone.directives.dexterity import DisplayForm

class IpaginaLlibre(form.Schema):
    """ Pagina Llibre Schema
    """   

    pagina = NamedImage(
        title=_(u"Pagina"),
        description=_(u"Please upload an image"),
        required=True,
    )

class View(DisplayForm):
    grok.context(IpaginaLlibre)
    grok.require('cmf.ManagePortal')

    def getLlibre(self):     
        pagina = self.context
        llibre = pagina.__parent__
        id_llibre = llibre.id
        portal = getToolByName(self.context, 'portal_url').getPortalObject()
        llibre = portal.portal_catalog.searchResults(portal_type="fatac.dummy", path='/fatac/ac/'+id_llibre)   
        url_llibre = llibre[0].getURL() 
        return url_llibre + '/gestionarLlibre'