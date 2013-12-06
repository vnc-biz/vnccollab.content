# import transaction
from persistent import Persistent
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from AccessControl import getSecurityManager

from zope.interface import implements

from .interfaces import IFollowing


class Following(Persistent):
    """Local utility for follow/unfollow users.
    """
    implements(IFollowing)
    __allow_access_to_unprotected_subobjects__ = True

    def __init__(self):
        self._subscribed_to = PersistentDict()
        self._my_subscribers = PersistentDict()

    def _auth_user_id(self):
        manager = getSecurityManager()
        return manager.getUser().getId()

    def _append(self, data, key, value):
        if data.get(key, False):
            if value not in data[key]:
                data[key].append(value)
        else:
            data[key] = PersistentList()
            data[key].append(value)

    def _remove(self, data, key, value):
        if data.get(key, False) and value in data[key]:
            data[key].remove(value)

    # High Level API Methods

    def subscribe(self, user1, user2):
        """Subscribe 'user1' to 'user2'.

        If user1 is None, get authenticated user id.
        """
        user = user1 if user1 else self._auth_user_id()
        if user2 == user:
            # do not subscribe to myself
            return
        self._append(self._subscribed_to, user, user2)
        self._append(self._my_subscribers, user2, user)

    def unsubscribe(self, user1, user2):
        """Unsubscribe 'user1' from 'user2'.

        If user1 is None, get authenticated user id.
        """
        user = user1 if user1 else self._auth_user_id()
        if user2 == user:
            # nothing to do
            return
        self._remove(self._subscribed_to, user, user2)
        self._remove(self._my_subscribers, user2, user)

    def is_following(self, user1, user2):
        """Check if 'user1' is following 'user2'.

        If user1 is None, get authenticated user id.
        """
        user = user1 if user1 else self._auth_user_id()
        return self._subscribed_to.get(user, False) and \
            user2 in self._subscribed_to[user]

    def is_followed_by(self, user1, user2):
        """Check if 'user1' is followed by 'user2'.

        If user1 is None, get authenticated user id.
        """
        user = user1 if user1 else self._auth_user_id()
        return self._my_subscribers.get(user, False) and \
            user2 in self._my_subscribers[user]

    def has_followers(self, user):
        """Check if user is followed by any other user.

        If user is None, get authenticated user id.
        """
        user = user if user else self._auth_user_id()
        return len(self._my_subscribers.get(user, [])) > 0

    def has_followings(self, user):
        """Check if user is following anybody.

        If user is None, get authenticated user id.
        """
        user = user if user else self._auth_user_id()
        return len(self._subscribed_to.get(user, [])) > 0

    def get_followers(self, user):
        """Get all followers of the user.

        If user is None, get authenticated user id.
        """
        user = user if user else self._auth_user_id()
        return list(self._my_subscribers.get(user, []))

    def get_followings(self, user):
        """Get all users the user is following.

        If user is None, get authenticated user id.
        """
        user = user if user else self._auth_user_id()
        return list(self._subscribed_to.get(user, []))
