.. contents::

vnccollab.content
=================

Overview
--------

``vnccollab.content`` offers contents tools for VNC Collaboration. You can find
here `Following` utility for marking following between users (user A is
followed/following user B), author page, assign `AutoComplete` widget to
Subject field.

Installation
------------

Please read INSTALL.txt for more details.

Usage
-----

After installing the package, you're have access to IFollowing utuilty,
accessed by:

    following = getUtility(IFollowing)

and you can use methods:

* subscribe(user1, user2) - subscribe 'user1' to 'user2'. If user1 is None,
  get authenticated user id.

* unsubscribe(user1, user2) - unsubscribe 'user1' from 'user2'. If user1 is
  None, get authenticated user id.

* is_following(user1, user2) - check if 'user1' is following 'user2'. If user1
  is None, get authenticated user id.

* is_followed_by(user1, user2) - check if 'user1' is followed by 'user2'. If
  user1 is None, get authenticated user id.

* has_followers(user) - check if user is followed by any other user. If user is
  None, get authenticated user id.

* has_followings(user) - check if user is following anybody. If user is None,
  get authenticated user id.

* get_followers(user) - get all followers of the user. If user is None, get
  authenticated user id.

* get_followings(user) - get all users the user is following. If user is None,
  get authenticated user id.
