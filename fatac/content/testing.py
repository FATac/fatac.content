from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from zope.configuration import xmlconfig

class FatacContent(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import fatac.content
        xmlconfig.file('configure.zcml',
                       fatac.content,
                       context=configurationContext)


    def setUpPloneSite(self, portal):
        applyProfile(portal, 'fatac.content:default')

FATAC_CONTENT_FIXTURE = FatacContent()
FATAC_CONTENT_INTEGRATION_TESTING = \
    IntegrationTesting(bases=(FATAC_CONTENT_FIXTURE, ),
                       name="FatacContent:Integration")
