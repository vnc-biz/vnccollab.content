from plone import api
from Products.Five.browser import BrowserView

from vnccollab.content import messageFactory as _

AUTHOR_TABS_KEY = 'vncollab.content.author_tab_list'


class AuthorView(BrowserView):

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.uid = self.request.form.get('uid', '')

    def tabs_info(self):
        """Returns a string representing the dynamic tabs in author.cpt."""
        return self.get_tabs_info(self.uid)

    def get_tabs_info(self, uid):
        """Returns a list with info about the dynamic tabs for author.cpt.

        The list consist in a tuple of (title, url), obtained from the
        registry. The registry contains lines of the form:

            title::path

        The title is localized and the path is converted into an URL, after
        replacing certain strings with the arguments of this method.
        Currently the list of replacements is:

            '{%uid}': Replaced by the uid argument.
        """

        try:
            info = api.portal.get_registry_record(AUTHOR_TABS_KEY)
        except api.exc.InvalidParameterError:
            return []

        base_url = api.portal.get().absolute_url()

        tabs = []
        for line in info:
            title, path, mode = (line.split('::') + ['', '', ''])[:3]
            if not title or not path:
                continue
            path = path.replace('{%uid}', uid)
            url = '{0}/{1}'.format(base_url, path)
            tabs.append((_(title), url, mode))

        return tabs
