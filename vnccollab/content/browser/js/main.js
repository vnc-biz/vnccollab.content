// module definition
var vnc_collab_content = (function () {

  // Private components

  //
  // Following Controls
  //

  function initFollowingControls() {
    // attach hover actions
    jq('a.followLink, a.unfollowLink').mouseover(function(event){
      var link = $(event.target);
      link.data('orig_label', link.text()).text(link.attr('title'));
    }).mouseout(function(event){
      var link = $(event.target);
      if (link.data('orig_label')) {
        link.text(link.data('orig_label'));
      }
    });

    // attach click handlers to Follow/Unfollow buttons
    jq('body').on('click', 'a.followLink, a.unfollowLink', function(event){
       event.preventDefault();
       event.stopPropagation();
       var link = $(event.target),
        path = link.is('.followLink') ? '@@follow_user' : '@@unfollow_user';

      jq.ajax({
        'url': portal_url + '/' + path,
        'type': 'POST',
        'dataType': 'json',
        'data': {'user1': '', 'user2': link.data('userid')},
        'success': function(data, status, xhr){
          link.text(data['label']).attr('title', data['title'])
            .data('orig_label', '');
          if (link.is('.followLink')) {
            link.removeClass('followLink').addClass('unfollowLink');
          } else {
            link.removeClass('unfollowLink').addClass('followLink');
          }
          return false;
        },
        'error': function(){
          alert('Sorry, something went wrong on the server. Please, try a ' +
            'bit later.');
          return false;
        }
      });

      return false;
    });
  }

  //
  // User profile tabs Handler
  //

  function initUserProfileTabHandler() {
    jq('#userprofile-tabmenu').on('click', 'a', function(event) {
      event.preventDefault();

      var pageClass =  '.' + jq(this).data('pageTab');
      var $page = jq('#userprofile-tabcontents').find(pageClass);
      var mode = jq(this).data('pageMode');
      var href = jq(this).attr('href');

      // select/unselect tab menu option
      jq('#userprofile-tabmenu a').removeClass('selected');
      jq(this).addClass('selected');

      // hide all tabs panel
      jq('.formPanel').hide();

      // if dynamic content then load it
      if ( href  != '#') {
         var content = '';

         // show the clean page
         $page.empty().show();

        // start spinner
        jq('#userprofile-spinner').show();

        // If want to load by iframe
        if (mode == 'iframe') {
          content = '<iframe src="' + href + '" width="100%" height="750px" align="center"></iframe>';

          // hide unnecessary content
          jq('#userprofile-tabcontents').find('iframe').contents().find('#edit-bar').hide();
          jq('#userprofile-tabcontents').find('iframe').contents().find('#portal-header').hide();
          jq('#userprofile-tabcontents').find('iframe').contents().find('#portal-footer').hide();
          jq('#userprofile-spinner').hide();
        } else {
          content = loadTab(href);
        }
        // Append content to tab
        $page.append(content);
      } else {
        $page.show();
      }

      // load content tab by ajax
      function loadTab(url) {
          var content = '';

          jq('#userprofile-spinner').show();

          jq.ajax({
            type: 'GET',
            url: url,
            dataType: 'html',
            async: false,
            cache: false,
            success: function( data ){
              var $content = jq(data).find('#content');
              var $script =  jq(data).find('script[type="text/javascript"]');

              $script.each(function(i) {
                    eval(jq(this).text());
              });

              jq('#userprofile-spinner').hide();

              // remove unneccesary content
              $content.find('.backLink').remove();
              $content.find('h1').remove();



              content = $content.html();
            },
            error: function(){
              jq('#userprofile-spinner').hide();
              content = '';
            }
          });
          return content;
      }
    });
  }

  // public interface
  return {
        initFollowingControls: initFollowingControls,
        initUserProfileTabHandler: initUserProfileTabHandler
  };
}) ();


// run on load
jq(function() {
  var me = vnc_collab_content;
  me.initFollowingControls();
  me.initUserProfileTabHandler();
});
