import logging

from zope.formlib import form
from zope.interface import implements
from zope import schema

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from vnccollab.content import messageFactory as _

logger = logging.getLogger('vnccollab.content.GenericIframePortlet')


class IGenericIframePortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Header"),
        description=_(u"Header of the Generic Iframe Portlet."),
        required=True,
        default=u'Generic IFrame')

    uri = schema.URI(
        title=_(u"URL of the Iframe"),
        description=_(u"URL of the site to include."),
        required=True)

    width = schema.Int(
        title=_(u"Width"),
        default=200,
        required=True)

    height = schema.Int(
        title=_(u"Height"),
        default=200,
        required=True)


class Assignment(base.Assignment):
    implements(IGenericIframePortlet)

    header = u'Generic IFrame'
    uri = u''
    width = 200
    height = 200

    def __init__(self, header=u'', uri=u'', width=200, height=200):
        self.header = header
        self.uri = uri
        self.width = width
        self.height = height

    @property
    def title(self):
        """Return portlet header"""
        return self.header


class Renderer(base.Renderer):
    render = ZopeTwoPageTemplateFile('templates/generic_iframe.pt')

    @property
    def title(self):
        """return title of feed for portlet"""
        return self.data.header


class AddForm(base.AddForm):
    form_fields = form.Fields(IGenericIframePortlet)
    label = _(u"Add Generic Iframe Portlet")
    description = _(u"Renders an external page inside a portlet.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IGenericIframePortlet)
    label = _(u"Edit Generic Iframe Portlet")
    description = _(u"Renders an external page inside a portlet.")
