###########
# Metodes que s'executen a l'instalar el producte
###########

"""
	Alerta!! Plone conte un bug a l'hora de declarar importSteps!! (configure.zcml)
    Es pot comprovar l'error aqui: https://dev.plone.org/ticket/8350
    No afecta al correcte funcionament del producte ni del Plone, simplement
    dona un "Warning" en el Log. (GenericSetup There are unresolved or circular dependencies.)
"""

from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.security import ISecuritySchema
from plone.registry.interfaces import IRegistry



def setupSiteSecurity(portal):
    """
        site security setup!
    """
    secSchema = ISecuritySchema(portal)

    # Activa el poder crear carpetes d'usuari al fer login un usuari
    if secSchema.get_enable_user_folders() == False:
        secSchema.set_enable_user_folders(True)
        print "fatac.content >> enabled user folder creation"

    # Afegim propietat en els grups per controlar qui es el creador / Administradors
    gd_tool = getToolByName(portal, 'portal_groupdata')
    if not hasattr(gd_tool, 'delegated_group_member_managers'):
        gd_tool._setProperty('delegated_group_member_managers', (), 'lines')
        print "fatac.content >> add group member managers property to portal_groupdata"

    # Si no esta creada la carpeta de grups la creem
    if "Groups" not in portal.objectIds():
        portal.invokeFactory(id="Groups", type_name="Folder")
        print "fatac.content >> Groups folder added"


def setupVarious(context):
    portal = context.getSite()
    setupSiteSecurity(portal)