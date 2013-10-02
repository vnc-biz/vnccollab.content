//
// Deferred Portlets
//
function initDeferredPortlets() {
  function deferredUrlInfo(elem) {
    var $elem = jq(elem);
    var manager = $elem.attr('portlet-manager');
    var name    = $elem.attr('portlet-name');
    var key     = $elem.attr('portlet-key');

    if (!manager || ! name || !key) {
      return '';
    }

    return ({
      'url': window.location.origin + window.location.pathname + '/portlet_deferred_render',
      'data': {
        'manager': manager,
        'name': name,
        'key': key
      }
    });
  }

  function updatePortlet(elem){
    // Returns a funciton to update the portlet represented by elem DOM
    var fn = function(data) {
      var $elem = jq(elem),
          $data = jq(data);
  
      // We want to be sure we got the portlet and not an error page
      if ($data.hasClass('portlet-deferred')) {
        $data.find('.portletBody').slimScroll({'height': '240px'});
        $elem.replaceWith($data);
        attachPortletButtons();
      } else {
        $elem.find('.portletBodyWrapper').empty();
      }
    }
    return fn;
  }

  function deferredRender() {
    // Starts the deferred render of the portlet,
    // if it has enough info
    var urlInfo = deferredUrlInfo(this);
    if (!urlInfo) {
      return;
    }

    var url = urlInfo.url;
    var data = urlInfo.data;
    jq.get(url, data, updatePortlet(this));
  }

  var deferredPortlets = jq('.portlet-deferred');
  deferredPortlets.each(deferredRender);
}


jq(function() {
     initDeferredPortlets();
   });
