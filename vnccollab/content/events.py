from Products.CMFCore.utils import getToolByName

def turnOffLocalRolesInheritance(obj, event):
    """Block local roles inheritance for newly created object"""
    # If user has inherited local roles, locally set roles he inherited before
    # to avoid definitive lose of access (refs #11945)
    mtool = getToolByName(obj, 'portal_membership')
    user = mtool.getAuthenticatedMember()
    if user is None:
        return
    
    context_roles = user.getRolesInContext(obj)
    global_roles = user.getRoles()
    local_roles = [r for r in context_roles if r not in global_roles]
    if local_roles:
        obj.manage_setLocalRoles(user.getId(), local_roles)
    obj.__ac_local_roles_block__ = True
    obj.reindexObjectSecurity()
