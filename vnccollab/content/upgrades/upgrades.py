from vnccollab.common.util import replace_all_portlets, _class_name
from vnccollab.content.portlets import etherpads_list
from vnccollab.content.portlets import generic_iframe, special_rss, users_box


def upgrade_1003_1004(context):
    """Replaces theme's etherpad portlet to content ones."""
    replace_all_portlets(_replace_etherpad)
    replace_all_portlets(_replace_iframe)
    replace_all_portlets(_replace_rss)
    replace_all_portlets(_replace_users_box)


def _replace_etherpad(portlet, portlet_name):
    """Returns a content's ethepath portlet, given a theme's one."""
    class_name = _class_name(portlet)

    if class_name != 'vnccollab.theme.portlets.etherpad_list.Assignment':
        return None

    new_portlet = etherpads_list.Assignment(portlet.header, portlet.url,
                                            portlet.count, portlet.username,
                                            portlet.password)
    new_portlet.__name__ = portlet_name
    return new_portlet


def _replace_iframe(portlet, portlet_name):
    """Returns a content's iframe portlet, given a theme's one."""
    class_name = _class_name(portlet)

    if class_name != 'vnccollab.theme.portlets.generic_iframe.Assignment':
        return None
    new_portlet = generic_iframe.Assignment(portlet.header, portlet.uri,
                                            portlet.width, portlet.height)
    new_portlet.__name__ = portlet_name
    return new_portlet


def _replace_rss(portlet, portlet_name):
    """Returns a content's rss portlet, given a theme's one."""
    class_name = _class_name(portlet)

    if class_name != 'vnccollab.theme.portlets.special_rss.Assignment':
        return None

    new_portlet = special_rss.Assignment(portlet.header, portlet.source,
                                         portlet.count, portlet.timeout)
    new_portlet.__name__ = portlet_name
    return new_portlet


def _replace_users_box(portlet, portlet_name):
    """Returns a content's users_box portlet, given a theme's one."""
    class_name = _class_name(portlet)

    if class_name != 'vnccollab.theme.portlets.users_box.Assignment':
        return None

    new_portlet = users_box.Assignment(portlet.header,
                                       portlet.do_not_recurse,
                                       portlet.count)
    new_portlet.__name__ = portlet_name
    return new_portlet
