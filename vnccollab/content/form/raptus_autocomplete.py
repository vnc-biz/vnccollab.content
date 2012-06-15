import simplejson

from Acquisition import aq_inner

from Products.Five.browser import BrowserView

from Products.Archetypes.Registry import registerPropertyType
from Products.Archetypes.Registry import registerWidget

from Products.CMFPlone.utils import safe_unicode

from raptus.autocompletewidget import widget as base


class KeywordsAutocompleteSearch(BrowserView):
    
    def __call__(self):
        return simplejson.dumps(self._search())
    
    def _search(self, param='term'):
        context = aq_inner(self.context)
        field = self.request.get('f', None)
        query = self.request.get(param, '')
        limit = self.request.get('limit', None)
        if not query or not field:
            return []
        
        field = context.Schema().getField(field)
        if not field:
            return []
        
        query = query.lower()
        values = context.collectKeywords(field.getName(), field.accessor)
        return [v for v in values if query in v.lower()]
    
class KeywordsAutocompletePopulate(KeywordsAutocompleteSearch):
    
    def __call__(self):
        query = (self.request.get('q', '') or '').strip()
        if not query:
            return ''
        
        results = self._search('q')
        for r in results:
            if query == r:
                return r

class KeywordsAutocompleteBaseWidget(base.AutocompleteBaseWidget):
    """Override raptus.autocompletewidget in order to set our own
    ajax search autocomplete url which knows how to get Archetypes
    Keywords Widget vocabulary items.
    """
    
    # JavaScript template
    
    js_template = """\
    (function($) {
        $().ready(function() {
            $('#archetypes-fieldname-%(id)s #%(id)s').each(function() {
                $('#archetypes-fieldname-%(id)s').append('<input name="%(id)s-input" type="text" id="%(id)s-input" />');
                %(js_populate)s
                $(this).remove();
                
                // append Add link to autocomplete input, it'll add new tags,
                // that do not exist yet
                var input = $('#%(id)s-input');
                var add_link = input.after('<a href="#" style="margin-left: 10px" id="autocomplete-add-%(id)s">Add as a New Tag</a>');
                $('#autocomplete-add-%(id)s').click(function(event){
                  // skip empty value
                  if (!input.val().strip()) {
                    input.val('');
                    return false;
                  }
                  
                  // populate checkboxes from entered value
                  value = input.val().split("\\n");
                  for (var i=0; i<value.length; i++) {
                    var v = value[i].strip();
                    if (v) {
                        $('#archetypes-fieldname-%(id)s #%(id)s-input').before("<" + "label class='plain'><" + "input type='checkbox' name='%(id)s:list' checked='checked' value='" + v + "' /> " + v + "</label><br />");
                    }
                  }
                  
                  // reset input
                  input.val('');
                  return false;
                });
                
                $('#archetypes-fieldname-%(id)s #%(id)s-input').autocomplete({
                    source: '%(url)s/@@keywordsautocompletewidget-search?f=%(id)s',
                    minLength: %(minChars)d,
                    select: %(js_callback)s
                });
            })
        });
    })(jQuery);
    """

class KeywordsAutocompleteSelectionWidget(KeywordsAutocompleteBaseWidget,
    base.AutocompleteSelectionWidget):
    """See doc string in above defined class"""
    
    _properties = base.AutocompleteSelectionWidget._properties.copy()
    
    # JavaScript template
    
    # the funny <" + "input bit is to prevent breakage in testbrowser tests
    # when it parses the js as a real input, but with a bogus value
    js_callback_template = """\
    function(event, ui) {
        var data = ui.item ? ui.item.value : '';
        var field = $('#archetypes-fieldname-%(id)s input[type="radio"][value="' + data + '"]');
        if(field.length == 0)
            $('#archetypes-fieldname-%(id)s #%(id)s-input').before("<" + "label class='plain'><" + "input type='radio' name='%(id)s' checked='checked' value='" + data + "' /> " + data + "</label><br />");
        else
            field.each(function() { this.checked = true });
        if(data) {
            $('#archetypes-fieldname-%(id)s #%(id)s-input').val('');
            return false;
        }
    }
    """
    
    js_populate_template = """\
    var value = $(this).val();
    if(value)
        $.get('%(url)s/@@keywordsautocompletewidget-populate', {'f': '%(id)s', 'q': value}, function(data) {
            if(data) {
                $('#archetypes-fieldname-%(id)s #%(id)s-input').before("<" + "label class='plain'><" + "input type='radio' name='%(id)s' checked='checked' value='" + data + "' /> " + data + "</label><br />");
            }
        }, 'json');
    """
    
class KeywordsAutocompleteMultiSelectionWidget(KeywordsAutocompleteBaseWidget,
    base.AutocompleteMultiSelectionWidget):
    """See doc string in above defined class"""
    
    _properties = base.AutocompleteMultiSelectionWidget._properties.copy()
    
    # JavaScript template
    
    # the funny <" + "input bit is to prevent breakage in testbrowser tests
    # when it parses the js as a real input, but with a bogus value
    js_callback_template = """\
    function(event, ui) {
        var data = ui.item ? ui.item.value : '';
        var field = $('#archetypes-fieldname-%(id)s input[type="checkbox"][value="' + data + '"]');
        if(field.length == 0)
            $('#archetypes-fieldname-%(id)s #%(id)s-input').before("<" + "label class='plain'><" + "input type='checkbox' name='%(id)s:list' checked='checked' value='" + data + "' /> " + data + "</label><br />");
        else
            field.each(function() { this.checked = true });
        if(data) {
            $('#archetypes-fieldname-%(id)s #%(id)s-input').val('');
            return false;
        }
    }
    """
    
    js_populate_template = """\
    value = $(this).text().split("\\n");
    if(value)
        for(var i=0; i<value.length; i++)
            $.get('%(url)s/@@keywordsautocompletewidget-populate', {'f': '%(id)s', 'q': value[i]}, function(data) {
                if(data) {
                    $('#archetypes-fieldname-%(id)s #%(id)s-input').before("<" + "label class='plain'><" + "input type='checkbox' name='%(id)s:list' checked='checked' value='" + data + "' /> " + data + "</label><br />");
                }
            }, 'html');
    """

registerWidget(KeywordsAutocompleteSelectionWidget,
               title='Keywords Autocomplete selection',
               description=(''),
               used_for=('Products.Archetypes.Field.StringField',)
               )

registerWidget(KeywordsAutocompleteMultiSelectionWidget,
               title='Keywords Autocomplete multiselection',
               description=(''),
               used_for=('Products.Archetypes.Field.LinesField',)
               )

registerPropertyType('autoFill', 'boolean', KeywordsAutocompleteSelectionWidget)
registerPropertyType('minChars', 'integer', KeywordsAutocompleteSelectionWidget)
registerPropertyType('maxResults', 'integer',
    KeywordsAutocompleteSelectionWidget)
registerPropertyType('mustMatch', 'boolean',
    KeywordsAutocompleteSelectionWidget)
registerPropertyType('matchContains', 'boolean',
    KeywordsAutocompleteSelectionWidget)
registerPropertyType('formatItem', 'string',
    KeywordsAutocompleteSelectionWidget)
registerPropertyType('formatResult', 'string',
    KeywordsAutocompleteSelectionWidget)
