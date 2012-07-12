from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from five import grok
import base64

"""
    * retornaUserRoles *

    Servei que retorna els rols donat un nom d'usuari en codificacio base64
"""


class IRetornaUserRoles(Interface):
    """
        Interficie de IRetornaUserRoles que retorna els rols donat un usuari
    """


class retornaUserRoles(grok.View):
    """
        Vista que retorna els rols d'un usuari
    """

    grok.context(IPloneSiteRoot)
    grok.require('zope2.View')
    grok.name('retornaUserRoles')

    def render(self):
        """
            Render, retornem la llista de rols separat per comes
        """
        context = self.context
        request = self.request

        userIdBase64 = request.get('uid')
        self.userId = ""
        self.roles = []

        if userIdBase64 != "":
            try:
                self.userId = base64.b64decode(userIdBase64)
            except:
                self.userId = ""

            mtool = getToolByName(context, 'portal_membership')

            # Retorna els grups de l'usuari
            member = mtool.getMemberById(self.userId)

            if member == None:
                return 'no_such_user'
            else:
                mRoles = member.getRoles()
                for role in mRoles:
                    self.roles.append(role)

        return ','.join(self.roles)
