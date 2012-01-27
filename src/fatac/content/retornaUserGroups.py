from Products.CMFCore.utils import getToolByName
from zope.interface import Interface
from five import grok
import base64

"""
    * retornaUserGroups *

    Servei que retorna els grups donat un nom d'usuari en codificacio base64
"""


class IRetornaUserGroup(Interface):
    """
        Interficie de IRetornaUserGroup que retorna el grup donat un usuari
    """


class retornaUserGroups(grok.View):
    """
        Vista que retorna els grups d'un usuari
    """

    grok.context(IRetornaUserGroup)
    grok.require('zope2.View')
    grok.name('retornaUserGroups')

    def update(self):
        context = self.context
        request = self.request

        userIdBase64 = request.get('uid')
        self.userId = ""
        self.groups = []

        if userIdBase64 != "":
            try:
                self.userId = base64.b64decode(userIdBase64)
            except:
                self.userId = ""

            gtool = getToolByName(context, 'portal_groups')

            # Retorna els grups de l'usuari
            groupObjects = gtool.getGroupsByUserId(self.userId)

            for group in groupObjects:
                self.groups.append(group.getId())



    def render(self):
        """
            Render, retornem la llista de grups separat per comes
        """

        groupsString = ""
        for group in self.groups:
            if groupsString == "":
                groupsString = group
            else:
                groupsString = groupsString + ',' + group
        return groupsString