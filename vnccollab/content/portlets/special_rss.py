from zope.formlib import form
from zope.interface import implements
from zope import schema
from plone.app.portlets.portlets.rss import RSSFeed

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from vnccollab.content import messageFactory as _


class ISpecialRSSPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Header"),
        description=_(u"Header of the RSS Portlet."),
        required=True,
        default=u'New in the Cloud')

    source = schema.List(
        title=_(u"RSS Sources"),
        description=u'Please select links that point to RSS feeds',
        required=True,
        value_type=schema.Choice(
            vocabulary='vnccollab.theme.vocabularies.ATLinkVocabulary',))

    count = schema.Int(title=_(u'Number of items to display'),
        description=_(u'How many items to list.'),
        required=True,
        default=5)

    timeout = schema.Int(title=_(u'Feed reload timeout'),
        description=_(u'Time in minutes for the feeds should be reloaded.'),
        required=True,
        default=15)


class Assignment(base.Assignment):
    implements(ISpecialRSSPortlet)

    header = u'New in the Cloud'
    source = []
    count = 5
    timeout = 15

    @property
    def title(self):
        """Return portlet header"""
        return self.header

    def __init__(self, header=u'New in the Cloud', source=[],
                 count=5, timeout=15):
        self.header = header
        self.source = source
        self.count = count
        self.timeout = timeout


class Renderer(base.DeferredRenderer):
    # This is an adaptation of plone.app.portlets.portlets.rss.Renderer
    # modified to handle several feeds
    render = ZopeTwoPageTemplateFile('templates/special_rss.pt')

    MAX_SUMMARY_LEN = 80

    @property
    def initializing(self):
        """should return True if deferred template should be displayed"""
        if any([not x.loaded for x in self.feeds]):
            return True
        if any([x.needs_update for x in self.feeds]):
            return True
        return False

    def deferred_update(self):
        """refresh data for serving via KSS"""
        for feed in self.data.feeds:
            feed.update()

    def update(self):
        """update data before rendering. We can not wait for KSS since users
        may not be using KSS."""
        self.feeds = []
        for link in self.data.source:
            rss = RSSFeed(link.remote_url(), self.data.timeout)
            rss.id = link.id
            self.feeds.append(rss)

        self.deferred_update()

    def items(self, feed):
        """Return postprocessed items"""
        return (self.sanitize(item) for item in feed.items[:self.data.count])

    def sanitize(self, item):
        """return a news feed item sanitized."""
        new = dict(**item)
        # Convert HTML to plain text.
        # We won't use portal_transforms due to potential problems with
        # encoding on the summary text.
        s = MLStripper()
        s.feed(new['summary'])
        summary = s.get_data()

        if len(summary) > self.MAX_SUMMARY_LEN:
            summary = summary[:self.MAX_SUMMARY_LEN] + '...'
        new['summary'] = summary

        return new


class AddForm(base.AddForm):
    form_fields = form.Fields(ISpecialRSSPortlet)
    label = _(u"Add Special RSS portlet")
    description = _(u"A portlet displaying multiple RSS sources "
                    u"(Its sources are link objects).")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(ISpecialRSSPortlet)
    label = _(u"Edit Special RSS portlet")
    description = _(u"A portlet displaying multiple RSS sources "
                    u"(Its sources are link objects).")


from HTMLParser import HTMLParser


class MLStripper(HTMLParser):
    '''Support class to convert HTML to ASCII'''
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
