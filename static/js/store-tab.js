// This file is used to store the last active tab in the browser's local storage
$(function() {
  // generate a simple unique deterministic ID for the page
  const pageid = window.location.pathname.replaceAll('/','_')

  // when a tab is clicked
  $('a[data-bs-toggle="tab"]').on('shown.bs.tab', function (e) {
    // save the latest tab using a cookie
    localStorage.setItem('lastTab' + pageid, $(this).attr('id'));
  });

  // get the last tab if it exists
  var lastTabStories = localStorage.getItem('lastTab' + pageid);

  if (lastTabStories) {
    $('#' + lastTabStories).tab('show');
  } else {
    // Set the first tab to active if no active tab exists
    $('a[data-bs-toggle="tab"]:first').tab('show');
  }
});
