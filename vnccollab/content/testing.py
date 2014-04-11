import transaction

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


def setObjDate(obj, dt):
    """Prevent update of modification date
       during reindexing"""
    obj.setCreationDate(dt)
    obj.setEffectiveDate(dt)
    obj.setModificationDate(dt)
    od = obj.__dict__
    od['notifyModified'] = lambda *args: None
    obj.reindexObject()
    del od['notifyModified']


def createObject(context, _type, id, delete_first=True, check_for_first=False,
                 object_date=None, **kwargs):
    result = None
    if delete_first and id in context.objectIds():
        context.manage_delObjects([id])
    if not check_for_first or id not in context.objectIds():
        result = context[context.invokeFactory(_type, id, **kwargs)]
    else:
        result = context[id]

    if object_date:
        setObjDate(result, object_date)

    transaction.commit()
    return result