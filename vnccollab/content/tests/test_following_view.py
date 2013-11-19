import ast
import json
import urllib

from vnccollab.content.tests.base import FunctionalTestCase


class TestFollowingView(FunctionalTestCase):
    members = (
        ('secret', 'Scott Tiger', 'scott@tiger.com', ['members'], '2013-09-24'),
        ('secret', 'Johann Sebastian Bach', 'johan@bach.com', ['members'], '2013-09-24'),)

    def test_user_following_nothing(self):
        users = ((None, 'test_user_1_'),
                 (('scott@tiger.com', 'secret'), 'Scott Tiger'),
                 (('johan@bach.com', 'secret'), 'Johann Sebastian Bach'))

        for user in users:
            browser = self.login() if not user[0] else self.login(*user[0])
            browser.open(self.portal_url + '/@@user-following')
            self.assertIn('%s is Following:' % (user[1]), browser.contents)
            self.assertIn('No Users Yet.', browser.contents)
            self.logout(browser)


    def test_user_no_followers(self):
        users = ((None, 'test_user_1_'),
                 (('scott@tiger.com', 'secret'), 'Scott Tiger'),
                 (('johan@bach.com', 'secret'), 'Johann Sebastian Bach'))

        for user in users:
            browser = self.login() if not user[0] else self.login(*user[0])
            browser.open(self.portal_url + '/@@user-followers')
            self.assertIn('%s Followers:' % (user[1]), browser.contents)
            self.assertIn('No Users Yet.', browser.contents)
            self.logout(browser)

    def test_follow_user(self):
        browser = self.login('scott@tiger.com', 'secret')
        browser.open(self.portal_url + '/author/johan@bach.com')
        self.assertIn(
            '<a class="followLink" title="Follow" data-userid="johan@bach.com" href="#">Follow</a>',
            browser.contents)

        data = {'user1': '', 'user2': 'johan@bach.com'}
        browser.open(self.portal_url + '/@@follow_user', urllib.urlencode(data))
        data = json.loads(browser.contents)
        self.assertTrue(data['following'])
        self.assertEqual(data['title'], 'Unfollow')
        self.assertEqual(data['label'], 'Unfollow')

        browser.open(self.portal_url + '/author/' + 'johan@bach.com')
        self.assertIn(
            '<a class="unfollowLink" title="Unfollow" data-userid="johan@bach.com" href="#">Unfollow</a>',
            browser.contents)

        # incorret user - are you sure this is the correct behavior?
        data = {'user1': '', 'user2': 'johan_blah@bach.com'}
        browser.open(self.portal_url + '/@@follow_user', urllib.urlencode(data))
        data = json.loads(browser.contents)
        self.assertTrue(data['following'])
        self.assertEqual(data['title'], 'Unfollow')
        self.assertEqual(data['label'], 'Unfollow')

    def test_user_following(self):
        browser = self.login('scott@tiger.com', 'secret')

        data = {'user1': '', 'user2': 'johan@bach.com'}
        browser.open(self.portal_url + '/@@follow_user', urllib.urlencode(data))
        data = json.loads(browser.contents)
        self.assertTrue(data['following'])
        self.assertEqual(data['title'], 'Unfollow')
        self.assertEqual(data['label'], 'Unfollow')

        browser.open(self.portal_url + '/@@user-following')
        self.assertIn('<ul class="followersList">', browser.contents)
        self.assertIn('<a class="userImage" href="http://nohost/plone/author/johan@bach.com">', browser.contents)
        self.assertIn('Johann Sebastian Bach', browser.contents)
        self.assertIn('<a class="unfollowLink" title="Unfollow" data-userid="johan@bach.com" href="#">Unfollow</a>', browser.contents)

    def test_user_followers(self):
        browser = self.login('scott@tiger.com', 'secret')

        data = {'user1': '', 'user2': 'johan@bach.com'}
        browser.open(self.portal_url + '/@@follow_user', urllib.urlencode(data))
        data = json.loads(browser.contents)
        self.assertTrue(data['following'])
        self.assertEqual(data['title'], 'Unfollow')
        self.assertEqual(data['label'], 'Unfollow')
        self.logout(browser)

        browser = self.login('johan@bach.com', 'secret')
        browser.open(self.portal_url + '/@@user-followers')
        self.assertIn('<ul class="followersList">', browser.contents)
        self.assertIn('<a class="userImage" href="http://nohost/plone/author/scott@tiger.com">', browser.contents)
        self.assertIn('Scott Tiger', browser.contents)
        self.assertIn('<a class="followLink" title="Follow" data-userid="scott@tiger.com" href="#">Follow</a>', browser.contents)

        data = {'user1': '', 'user2': 'scott@tiger.com'}
        browser.open(self.portal_url + '/@@follow_user', urllib.urlencode(data))
        data = json.loads(browser.contents)
        self.assertTrue(data['following'])
        self.assertEqual(data['title'], 'Unfollow')
        self.assertEqual(data['label'], 'Unfollow')

        browser = self.login('johan@bach.com', 'secret')
        browser.open(self.portal_url + '/@@user-followers')
        self.assertIn('<ul class="followersList">', browser.contents)
        self.assertIn('<a class="userImage" href="http://nohost/plone/author/scott@tiger.com">', browser.contents)
        self.assertIn('Scott Tiger', browser.contents)
        self.assertIn('<a class="unfollowLink" title="Unfollow" data-userid="scott@tiger.com" href="#">Unfollow</a>', browser.contents)

    def test_follow_button(self):
        browser = self.login('scott@tiger.com', 'secret')

        data1 = urllib.urlencode({'user1': '', 'user2': 'johan@bach.com'})
        data2 = urllib.urlencode({'user1': 'johan@bach.com', 'user2': ''})

        browser.open(self.portal_url + '/@@follow_button', data2)
        result = ast.literal_eval(browser.contents)
        self.assertFalse(result['following'])
        self.assertEqual(result['label'], 'Follow')
        self.assertEqual(result['title'], 'Follow')

        browser.open(self.portal_url + '/@@follow_user', data1)

        browser.open(self.portal_url + '/@@follow_button', data2)
        result = ast.literal_eval(browser.contents)
        self.assertTrue(result['following'])
        self.assertEqual(result['label'], 'Unfollow')
        self.assertEqual(result['title'], 'Unfollow')

        browser.open(self.portal_url + '/@@unfollow_user', data1)

        browser.open(self.portal_url + '/@@follow_button', data2)
        result = ast.literal_eval(browser.contents)
        self.assertFalse(result['following'])
        self.assertEqual(result['label'], 'Follow')
        self.assertEqual(result['title'], 'Follow')

    def test_unfollow_user(self):
        browser = self.login('scott@tiger.com', 'secret')
        browser.open(self.portal_url + '/@@author?uid=' + 'johan@bach.com')
        self.assertIn(
            '<a class="followLink" title="Follow" data-userid="johan@bach.com" href="#">Follow</a>',
            browser.contents)

        data = {'user1': '', 'user2': 'johan@bach.com'}
        browser.open(self.portal_url + '/@@follow_user', urllib.urlencode(data))
        data = json.loads(browser.contents)
        self.assertTrue(data['following'])
        self.assertEqual(data['title'], 'Unfollow')
        self.assertEqual(data['label'], 'Unfollow')

        browser.open(self.portal_url + '/@@author?uid=' + 'johan@bach.com')
        self.assertIn(
            '<a class="unfollowLink" title="Unfollow" data-userid="johan@bach.com" href="#">Unfollow</a>',
            browser.contents)

        data = {'user1': '', 'user2': 'johan@bach.com'}
        browser.open(self.portal_url + '/@@unfollow_user', urllib.urlencode(data))

        browser.open(self.portal_url + '/@@author?uid=' + 'johan@bach.com')
        self.assertIn(
            '<a class="followLink" title="Follow" data-userid="johan@bach.com" href="#">Follow</a>',
            browser.contents)
