from zope import schema
from zope.component import adapts
from zope.interface import implements, Interface
from zope.publisher.browser import IBrowserRequest

from collective.customizablePersonalizeForm.adapters.interfaces import \
    IExtendedUserDataSchema, IExtendedUserDataPanel

from vnccollab.content import messageFactory as _


class UserDataSchemaAdapter(object):
    adapts(object, IBrowserRequest)
    implements(IExtendedUserDataSchema)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getSchema(self):
        return IUserDataSchema


class UserDataSchemaPropertiesAdapter(object):
    adapts(object, IBrowserRequest)
    implements(IExtendedUserDataPanel)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getProperties(self):
        return ['position', 'telephone']


class IUserDataSchema(Interface):

    position = schema.TextLine(
        title=_("Company Position"),
        description=_("Position in the company"),
        required=False)

    telephone = schema.TextLine(
        title=_("Telephone Number"),
        description=_("Personal Phone Number"),
        required=False)
