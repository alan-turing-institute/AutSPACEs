$(document).ready(function () {
  let form = $('.form-context');
  let submitFormButton = $('#submitForm');
  let viewableCheckbox = $('#shareOnAutSPACEs');
 
  let submitModal = new bootstrap.Modal($('#submitModal').get(0));

  // Check whether Share Experience checkbox is ticked
  let shareExperience = () => {
    return viewableCheckbox.prop('checked');
  };

  let submitButton = $('#submitBtn');
  // when submit button is clicked, check if the Share Experience checkbox is ticked,
  // and the story exists (uuid) and has been moderated (approved)
  submitButton.on('click', (event) => {
    const uuid = submitButton.data('uuid');
    const moderation_status = submitButton.data('moderation-status');
    const shouldShowModal = uuid && moderation_status === 'approved';

    if (shareExperience() && shouldShowModal) {
      event.preventDefault(); // Prevent default button action
      submitModal.show(); // Show the modal if conditions are met
    } else {
      form.submit(); // Submit the form if conditions are not met
    }
  });
  
  
  // When the submit button is clicked in the modal popup, submit the form
  submitFormButton.on('click', function () {
    submitModal.hide();
    form.submit();
  });
  
});



  
  
  
  
  