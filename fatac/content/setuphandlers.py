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
from fatac.core.utils import crearObjecte
import logging


def setupSiteSecurity(portal):
    """
        site security setup!
    """
    logger = logging.getLogger("fatac.content")
    secSchema = ISecuritySchema(portal)

    # Activa el poder crear carpetes d'usuari al fer login un usuari
    if secSchema.get_enable_user_folders() == False:
        secSchema.set_enable_user_folders(True)
        logger.info("fatac.content >> enabled user folder creation")

    # Afegim propietat en els grups per controlar qui es el creador / Administradors
    gd_tool = getToolByName(portal, 'portal_groupdata')
    if not hasattr(gd_tool, 'delegated_group_member_managers'):
        gd_tool._setProperty('delegated_group_member_managers', (), 'lines')
        logger.info("fatac.content >> add group member managers property to portal_groupdata")

    # Si no esta creada la carpeta de grups la creem
    if "Groups" not in portal.objectIds():
        crearObjecte(portal, "Groups", "Folder", 'Groups', 'Carpeta contenidora de les carpetes de grup')
        logger.info("fatac.content >> Groups folder added")

    gtool = getToolByName(portal, 'portal_groups')
    if 'Reviewers' in gtool.listGroupNames():
        gtool.removeGroup("Reviewers")
        logger.info("fatac.content >> Removed 'Reviewers' group")


def setupVarious(context):
    portal = context.getSite()
    setupSiteSecurity(portal)
