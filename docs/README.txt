.. contents::

vnccollab.content
=================

Overview
--------

``vnccollab.content`` offers content tools for VNC Collaboration. Here you can find
the `Following` utility to create following between users (user A is
followed/following user B), author page, and `AutoComplete` widget to
Subject field.

Installation
------------

Please read INSTALL.txt for more details.

Usage
-----

After installing the package, you can access IFollowing utilty in this way:

    following = getUtility(IFollowing)

and you can use the `Following` methods:

* subscribe(user1, user2) - subscribe 'user1' to 'user2'. If user1 is None,
  get the current user.

* unsubscribe(user1, user2) - unsubscribe 'user1' from 'user2'. If user1 is
  None, get the current user.

* is_following(user1, user2) - check if 'user1' is following 'user2'. If user1
  is None, get the current user.

* is_followed_by(user1, user2) - check if 'user1' is followed by 'user2'. If
  user1 is None, get the current user.

* has_followers(user) - check if user is followed by any other user. If user is
  None, get the current user.

* has_followings(user) - check if user is following anybody. If user is None,
  get the current user.

* get_followers(user) - get all followers of the user. If user is None, get
  the current user.

* get_followings(user) - get all users the user is following. If user is None,
  get the current user.
