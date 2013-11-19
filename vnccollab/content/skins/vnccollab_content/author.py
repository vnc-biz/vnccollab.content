## Script (Python) "author"
from Products.PythonScripts.standard import url_unquote_plus

request = context.REQUEST
response = request.RESPONSE

uid = (len(request.traverse_subpath) > 0 \
    and url_unquote_plus(request.traverse_subpath[0])) \
    or request.get('author', None)
url = '/@@author?uid=' + uid
response.redirect(url)
