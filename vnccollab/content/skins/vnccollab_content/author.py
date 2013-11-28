## Script (Python) "author"
from Products.PythonScripts.standard import url_unquote_plus
from Products.CMFCore.utils import getToolByName

request = context.REQUEST
response = request.RESPONSE
portal_url = getToolByName(context, 'portal_url')()

uid = (len(request.traverse_subpath) > 0 \
    and url_unquote_plus(request.traverse_subpath[0])) \
    or request.get('author', None)
url = portal_url + '/@@author?uid=' + uid
response.redirect(url)
