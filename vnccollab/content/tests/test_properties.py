#from plone import api
#from plone.app.testing import setRoles
#from plone.app.testing import TEST_USER_ID

from zope.component import getMultiAdapter

from vnccollab.content.tests.base import IntegrationTestCase
from vnccollab.content.testing import VNCCOLLAB_CONTENT_INTEGRATION_TESTING


class TestProperties(IntegrationTestCase):
    layer = VNCCOLLAB_CONTENT_INTEGRATION_TESTING

    def personalPrefs(self):
        return getMultiAdapter((self.portal, self.portal.REQUEST),
                               name='personal-information')

    def test_new_properties_exists(self):
        user_properties = self.personalPrefs().form_fields.\
            __dict__['__FormFields_byname__'].keys()
        self.failUnless('telephone' in user_properties)
        self.failUnless('position' in user_properties)
