from vnccollab.content.tests.base import FunctionalTestCase
from vnccollab.content.testing import createObject
from vnccollab.content.events import turnOffLocalRolesInheritance


class TestEventsView(FunctionalTestCase):
    members = (
        ('secret', 'Scott Tiger', 'scott@tiger.com', ['members'], '2013-09-24'),
        ('secret', 'Johann Sebastian Bach', 'johan@bach.com', ['members'], '2013-09-24'),)

    def test_turnOffLocalRolesInheritance(self):
        folder_1 = createObject(
            self.portal, 'Folder', 'test_folder_1', title='Folder 1',
            description='Some Folder 1 description - itsfolder',
            text='Some Folder 1 text')

        browser = self.login()
        browser.open(folder_1.absolute_url_path())
        self.assertFalse(hasattr(folder_1, '__ac_local_roles_block__'))
        turnOffLocalRolesInheritance(folder_1, None)
        self.assertTrue(hasattr(folder_1, '__ac_local_roles_block__'))
