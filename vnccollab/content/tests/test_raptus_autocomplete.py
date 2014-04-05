import simplejson
from vnccollab.content.tests.base import FunctionalTestCase
from vnccollab.content.testing import createObject
from vnccollab.content.events import turnOffLocalRolesInheritance
from vnccollab.content.form.raptus_autocomplete import KeywordsAutocompleteSearch, KeywordsAutocompletePopulate


class TestRaptusAutocompleteView(FunctionalTestCase):
    def setUp(self):
        super(TestRaptusAutocompleteView, self).setUp()
        folder_1 = createObject(
            self.portal, 'Folder', 'test_folder_1', title='Folder 1',
            description='Some Folder 1 description - itsfolder',
            text='Some Folder 1 text', subject="Foo bar")
        self.folder_1 = folder_1

        document_1_folder_1 = createObject(
            folder_1, 'Document', 'test_doc_1_folder_1', title='A title doc 1 - testing very long title - longtitle',
            description='Some description of document 1 - itsdocument',
            text='Some text of document 1 from folder 1', subject="Foo rab 2")

        document_2_folder_1 = createObject(
            folder_1, 'Document', 'test_doc_2_folder_1', title='A title doc 2',
            description='Some description of document 2 - itsdocument',
            text='Some text of document 2 from folder 1', subject="Foo 3")

    def test_KeywordsAutocompleteSearch(self):
        self.app.REQUEST['f'] = 'subject'
        self.app.REQUEST['term'] = 'Fo'
        view = KeywordsAutocompleteSearch(self.folder_1, self.app.REQUEST)
        result = simplejson.loads(view())

        self.assertTrue(len(result) == 3)

        self.app.REQUEST['f'] = 'subject'
        self.app.REQUEST['term'] = 'Foo b'
        view = KeywordsAutocompleteSearch(self.folder_1, self.app.REQUEST)
        result = simplejson.loads(view())
        self.assertTrue(len(result) == 1)
        self.assertEqual(result[0], "Foo bar")

    def test_KeywordsAutocompletePopulate(self):
        self.app.REQUEST['f'] = 'subject'
        self.app.REQUEST['q'] = 'Foo'
        view = KeywordsAutocompletePopulate(self.folder_1, self.app.REQUEST)
        result = view()
        self.assertEqual(result, None)


        self.app.REQUEST['f'] = 'subject'
        self.app.REQUEST['q'] = 'Foo bar'
        view = KeywordsAutocompletePopulate(self.folder_1, self.app.REQUEST)
        result = view()
        self.assertTrue(result, 'Foo bar')
