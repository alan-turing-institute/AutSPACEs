# AutSPACEs Requirements List

This is a requirement list which can be used to see the basic structure of the platform. 

This file lists every page/page-flow of the AutSPACEs platform which has to be built for the platform to be functional, along with a list of desired features on each page. These will eventually be turned into issues on the main repository. For now we are working on a simplified MVP version of the platform.  
It also includes some additional features to be used throughout the platform.  

This list can be used to 

*The content is based on preferences and needs emerging from the Autistic/Turing Citizen Science community in discussion sessions and co-working sesssions. 
You can view all the gathered recommendations from the community in the [community-recommendations folder](https://github.com/alan-turing-institute/AutisticaCitizenScience/tree/master/community-recommendations) of the project management reepository.

A complete board of issues is available on the AutSPACEs issues board on [Trello](https://trello.com/b/w2XLjB9g/issues).
Issues will be migrated gradually as the platform progresses, to make sure priority milestones are met and the supporting platform infrastructure is in place.

A wireframe mockup of the platform is is available on [Figma](https://www.figma.com/file/HxqTSdeyAUNMualnBV0PET/Autspace-(WIP)?node-id=1%3A111). The MVP pages are those prefaced by "simplified".

## Contents

*Platform pages and page-flows: content, community evidence, sources and resources*
- [AutSPACEs Requirements List](#autspaces-requirements-list)
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
		- [Settings page](#settings-page)
		- [About page](#about-page)
		- [Crisis Support Page](#crisis-support-page)
- [](#-1)
		- [Additional design considerations](#additional-design-considerations)
		- [Additional design considerations: resources](#additional-design-considerations-resources)
 
*General design features* 
- [Additional design considerations](#additional-design-considerations)

# 

## Platform pages and page-flows: content, community evidence, sources and resources

### Landing Page

* Navigation bar
	* Login/sign-out
	* Help
	* Links to other pages
	* Accessibility icon
	* Text-to-voice/voice-to-text options
	* Crisis support – we make it clear we don’t provide this but can link to other places
* Title
* Strapline
* Engaging visual imagery or video
* OH, Autistica and ATI logos
* Call to actions
	* sign up
	* enter experience
	* read experiences
	* Find out more
* Information on:
	* Project summary (inc. sensory processing)
	* How it works – step by step
	* Main goals – how it will help
	* Autistic-first space with autistic community
	* Reassurance about data: anonymous, you choose, no selling for profit
* Get in touch
* Give feedback

### Sign-up flow

* Sign-up Flow
* Sign-in integration with Open Humans: email and password 
* Explanation of why they’re going to Open Humans 
* Sign-up questions:
	* Are you autistic?
	* Are you the parent or full time carer of someone autistic? 
	* Are you answering on behalf of someone else?
	* Option to describe other connection to autism (free text box)
* option to sign up straight away or answer more questions
* Additional demographic questions (e.g.): 
	* *Ethnicity	
	* *Education	
	* *Income bracket	
	* *Gender identification	
	* *Sexuality
* option to prefer not to answer for each question; 
* option to self-describe for each question
* Sign up confirmation
* easy navigation from confirmation page
* Option to create a shared account?

### Sign-up flow resources

* Fujitsu have created an integration with the Open Humans signup process which collects email and password for login purposes
* Gov.uk has open source code freely available for individual, well-evidenced and user-tested components that could be used for the sign-up flow

![](https://i.imgur.com/J6LKVL8.png)

![](https://i.imgur.com/v3wxAZH.png)


* Free reusable open source code for typeform-style surveys: https://github.com/ohmyform/ohmyform

### Sign-in

* Take user details and log them into their private account via Open Humans 
* Explanation of why signing up via Open Humans  (drop down?)
* Help for forgotten usernames and passwords/for problems signing in (check Open Humans process?)

### Enter experiences flow

* Asks user to enter experience 
* Asks user what would have made their experience better
* Takes input
	* free text
	* structured input
	* record videos
	* record voice
* Option to upload extra files or other as supplement
* Save option
* Change permissions:
	* for researcher
	* share online
	* share online only with autistic people
* Add tags option
* Review option
* Submit option – let’s you skip the suggestions button
	* consent (radio) button – second consent that appears if you’ve uploaded a video or a voice – research suggestion if not okay with consent statement 
* Suggestions button – continues to what would have been better page
* Confirmation page
* Easy navigation from confirmation page

### Enter experiences flow: resources

* Crisisloggerl https://crisislogger.org has some good basic input options and is open source so we could reuse the code 

![](https://i.imgur.com/hCdwuG1.png)

### View other experiences page

* Search function
* Filter options
	* Autistic-only
	* Child-friendly (tag for adult content)
	* No distressing experiences (tag for sensitive content) 
* See different kinds of input option
	* All, or selection of:
		* Text
		* Videos
		* Sound recordings
		* Images
* Display experiences
* Option to flag for moderation
* Sort by options
	* Date
	* Relevance
* Option to save to personal page

### View own experiences page

* Private page
* Shows list of experiences submitted or saved by user
* Show status of experiences
* Shows date or time stamp of when experience submitted
* View full experiences
* Edit experiences
	* Add tags
* Change sharing permissions for experiences:
		* Publish openly 
		* Only for research
		* Only for autistic people
* Delete experiences
* Export button - share page with someone else or email to self 
* Allow someone else to edit/co-create page – toggle consent 
* View and edit tags created by machine learning algorithm as well as own 

### Moderation flow

The moderation process is currently being co-created by the autistic/turing citizen science community. 
In the meantime, it would be useful to have a basic moderation flow:

* Sign-in flow adapted for moderators
* With sign access to a moderation page:
	* All experiences with permission to publicly share are automatically fed into this page.
	* User can view an experience and assess it anonymously 
	* User can publish experience if appropriate
	* User can reject experience if appropriate 

### Settings page

* View profile
* Change signup information answers
* Customise platform
	* colour palette 
	* contrast, 
	* text size
	* default input mode
	* default view modes
* Accessibility settings
* Help with platform
* Need other help
	* Link to different websites which can offer advice on:
		* medical issues
		* diagnostic issues
		* anxiety issues
		* general autism information (Autistica)
* Get in touch
* Logout

N.B. jiraslama has already done a lot of design work on this which is available via. axshare 

### About page

* Project news and updates
* Testimonials 
* How it works
* Our main goals * Overview of project
* Sensory processing info * About our community
	* Autistic citizen scientists
	* Researchers
	* Organisations
		* Alan Turing Institute
		* Autistica
		* Open Humans* How AutSPACE was created (participatory science)* Code of Conduct
* Guidelines on sharing on behalf of others* How we moderate – simple diagram* What happens to your data – simple diagram, privacy notice and GDPR
* Open Source (and link to GitHub repositories)
* Get in touch
* Give feedback
* Newsletter sign up
* Resources/links to external resources for concerns, e.g. welfare concerns  

### Crisis Support Page
* Link to different websites which can offer advice on:
	* medical issues
	* diagnostic issues
	* anxiety issues
	* general autism information (Autistica)

# 

*General design features* 

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
