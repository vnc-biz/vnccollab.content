import logging
from BeautifulSoup import BeautifulSoup

from zope.formlib import form
from zope.interface import implements
from zope import schema
from zope.testbrowser.browser import Browser

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from vnccollab.content import messageFactory as _
from vnccollab.common.portlets import deferred
from vnccollab.content.util import log_exception

logger = logging.getLogger('vnccollab.content.EtherpadListsPortlet')


class IEtherpadsListPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Header"),
        description=_(u"Header of the portlet."),
        required=True,
        default=u'Your Pads')

    url = schema.URI(
        title=_(u"Etherpad Root URL"),
        description=_(u"Root url to your Etherpad service. If not set, "
                      u"it will be picked from settings."),
        required=False)

    count = schema.Int(
       title=_(u"Number of pads to display"),
       description=u'',
       required=True,
       default=10)

    username = schema.ASCIILine(
        title=_(u"Username"),
        description=_(u"If not set, etherpad_username property of "
            "authenticated user will be used."),
        required=False,
        default='')

    password = schema.Password(
        title=_(u"Password"),
        description=_(u"If not set, etherpad_password property of authenticated"
            " user will be used."),
        required=False,
        default=u'')


class Assignment(base.Assignment):
    implements(IEtherpadsListPortlet)

    header = u'Your Pads'
    url = 'https://vitaliy.etherpad.zdemo.vnc.biz'
    count = 10
    username = ''
    password = u''

    @property
    def title(self):
        """Return portlet header"""
        return self.header

    def __init__(self, header=u'Your Pads',
                 url='https://vitaliy.etherpad.zdemo.vnc.biz',
                 count=10, username='', password=u''):
        self.header = header
        self.url = url
        self.count = count
        self.username = username
        self.password = password


class Renderer(deferred.DeferredRenderer):

    render = ZopeTwoPageTemplateFile('templates/etherpads_list.pt')

    def refresh(self):
        self.pads = self.getPads()

    @memoize
    def getPads(self):
        pads = []
        username, password, url = self.getUserData()
        if not (username and password and url):
            return ()

        # try to request etherpad for page with table of pads
        try:
            content = self._getPadsPage()

        except:
            log_exception(_(u"Error during fetching pads from %s" % url),
                context=self.context, logger=logger)
            return ()

        # try to parse html page into pads
        try:
            pads = self._parsePadsPage(content, self.trail_url(url),
                self.data.count)

        except:
            log_exception(_(u"Error during parsing pads page from %s" % url),
                context=self.context, logger=logger)
            return ()

        return tuple(pads)

    def _parsePadsPage(self, content, base_url, limit):
        pads = []
        soup = BeautifulSoup(content)

        # go over pads table rows, skipping first header row
        counter = 0
        for row in soup.find('table', id='padtable').findAll('tr')[1:]:
            if limit and limit <= counter:
                break

            # get row cells
            ctitle, cdate, ceditors = row.findAll('td')[:3]

            if not (ctitle and cdate and ceditors):
                continue

            # prepare pad url
            link = ctitle.find('a')
            if not link:
                continue

            url = '%s%s' % (base_url, link.get('href'))
            if not url:
                continue

            # prepare editors
            editors = []
            for editor in ceditors.findAll('a'):
                editors.append({
                    'name': editor.text,
                    'url': '%s%s' % (base_url, editor.get('href'))
                })

            pads.append({
                'url': url,
                'title': link.text,
                'date': cdate.text,
                'editors': tuple(editors)
            })
            counter += 1

        return pads

    def _getPadsPage(self):
        username, password, url = self.getUserData()

        # login
        browser = Browser()
        browser.open('%s/ep/account/sign-in' % self.trail_url(url))
        browser.getControl(name='email').value = username
        browser.getControl(name='password').value = password
        browser.getForm(id='signin-form').submit()

        # open pads table page
        browser.getLink('Pads').click()

        return safe_unicode(browser.contents)

    @memoize
    def root_url(self):
        """Return url w/o trailing slash prepared either from portlet or
        user settings.

        Used in template.
        """
        return self.trail_url(self.getUserData()[2])

    def trail_url(self, url=None):
        """Remove trailing slash from url."""
        if url and url.endswith('/'):
            return url[:-1]
        return url

    @memoize
    def getUserData(self):
        """Returns username, password and root etherpad url for user.

        Returns tuple of:
            (username, password, root etherpad url)
        """
        mtool = getToolByName(self.context, 'portal_membership')
        member = mtool.getAuthenticatedMember()
        username, password, url = self.data.username, self.data.password, \
            self.data.url

        # take username and password from authenticated user Etherpad creds
        if not (username and password):
            username, password = member.getProperty('etherpad_username', ''), \
                member.getProperty('etherpad_password', '')

        # if not set globally, take url from user settings
        if not url:
            url = member.getProperty('etherpad_url', '')

        # password could contain non-ascii chars, ensure it's properly encoded
        return username, safe_unicode(password).encode('utf-8'), url

    @property
    def title(self):
        """return title of feed for portlet"""
        return self.data.header


class AddForm(base.AddForm):
    form_fields = form.Fields(IEtherpadsListPortlet)
    label = _(u"Add Etherpad Lists portlet")
    description = _(u"A portlet displaying list of Etherpad pads.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IEtherpadsListPortlet)
    label = _(u"Edit Etherpad Lists portlet")
    description = _(u"A portlet displaying list of Etherpad pads.")
