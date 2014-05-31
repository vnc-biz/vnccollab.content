from vnccollab.common.util import replace_all_portlets, _class_name
from vnccollab.content.portlets import generic_iframe, special_rss


def upgrade_1003_1004(context):
    """Replaces theme's etherpad portlet to content ones."""
    replace_all_portlets(_replace_iframe)
    replace_all_portlets(_replace_rss)


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
