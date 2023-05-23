// This file is used to store the last active tab in the browser's local storage
$(function() {
    // when a tab is clicked
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      // save the latest tab using a cookie
      localStorage.setItem('lastTab', $(this).attr('id'));
    });

    // get the last tab if it exists
    var lastTabStories = localStorage.getItem('lastTab');
    
    if (lastTabStories) {
      $('#' + lastTabStories).tab('show');
    } else {
      // Set the first tab to active if no active tab exists
      $('a[data-toggle="tab"]:first').tab('show');
    }
  });