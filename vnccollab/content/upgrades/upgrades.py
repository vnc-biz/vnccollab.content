from vnccollab.common.util import replace_all_portlets, _class_name
from vnccollab.content.portlets import etherpads_list


def upgrade_1003_1004(context):
    """Replaces theme's etherpad portlet to content ones."""
    replace_all_portlets(_replace_etherpad)


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
