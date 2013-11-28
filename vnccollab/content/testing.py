from plone.testing import z2

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

import collective.customizablePersonalizeForm


class VnccollabContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        dependencies = [
            'raptus.autocompletewidget',
            'collective.customizablePersonalizeForm',
            'vnccollab.content',
        ]

        for package in dependencies:
            module = __import__(package, fromlist=[''])
            self.loadZCML(package=module)

        self.loadZCML(package=collective.customizablePersonalizeForm,
                name='overrides.zcml')

        z2.installProduct(app, 'collective.customizablePersonalizeForm')
        z2.installProduct(app, 'vnccollab.content')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.customizablePersonalizeForm:default')
        applyProfile(portal, 'vnccollab.content:default')


VNCCOLLAB_CONTENT_FIXTURE = VnccollabContentLayer()
VNCCOLLAB_CONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(VNCCOLLAB_CONTENT_FIXTURE,),
    name='VnccollabContentLayer:Integration')
VNCCOLLAB_CONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(VNCCOLLAB_CONTENT_FIXTURE,),
    name='VnccollabContentLayer:Functional')
