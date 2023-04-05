document.addEventListener('DOMContentLoaded', function () {
  let form = document.querySelector('.form-context');
  let submitFormButton = document.getElementById('submitForm');
  let viewableCheckbox = document.getElementById('shareOnAutSPACEs');
  
  // Check that event listener is working
  // if (viewableCheckbox) {
  //   viewableCheckbox.addEventListener('change', function () {
  //     console.log('viewableCheckbox checked:', viewableCheckbox.checked);
  //   });
  // }
  
  if (submitFormButton) {
    let submitModal = new bootstrap.Modal(document.getElementById('submitModal'));

    // Check whether Share Experience checkbox is ticked
    let shareExperience = () => {
      return viewableCheckbox.checked;
    };

    let submitButton = document.getElementById('submitBtn');
    if (submitButton) {
      // when submit button is clicked, check if the Share Experience checkbox is ticked,
      // and the story exists (uuid) and has been moderated (approved)
      submitButton.addEventListener('click', (event) => {
        const uuid = submitButton.getAttribute('data-uuid');
        const moderation_status = submitButton.getAttribute('data-moderation-status');
        const shouldShowModal = uuid && moderation_status === 'approved';

        if (shareExperience() && shouldShowModal) {
          event.preventDefault(); // Prevent default button action
          submitModal.show(); // Show the modal if conditions are met
        } else {
          form.submit(); // Submit the form if conditions are not met
        }
      });
    }
    
    // When the submit button is clicked in the modal popup, submit the form
    submitFormButton.addEventListener('click', function () {
      submitModal.hide();
      form.submit();
    });
  }
});



  
  
  
  
  