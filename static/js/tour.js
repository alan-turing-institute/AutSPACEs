$(function () {
  // Set a few things up
  function openDropdown(selector) {
    let element = $(selector)
    if (!element.hasClass("show")) {
      element.find('.dropdown-toggle').dropdown('toggle');
    }
    return element;
  }

  function closeDropdown(selector) {
    let element = $(selector)
    if (element.hasClass("show")) {
      element.find('.dropdown-toggle').dropdown('toggle');
    }
    return element;
  }

  // Set up the steps
  const steps = [
    {
      content: "Welcome ot the AutSPACEs platform!<br/></br>Please take a few minutes to go through our introductory tour.",
      title: "Welcome",
      target: undefined,
      order: 0,
      group: "main"
    },
    {
      content: "AutSPACEs is all about providing a platform for autistic people to share stories.",
      title: "AutSPACEs",
      target: ".title-text",
      order: 1,
      group: "main"
    },
    {
      content: "Before submitting a story, please make sure you read our Code of Conduct carefully. It will only take a few minutes. Once you\'ve read it, press your browser\'s \`back\` button to return to this tour.",
      title: "Code of conduct",
      target: "#nav-coc",
      order: 2,
      group: "main"
    },
    {
      content: "A good place to start is by reading others\'s stories to get an idea of what\'s already here. Select the \'Experiences\' item now to open the experiences submienu.",
      title: "Experiences",
      target: "#nav-experiences",
      order: 3,
      group: "main"
    },
    {
      content: "A good place to start is by reading others\'s stories to get an idea of what\'s already here. Select the \'View Stories\' option under the \'Experiences\' item to check them out.",
      title: "View",
      target: "#nav-experiences-view",
      order: 4,
      group: "main",
      beforeEnter: async () => {
        return new Promise(async (resolve) => {
          openDropdown('#nav-experiences');
          return resolve(true);
        })
      },
      beforeLeave: async () => {
        return new Promise(async (resolve) => {
          closeDropdown('#nav-experiences');
          return resolve(true);
        })
      }
    },
    {
      content: "Before you submit your first experience, please take the time to fill out your details in the user profile. To open your profile select the Account menu.",
      title: "Account",
      target: "#nav-account",
      order: 5,
      group: "main"
    },
    {
      content: "Select the profile menu entry to view and edit your profile.",
      title: "Profile",
      target: "#nav-account-profile",
      order: 6,
      group: "main",
      beforeEnter: async () => {
        return new Promise(async (resolve) => {
          openDropdown('#nav-account');
          return resolve(true);
        })
      },
      beforeLeave: async () => {
        return new Promise(async (resolve) => {
          closeDropdown('#nav-account');
          return resolve(true);
        })
      }
    },
    {
      content: "AutSPACEs is co-developed with our community. We\'d love for you to be involved too. Whatever your skills we can use them, from research to design to documentation to development to discussion. Find out more here.",
      title: "Get involved",
      target: "#cta",
      order: 7,
      group: "main"
    },
    {
      content: "That\s it! We hope you find the AutSPACEs platform useful and we look forward to helping share your experiences.",
      title: "Finish",
      target: undefined,
      order: 8,
      group: "main"
    },
  ];

  // Initialise the tour
  const tg =  new tourguide.TourGuideClient({
    steps: steps,
  });

  // Ensure the dialog is above the backdrop
  tg.setOptions({
    dialogZ: 1002
  });

  tg.start();

  // Bootstrap places its menus at z-index 1000, the backdrop should be above this
  tg.backdrop.style.zIndex = "1001";
});
