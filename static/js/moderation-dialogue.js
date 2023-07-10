$(() => {
  let submitModal = new bootstrap.Modal($('#submitModal').get(0));

  // Attach the dialogue check to the submit button
  $('#submitBtn').on('click', (event) => {
    let moderation_status = $('#id_moderation_status').val();
    let shouldShowModal = false;
    let text = ""
    let reasons = [];
    try {
      let moderation_reply = $("#id_moderation_reply").val()
      if (moderation_reply) {
        reasons = JSON.parse(moderation_reply) || []
      }
    } catch(e) {
      console.log('Error parsing submitted moderation reasons JSON: ' + e.message)
    }
    let reason_count = reasons.length;
    let red_count = 0;
    reasons.forEach((item) => {if (item.severity == 'red') {red_count +=1;}});

    if ((reason_count > 0) && (moderation_status == 'not reviewed')) {
      // The user is trying to set the story to 'not reviewed' but added moderation comments
      text = $('#template-text-not-reviewed-comments');
      $('#closeModal').show();
      $('#cancelModal,#submitForm').hide();
      shouldShowModal = true;
    }
    else if ((reason_count == 0) && (moderation_status == 'rejected')) {
      // The user is trying reject a story without giving any reasons
      text = $('#template-text-reject-no-comments');
      $('#closeModal').hide();
      $('#cancelModal,#submitForm').show();
      shouldShowModal = true;
    }
    else if ((red_count > 0) && (moderation_status == 'approved')) {
      // Check whether there are any "Red" reasons/
      // The user is trying reject a story without giving any reasons
      text = $('#template-text-approve-comments');
      $('#closeModal').show();
      $('#cancelModal,#submitForm').hide();
      shouldShowModal = true;
    }

    if (shouldShowModal) {
      // Show the dialogue box
      $('#modal-text').empty().append(text.clone().prop('content'));

      event.preventDefault();
      submitModal.show();
    }
    else {
      // Skip the dialogue box and just submit the form
      $('.form-context').submit();
    }
  });

  // When the submit button is clicked in the modal popup, submit the form
  $('#submitForm').on('click', function () {
    submitModal.hide();
    $('.form-context').submit();
  });
});




