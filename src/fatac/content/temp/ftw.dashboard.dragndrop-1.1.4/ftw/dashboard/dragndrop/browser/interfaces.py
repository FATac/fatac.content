from zope.interface import Interface

from plone.theme.interfaces import IDefaultPloneLayer

class IDashboard(Interface):
    """ marker interface"""

class IDashboardViewable(Interface):
    """ marker interface"""

class IDashboardEditViewable(IDashboardViewable):
    """ marker interface"""