# AutSPACEs MVP Requirements List

This is a requirement list which can be used to see the most basiic, MVP structure of the platform. 

This file lists every page/page-flow of the AutSPACEs platform which has to be built for the platform to be functional, along with essential components.
Creating a platform prototype which meets all these requirements completes Milestone 2.
This folder also contains a more complete requirements list. Not all requirements for the finished platform will be in the MVP. 
Another essential requirement of the MVP is that it meets GDS accessibility standards, ensuring they are 'baked in' to the earliest designs. 
These are on the repository as separate issues. Completing these issues completes Milestone 3. 

A wireframe mockup of the platform is is available on [Figma](https://www.figma.com/file/HxqTSdeyAUNMualnBV0PET/Autspace-(WIP)?node-id=1%3A111). The MVP pages are those prefaced by "simplified".

*The content is based on preferences and needs emerging from the Autistic/Turing Citizen Science community in discussion sessions and co-working sesssions. 
You can view all the gathered recommendations from the community in the [community-recommendations folder](https://github.com/alan-turing-institute/AutisticaCitizenScience/tree/master/community-recommendations) of the project management reepository.

A complete board of issues is available on the AutSPACEs issues board on [Trello](https://trello.com/b/w2XLjB9g/issues).
Issues will be migrated gradually as the platform progresses, to make sure priority milestones are met and the supporting platform infrastructure is in place.

## Contents

*Platform pages and page-flows: content, community evidence, sources and resources*
- [AutSPACEs MVP Requirements List](#autspaces-mvp-requirements-list)
	- [Contents](#contents)
- [](#)
	- [Platform pages and page-flows: content, community evidence, sources and resources](#platform-pages-and-page-flows-content-community-evidence-sources-and-resources)
		- [Landing Page](#landing-page)
		- [Sign-up flow](#sign-up-flow)
		- [Sign-up flow resources](#sign-up-flow-resources)
		- [Sign-in](#sign-in)
		- [Enter experiences flow](#enter-experiences-flow)
		- [Enter experiences flow: resources](#enter-experiences-flow-resources)
		- [View other experiences page](#view-other-experiences-page)
		- [View own experiences page](#view-own-experiences-page)
		- [Moderation flow](#moderation-flow)
		- [Additional design considerations](#additional-design-considerations)
		- [Additional design considerations: resources](#additional-design-considerations-resources)
 
*General design features* 
- [Additional design considerations](#additional-design-considerations)

# 

## Platform pages and page-flows: content, community evidence, sources and resources

### Landing Page

* Navigation bar
	* Login/sign-out
	* Links to other MVP pages
* Title
* Autistica and ATI logos
* Call to actions
	* sign up
	* enter experience
	* read experiences
* Information on:
	* Basic introduction to project
	* How it works – step by step
	* Main goals – how it will help

### Sign-up flow

* Sign-up Flow
* Sign-in integration with Open Humans: email and password 
* Sign-up questions:
	* Are you autistic?
	* Are you the parent or full time carer of someone autistic? 
	* Are you answering on behalf of someone else?
	* Option to describe other connection to autism (free text box)
* option to prefer not to answer for each question; 
* option to self-describe for each question
* option to sign-up as a moderator 
* easy navigation from confirmation page

### Sign-up flow resources

* Fujitsu have created an integration with the Open Humans signup process which collects email and password for login purposes
* Gov.uk has open source code freely available for individual, well-evidenced and user-tested components that could be used for the sign-up flow

![](https://i.imgur.com/J6LKVL8.png)

![](https://i.imgur.com/v3wxAZH.png)


* Free reusable open source code for typeform-style surveys: https://github.com/ohmyform/ohmyform

### Sign-in

* Take user details and log them into their private account via Open Humans 
* Help for forgotten usernames and passwords/for problems signing in (check Open Humans process?)

### Enter experiences flow

* Asks user to enter experience 
* Asks user what would have made their experience better
* Takes input
	* free text
* Save option
* Change permissions:
	* for researcher
	* share online
* Review option
* Submit option – let’s you skip the suggestions button 
* Confirmation page
* Easy navigation from confirmation page

### Enter experiences flow: resources

* Crisisloggerl https://crisislogger.org has some good basic input options and is open source so we could reuse the code 

![](https://i.imgur.com/hCdwuG1.png)

### View other experiences page

* Search function
* Display experiences which have been given permission to be shared publicly

### View own experiences page

* Private page
* Shows list of experiences submitted or saved by user
* Show status of experiences
* Change sharing permissions for experiences:
		* Publish openly 
		* Only for research
* Delete experiences

### Moderation flow

The moderation process is currently being co-created by the autistic/turing citizen science community. 
In the meantime, it would be useful to have a basic moderation flow:

* Private access to a page for those signed in as a moderator 
	* All experiences with permission to publicly share are automatically feed into this page.
	* User can view an experience and assess it anonymously 
	* User can publish experience if appropriate
	* User can reject experience if appropriate

### Additional design considerations

* autistic people can be overwhelmed by too much information on one page: clear, clean, logical and sequential design. 
* simple words, no metaphors 
* step-by-steps and diagrams
* must be accessible to people with diverse needs (incorporate Chris’ work)
* not too high contrast (too bright a screen can cause pain to some autistic people) (A)
* adapts to different screen sizes well (phone, website, ipad) (AP)
* option to ask real people for help
* must contain voice-to-text and screen reader capabilities  
* make motivation salient
* no word limits/counts (AP)
* no bewildering alerts or prompts that may provoke anxiety
* no time countdowns  
* Help and guidance options

Basic, government digital services guide to designing for autistic users: 

![](https://i.imgur.com/B1vVF7W.png)

### Additional design considerations: resources

Blog by an autistic UX designer: https://uxmastery.com/researching-designing-for-autism/

Jiraslama's Accessibility Menu: https://5wwsja.axshare.com/#g=1&p=1-settings
Screen reader options: https://5wwsja.axshare.com/#g=1&p=0-home-light-screen-reader-option-2
