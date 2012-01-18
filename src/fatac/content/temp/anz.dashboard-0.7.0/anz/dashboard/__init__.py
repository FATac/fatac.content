# zope
from zope.i18nmessageid import MessageFactory

# cmf
from Products.CMFCore import utils
from Products.CMFCore.permissions import AddPortalContent

# archetypes
from Products.Archetypes.public import process_types, listTypes

# product
from anz.dashboard.config import PROJECTNAME

MSG_FACTORY = MessageFactory( 'anz.dashboard' )

from anz.dashboard.dashboard import Dashboard

def initialize( context ):
    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)
    
    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types      = content_types,
        permission         = AddPortalContent,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)
