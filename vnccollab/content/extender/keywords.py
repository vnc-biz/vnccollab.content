from zope.component import adapts
from zope.interface import implements

from Products.Archetypes.interfaces import IBaseContent
from  Products.Archetypes.interfaces.base import IBaseObject
# from Products.Archetypes import public as atapi

from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender, \
    ISchemaModifier

# from Products.AutocompleteWidget.AutocompleteWidget import AutocompleteWidget
from vnccollab.content.form.raptus_autocomplete import \
    KeywordsAutocompleteMultiSelectionWidget
from vnccollab.content.browser.interfaces import IPackageLayer
from vnccollab.content import messageFactory as _


class KeywordsWidgetModifier(object):
    """Here we assign AutoComplete widget to Subject field"""

    adapts(IBaseObject)
    implements(ISchemaModifier, IBrowserLayerAwareExtender)
    
    layer = IPackageLayer
    
    def __init__(self, context):
        self.context = context
        
    def fiddle(self, schema):
        if schema.get('subject', None) is None:
            return
        
        # update Subject field widget
        old_widget = schema['subject'].widget
        schema['subject'].widget = KeywordsAutocompleteMultiSelectionWidget(
            label=old_widget.label,
            description=old_widget.description,
            # macro='keywordsautocomplete_widget',
        )
