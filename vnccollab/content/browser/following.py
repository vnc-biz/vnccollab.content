import json

from AccessControl import getSecurityManager

from zope.component import getUtility

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from vnccollab.content.interfaces import IFollowing


class FollowingView(BrowserView):
    """Provides utility functions for templates regarding users following
    functionality.
    """

    _users_list_template = ViewPageTemplateFile('templates/followers_list.pt')

    def _auth_user(self):
        """Authenticated user id"""
        return getSecurityManager().getUser().getId()

    def follow_user(self, user1, user2):
        """Subscribe user1 to user2.

        If user1 is None, get authenticated user id.
        """
        user = user1 and user1 or self._auth_user()
        following = getUtility(IFollowing)
        following.subscribe(user, user2)

        self.request.response.setHeader('Content-Type',
            'application/javascript')
        return json.dumps({
            'title': 'Unfollow',
            'label': 'Unfollow',
            'following': True,
        })

    def unfollow_user(self, user1, user2):
        """UnSubscribe user1 from user2.

        If user1 is None, get authenticated user id.
        """
        user = user1 and user1 or self._auth_user()
        following = getUtility(IFollowing)
        following.unsubscribe(user, user2)

        self.request.response.setHeader('Content-Type',
            'application/javascript')
        return json.dumps({
            'title': 'Follow',
            'label': 'Follow',
            'following': False,
        })

    def follow_button(self, user1, user2):
        """Returns following button details depending on subscription settings.
        user1 - profile owner, owner of follow button
        user2 - user that wants to see follow button for user1

        If no userid given, get authenticated user id.
        """
        user = user2 and user2 or self._auth_user()

        # return nothing if users are equal
        if user == user1:
            return {}

        # check if user1 is followed by user
        button = {}
        following = getUtility(IFollowing)
        if following.is_following(user, user1):
            button = {
                'title': 'Unfollow',
                'label': 'Unfollow',
                'following': True,
            }
        else:
            button = {
                'title': 'Follow',
                'label': 'Follow',
                'following': False,
            }

        return button

    def user_following(self, userid=None):
        """Returns rendered view of users current user is following"""
        auth = self._auth_user()
        userid = userid and userid or auth
        purl = getToolByName(self.context, 'portal_url')()
        img = '%s/defaultUser.png' % purl
        mtool = getToolByName(self.context, 'portal_membership')
        acl_users = getToolByName(self.context, 'acl_users')
        owner = acl_users.getUserById(userid)
        owner_name = userid
        if owner:
            owner_name = owner.getProperty('fullname') or userid
        following = getUtility(IFollowing)

        users = []
        for uid in following.get_followings(userid):
            user = acl_users.getUserById(uid)
            name = uid
            homepage = ''
            if user:
                name = user.getProperty('fullname') or uid
                homepage = user.getProperty('home_page') or ''

            # prepare image url
            portrait = mtool.getPersonalPortrait(uid)
            if portrait is not None:
                img = portrait.absolute_url()

            users.append({
                'id': uid,
                'name': name,
                'url': '%s/author/%s' % (purl, uid),
                'img': img,
                'homepage': homepage,
                'following': following.is_following(auth, uid),
                'show_button': auth != uid,
            })

        return self._users_list_template(title='%s is Following:' % owner_name,
            back_url='%s/author/%s' % (purl, userid),
            users=users)

    def user_followers(self, userid=None):
        """Returns rendered view of current user followers"""
        auth = self._auth_user()
        userid = userid and userid or auth
        purl = getToolByName(self.context, 'portal_url')()
        img = '%s/defaultUser.png' % purl
        mtool = getToolByName(self.context, 'portal_membership')
        acl_users = getToolByName(self.context, 'acl_users')
        owner = acl_users.getUserById(userid)
        owner_name = userid
        if owner:
            owner_name = owner.getProperty('fullname') or userid
        following = getUtility(IFollowing)

        users = []
        for uid in following.get_followers(userid):
            user = acl_users.getUserById(uid)
            name = uid
            homepage = ''
            if user:
                name = user.getProperty('fullname') or uid
                homepage = user.getProperty('home_page') or ''

            # prepare image url
            portrait = mtool.getPersonalPortrait(uid)
            if portrait is not None:
                img = portrait.absolute_url()

            users.append({
                'id': uid,
                'name': name,
                'url': '%s/author/%s' % (purl, uid),
                'img': img,
                'homepage': homepage,
                'following': following.is_following(auth, uid),
                'show_button': auth != uid,
            })

        return self._users_list_template(title='%s Followers:' % owner_name,
            back_url='%s/author/%s' % (purl, userid),
            users=users)
