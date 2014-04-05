from zope.component import getUtility

from vnccollab.content.interfaces import IFollowing
from vnccollab.content.tests.base import FunctionalTestCase
from vnccollab.content.testing import createObject
from vnccollab.content.events import turnOffLocalRolesInheritance
from vnccollab.content.following import Following


class TestFollowingView(FunctionalTestCase):
    members = (
        ('secret', 'Scott Tiger', 'scott@tiger.com', ['members'], '2013-09-24'),
        ('secret', 'Scott2 Tiger2', 'scott2@tiger2.com', ['members'], '2013-09-24'),
        ('secret', 'Johann Sebastian Bach', 'johan@bach.com', ['members'], '2013-09-24'),
        ('secret', 'Johann2 Sebastian Bach', 'johan2@bach.com', ['members'], '2013-09-24'),)

    def test_subscribe(self):
        following = getUtility(IFollowing)
        following.subscribe('scott@tiger.com', 'scott2@tiger2.com')

        self.assertIn('scott@tiger.com', following._subscribed_to)
        self.assertIn('scott2@tiger2.com', following._subscribed_to['scott@tiger.com'])
        self.assertIn('scott2@tiger2.com', following._my_subscribers)
        self.assertIn('scott@tiger.com', following._my_subscribers['scott2@tiger2.com'])

    def test_unsubscribe(self):
        following = getUtility(IFollowing)
        following.subscribe('scott@tiger.com', 'scott2@tiger2.com')

        self.assertIn('scott@tiger.com', following._subscribed_to)
        self.assertIn('scott2@tiger2.com', following._subscribed_to['scott@tiger.com'])
        self.assertIn('scott2@tiger2.com', following._my_subscribers)
        self.assertIn('scott@tiger.com', following._my_subscribers['scott2@tiger2.com'])

        following.unsubscribe('scott@tiger.com', 'scott2@tiger2.com')
        self.assertTrue(len(following._subscribed_to['scott@tiger.com']) == 0)
        self.assertTrue(len(following._my_subscribers['scott2@tiger2.com']) == 0)

    def test_is_following(self):
        following = getUtility(IFollowing)
        following.subscribe('scott@tiger.com', 'scott2@tiger2.com')

        self.assertTrue(following.is_following('scott@tiger.com', 'scott2@tiger2.com'))
        self.assertFalse(following.is_following('scott2@tiger2.com', 'scott@tiger.com'))

        following.subscribe('scott2@tiger2.com', 'scott@tiger.com')

        self.assertTrue(following.is_following('scott@tiger.com', 'scott2@tiger2.com'))
        self.assertTrue(following.is_following('scott2@tiger2.com', 'scott@tiger.com'))

    def test_is_followed_by(self):
        following = getUtility(IFollowing)
        following.subscribe('scott@tiger.com', 'scott2@tiger2.com')

        self.assertTrue(following.is_followed_by('scott2@tiger2.com', 'scott@tiger.com'))
        self.assertFalse(following.is_followed_by('scott@tiger.com', 'scott2@tiger2.com'))

        following.subscribe('scott2@tiger2.com', 'scott@tiger.com')

        self.assertTrue(following.is_followed_by('scott2@tiger2.com', 'scott@tiger.com'))
        self.assertTrue(following.is_followed_by('scott@tiger.com', 'scott2@tiger2.com'))

    def test_has_followers(self):
        following = getUtility(IFollowing)
        following.subscribe('scott@tiger.com', 'scott2@tiger2.com')
        self.assertTrue(following.has_followers('scott2@tiger2.com'))
        self.assertFalse(following.has_followers('scott@tiger.com'))

    def test_has_followings(self):
        following = getUtility(IFollowing)
        following.subscribe('scott@tiger.com', 'scott2@tiger2.com')
        self.assertTrue(following.has_followings('scott@tiger.com'))
        self.assertFalse(following.has_followings('scott2@tiger2.com'))

    def test_get_followers(self):
        following = getUtility(IFollowing)
        following.subscribe('scott@tiger.com', 'scott2@tiger2.com')
        self.assertTrue(len(following.get_followers('scott2@tiger2.com')) == 1)
        self.assertIn('scott@tiger.com', following.get_followers('scott2@tiger2.com'))
        following.subscribe('johan2@bach.com', 'scott2@tiger2.com')
        self.assertTrue(len(following.get_followers('scott2@tiger2.com')) == 2)
        self.assertIn('scott@tiger.com', following.get_followers('scott2@tiger2.com'))
        self.assertIn('johan2@bach.com', following.get_followers('scott2@tiger2.com'))

    def test_get_followings(self):
        following = getUtility(IFollowing)
        following.subscribe('scott@tiger.com', 'scott2@tiger2.com')
        self.assertTrue(len(following.get_followings('scott@tiger.com')) == 1)
        self.assertIn('scott2@tiger2.com', following.get_followings('scott@tiger.com'))
        following.subscribe('johan2@bach.com', 'scott2@tiger2.com')
        following.subscribe('scott@tiger.com', 'johan2@bach.com')
        self.assertTrue(len(following.get_followings('scott@tiger.com')) == 2)
        self.assertIn('scott2@tiger2.com', following.get_followings('scott@tiger.com'))
        self.assertIn('johan2@bach.com', following.get_followings('scott@tiger.com'))
