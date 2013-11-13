from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from vnccollab.content.tests.base import IntegrationTestCase
from vnccollab.content.testing import VNCCOLLAB_CONTENT_INTEGRATION_TESTING


class TestBasic(IntegrationTestCase):
    layer = VNCCOLLAB_CONTENT_INTEGRATION_TESTING

    def test_addon_is_installed(self):
        """ Validate that our products GS profile has been run and the product
            installed
        """
        pid = 'vnccollab.content'
        qi_tool = api.portal.get_tool(name='portal_quickinstaller')
        installed = [p['id'] for p in qi_tool.listInstalledProducts()]
        self.assertTrue(pid in installed,
                        'package appears not to have been installed')
