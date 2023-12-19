// Code for adding, removing and listing moderation replies on the moderation page
// For info about the selection code, see:
// https://css-tricks.com/how-to-create-actions-for-selected-text-with-the-selection-api/

$(function() {
  // Get the html for our moderation menu from the template
  var control = $($("#template-control").prop('content')).find('.control')
  var controlOpen = false
  var reasons = []
  // Initialise the reason section
  try {
    let moderation_reply = $("#id_moderation_reply").val()
    if (moderation_reply) {
      reasons = JSON.parse(moderation_reply) || []
    }
  } catch(e) {
    console.log('Error parsing moderation reasons JSON: ' + e.message)
    console.log('JSON string: "' + $("#id_moderation_reply").val() + '"');
  }
  applySeverityFormatting();
  generateReasons()

  function applySeverityFormatting() {
    // Style the menu items to match their severity
    // This avoids us having to duplicate the severity info
    control.find('[data-severity="red"]').addClass("moderation-red");
    control.find('[data-severity="amber"]').addClass("moderation-amber");
  }

  function forwardSelection(selection) {
    // Returns true if the selection was made forwards, otherwise false
    position = selection.anchorNode.compareDocumentPosition(selection.focusNode)
    if (!position
      && selection.anchorOffset > selection.focusOffset
      || position === Node.DOCUMENT_POSITION_PRECEDING) {
      forwards = false
    }
    else {
      forwards = true
    }
    return forwards
  }

  $('.moderatable_text').on("pointerup", function(event) {
    // Executed when some moderatable text has been selected
    textSelected(event)
  })

  function textSelected(event) {
    // Text has been selected, so we should open the moderation menu
    if (!controlOpen) {
      let selection = document.getSelection()
      let text = selection.toString()
      if (text !== "") {
        let rect = selection.getRangeAt(0).getBoundingClientRect()
        control.appendTo($("#experience_text"))
        const scrollTop = $(document).scrollTop()
        const y = `calc(${rect.bottom}px + calc(${scrollTop}px) + 8px)`
        if (forwardSelection(selection)) {
          x = `calc(${event.pageX}px - calc(${control.width()}px))`
        }
        else {
          x = `calc(${event.pageX}px)`
        }
        showReasons(x, y, text)
      }
    }
  }

  function showReasons(x, y, text) {
    // Opens the 'moderation reasons' menu at the given position on screen
    control.css({left: x, top: y})
    control.prop('text', text)
    controlOpen = true
    control.find(".addreason").on("click", function(event) {
      addReason($(this).data("reason"), $(this).data("href"),
        $(this).data("severity"), text)
      hideReasons()
      event.stopPropagation()
    })
    control.on("pointerdown", function(event) {
      // Executed when the user clicks on a menu item
      event.stopPropagation()
    })
  }

  function hideReasons() {
    // Hides the 'moderation reasons' menu
    control.find(".dropdown-toggle").dropdown("hide")
    $('.control').remove()
    controlOpen = false
    document.getSelection().removeAllRanges()
  }

  function addReason(reason, href, severity, text) {
    // Adds a moderation reason to the list
    reasons.push({reason: reason, href: href, severity: severity, text: text})
    generateReasons()
  }

  function removeReason(index) {
    // Removes a moderation reason from the list
    reasons.splice(index, 1)
    generateReasons()
  }

  function generateReasons() {
    // Inserts a list of moderation reasons into the page
    $("#reasons").empty()
    for (var index = 0; index < reasons.length; index++) {
      let reasonrow = $($("#template-reasons").prop('content')).find('.reason-row').clone()
      reasonrow.find(".reason").text(reasons[index].reason)
      reasonrow.find(".reason").attr("href", "/main/content_moderation_guidelines/#" + reasons[index].href)
      reasonrow.find(".text").text(reasons[index].text)
      reasonrow.find(".remove").on("click", {index: index}, function(event) {
        event.preventDefault()
        removeReason(event.data.index)
      })
      reasonrow.appendTo($("#reasons"))
    }
    if (reasons.length > 0) {
      $("#reason-titles").show()
    }
    else {
      $("#reason-titles").hide()
    }
    $("#id_moderation_reply").val(JSON.stringify(reasons))
  }

  $(document).on("pointerdown", function() {
    // Executed when the user clicks anywhere
    hideReasons()
  })

})

