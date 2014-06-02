from Acquisition import aq_inner

from zope.formlib import form
from zope.interface import implements
from zope import schema
from zope.component import getMultiAdapter

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from vnccollab.content import messageFactory as _


class IUsersBoxPortlet(IPortletDataProvider):

    header = schema.TextLine(
        title=_(u"Header"),
        description=_(u"Header of the Users Box Portlet."),
        required=False,
        default=u'Users')

    do_not_recurse = schema.Bool(
        title=_(u"Do not fetch users recursively"),
        description=_(u"By default portlet displays all users that "
                      u"contributed to content under current container. If "
                      u"this option ticked, only current context object "
                      u"contributors will be shown."),
        required=False,
        default=False)

    count = schema.Int(
        title=_(u"Number of items to display"),
        description=u'',
        required=True,
        default=30)


class Assignment(base.Assignment):
    implements(IUsersBoxPortlet)

    header = u'Users'
    do_not_recurse = False
    count = 30

    @property
    def title(self):
        """Return portlet header"""
        return _(self.header) or _(u"Users Box")

    def __init__(self, header=u'Users', do_not_recurse=False, count=30):
        self.header = _(header)
        self.do_not_recurse = do_not_recurse
        self.count = count


class Renderer(base.Renderer):

    render = ZopeTwoPageTemplateFile('templates/users_box.pt')

    @property
    def available(self):
        return len(self._getUsers()) > 0

    def update(self):
        self.users = self._getUsers()
        self.header = _(self.data.header)

    @memoize
    def _getUsers(self):
        if not self.data.count:
            return ()

        users = []
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        acl_users = getToolByName(context, 'acl_users')
        mtool = getToolByName(context, 'portal_membership')
        cstate = getMultiAdapter((self.context, self.request),
                                 name='plone_context_state')

        # prepare catalog query
        query = {'sort_on': 'modified',
                 'sort_order': 'reverse'}
        path = '/'.join(cstate.folder().getPhysicalPath())
        if self.data.do_not_recurse:
            query['path'] = {'query': path, 'depth': 0}
        else:
            query['path'] = path

        added = []
        invalid = []
        purl = getToolByName(context, 'portal_url')()
        limit = self.data.count
        counter = 0
        for brain in catalog(**query):
            # already got enough users
            if counter >= limit:
                break

            creator = brain.Creator

            # skip duplicates
            if not creator or creator in added or creator in invalid:
                continue

            # check if user exists and whether user got profile image
            user = acl_users.getUserById(creator)
            if user is None:
                invalid.append(creator)
                continue

            # finally append user and increment counters
            users.append({
                'id': creator,
                'img': mtool.getPersonalPortrait(id=creator),
                'url': '%s/author/%s' % (purl, creator),
                'fullname': user.getProperty("fullname"),
                'email': user.getProperty("email")
            })
            added.append(creator)
            counter += 1

        return tuple(users)


class AddForm(base.AddForm):
    form_fields = form.Fields(IUsersBoxPortlet)
    label = _(u"Add Users Box Portlet")
    description = _(u"A portlet which lists users contributed to current "
                    "container.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IUsersBoxPortlet)
    label = _(u"Edit Users Box Portlet")
    description = _(u"A portlet which lists users contributed to current "
                    "container.")
