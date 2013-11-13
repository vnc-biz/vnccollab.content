from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from zope.configuration import xmlconfig


class AddonContent(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import raptus.autocompletewidget
        self.loadZCML(package=raptus.autocompletewidget)

        import vnccollab.content
        xmlconfig.file('configure.zcml',
                       vnccollab.content,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'vnccollab.content:default')


VNCCOLLAB_CONTENT_FIXTURE = AddonContent()
VNCCOLLAB_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VNCCOLLAB_CONTENT_FIXTURE,),
    name='AddonContent:Integration')
VNCCOLLAB_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VNCCOLLAB_CONTENT_FIXTURE,),
    name='VNCThemeContent:Functional')
