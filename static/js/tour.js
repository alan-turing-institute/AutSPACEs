import {offset} from 'https://cdn.jsdelivr.net/npm/@floating-ui/dom@1.5.0/+esm';

$(function () {
  // Set a few things up
  $('.dropdown').on('hide.bs.dropdown', function(e) {
    return !!$(this).data('closable');
  }).data('closable', true);

  function setClosable(selector, closable) {
    return $(selector).data('closable', closable);
  }

  function openDropdown(selector) {
    let element = $(selector)
    if (!element.hasClass("show")) {
      element.find('.dropdown-toggle').dropdown('toggle');
    }
    return element;
  }

  // Initialise the tour
  const tour = new Shepherd.Tour({
    useModalOverlay: true,
    defaultStepOptions: {
      scrollTo: {
        behavior: 'smooth',
        block: 'center'
      },
      modalOverlayOpeningPadding: 2,
      modalOverlayOpeningRadius: 16,
      floatingUIOptions: { middleware: [offset({ mainAxis: 20, crossAxis: 0 })] }
    }
  });

  // Add a tour step
  tour.addStep({
    id: 'welcome',
    text: 'Welcome ot the AutSPACEs platform!<br/></br>Would you like to take a tour?',
    buttons: [
      {
        text: 'No thank you',
        action: tour.complete
      },
      {
        text: 'Yes, let\'s go!',
        action: tour.next
      }
    ]
  });

  // Add a tour step
  tour.addStep({
    id: 'explanation',
    text: 'AutSPACEs is all about providing a platform for autistic people to share stories.',
    attachTo: {
      element: '.title-text',
      on: 'bottom'
    },
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Add a tour step
  tour.addStep({
    id: 'code-of-conduct',
    text: 'Before submitting a story, please make sure you read our Code of Conduct carefully. It will only take a few minutes. Once you\'ve read it, press your browser\'s \`back\` button to return to this tour.',
    attachTo: {
      element: '#nav-coc',
      on: 'bottom'
    },
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Add a tour step
  tour.addStep({
    id: 'experiences',
    text: 'A good place to start is by reading others\'s stories to get an idea of what\'s already here. Select the \'Experiences\' item now to open the experiences submienu.',
    attachTo: {
      element: '#nav-experiences',
      on: 'right-start'
    },
    advanceOn: {
      selector: '#experienceDropdownMenuLink',
      event: 'click'
    },
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Add a tour step
  tour.addStep({
    id: 'view',
    text: 'A good place to start is by reading others\'s stories to get an idea of what\'s already here. Select the \'View Stories\' option under the \'Experiences\' item to check them out.',
    attachTo: {
      element: '#nav-experiences-view',
      on: 'right-start',
    },
    when: {
      "before-show": function() {
        setClosable('#nav-experiences', false);
        openDropdown('#nav-experiences');
      },
      "before-hide": function() {
        setClosable('#nav-experiences', true);
      }
    },
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Add a tour step
  tour.addStep({
    id: 'account',
    text: 'Before you submit your first experience, please take the time to fill out your details in the user profile. To open your profile select the Account menu.',
    attachTo: {
      element: '#nav-account',
      on: 'left-start'
    },
    advanceOn: {
      selector: '#accountDropdownMenuLink',
      event: 'click'
    },
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Add a tour step
  tour.addStep({
    id: 'profile',
    text: 'Select the profile menu entry to view and edit your profile.',
    attachTo: {
      element: '#nav-account-profile',
      on: 'left-start',
    },
    when: {
      "before-show": function() {
        setClosable('#nav-account', false);
        openDropdown('#nav-account');
      },
      "before-hide": function() {
        setClosable('#nav-account', true);
      }
    },
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Add a tour step
  tour.addStep({
    id: 'get-involved',
    text: 'AutSPACEs is co-developed with our community. We\'d love for you to be involved too. Whatever your skills we can use them, from research to design to documentation to development to discussion. Find out more here.',
    attachTo: {
      element: '#cta',
      on: 'top'
    },
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Next',
        action: tour.next
      }
    ]
  });

  // Add a tour step
  tour.addStep({
    id: 'finish',
    text: 'That\s it! We hope you find the AutSPACEs platform useful and we look forward to helping share your experiences.',
    buttons: [
      {
        text: 'Back',
        action: tour.back
      },
      {
        text: 'Finish',
        action: tour.complete
      }
    ]
  });

  // Start the fans please!
  tour.start();
});


