# AutSPACEs Platform Pages

This file lists every page/page-flow of the platform to be built, along with a list of desired features on each page. 
It also includes some additional features to be used throughout the platform.   

*The content is based on preferences and needs emerging from the Autistic/Turing Citizen Science community in discussion sessions and co-working sesssions. 
A selection of community recommendations which support this list of features are also provided. 

You can view all the gathered recommendations from the community in the [community-recommendations folder](https://github.com/alan-turing-institute/AutisticaCitizenScience/tree/master/community-recommendations) of the project management reepository.

An selection of these features necessary to complete an MVP versoin of the platform is broken down into issues on [Asana](https://app.asana.com/0/1199166684586821/board)

A complete board of issues is available on the AutSPACEs issues board on [Trello](https://trello.com/b/w2XLjB9g/issues).
Issues will be migrated gradually as the platform progresses, to make sure priority milestones are met and the supporting platform infrastructure is in place.

A wireframe mockup of the platform is is available on [Figma](https://www.figma.com/file/HxqTSdeyAUNMualnBV0PET/Autspace-(WIP)?node-id=1%3A111). The MVP pages are those prefaced by "simplified".

## Contents

*Platform pages and page-flows: content, community evidence, sources and resources*
- [Landing Page](#landing-page)
- [Sign-up flow](#sign-up-flow)
- [Sign-in](#sign-in)
- [Enter experiences flow](#enter-experiences-flow)
- [View other experiences page](#view-other-experiences=page)
- [View own experiences page](#view-own-experiences-page)
- [Moderation flow](#moderation-flow)
- [Settings page](#settings-page)
- [About page](#about-page)
- [Crisis support page](#crisis-support-page)
 
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
	* fInd out more
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

### Enter expeeriences flow: community recommendations

**Have different input options**
* (A g): “we want to make it as accessible to as wide a scope of the autistic community as we can”
* (A d): “accommodate as many different preferences and styles for providing input within the realms of what’s actually achievable”
* (A g): “…accommodate as many different preferences and styles for providing input within the realms of what’s actually achievable…some people would prefer the free text option…but others would like to be guided down a more structured process”
* Free text
* **No word limit** (A P d): “please don’t put a word limit, and especially not seeing it count down, because it’s very horrible
* Structured input
* (A d): **split the question up**: “Where were you? What time was it? What happened? What effect did it have? and What would you like instead?
* (A P d): “you could give options for options, so you could say, for example, ‘would you like a template?’”
* (A d): split the question up: “Where were you? What time was it? What happened? What effect did it have? and What would you like instead?” 
* Record (vid or speak); upload;
* (A d): **Have a non-verbal means of inputting information**
* (A d): “…having the option to…upload photos, or pictures, or voice recordings of people.”
* Upload options
* (A g): upload pictures of situations that were a problem, so that organisations can go onto the platform and easily see what to change, “because visual things can have much more impact than just…a dense script”
* **Have a question about solutions or ideas for improvements/what would have made it better**
* **autistic people want to be part of the solution.** 
* (A d): “…it’s crucial to have a field that can capture…learning and solutions” 
* (A d): there are two important aspects: what can autistic people do to change their environments, and what can autistic people do to protect themselves from their environments. 
* (A g): “if you’re autistic you want to know…[how] are other autistic people with their expertise…dealing with it? Have they got something to solve the problem?”
* (A d): “I want to be able to say and this is what I think would have helped – you know, it may be that it’s not possible to do the thing, you know we can’t probably make the tube quieter very easily, but we do have ideas about what might help and we should be including those”
* **Able to save drafts and input experience after event**
* (R T d): drafts could be saved but would stay private, and would only be accessed by the person writing them
* Other features - Hashtag
* (P A d): highlight that as an option, “because I’m still very used to the hashtag”
* **Tag or hashtag option for people to search for experiences
* Give clear confirmation once experience has been submitted.** 

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

### View other experiences page: community recommendations

**Be able to search**
**Be able to filter out distressing experiences/self-censor**
* (A d): may cause additional stress: “don’t particularly want to be aroused, as it were, by 	reading about things”
8 (A d): include option to moderate out distressing or negative experiences: “if I’m feeling particularly stressed and I’m going to go on a platform, I don’t want to be reading…a lot of what went wrong on your day, I’d rather click on a button that filters to the – what happened, and what went well, and who accommodated you well”
* **Be able to filter autism-only experiences**
	* Desire for an autism first space
	* Desire for relevance
* (A d): “that would be good…if you’re an autistic person who wants someone to relate to…you can always filter it through to see personal perspectives, whilst…parents might be looking for a different thing”
* (A d): “it’s very difficult to make a place welcoming to autistic people when you also have a lot of neurotypical people explaining about autistic people”

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

### View own experiences page: community recommendations

* (P A d): important to deliver on promises: prior experience of being incentivised to use an app (Molehill Mountain) because it promised to give a mood graph, and was frustrated when this wasn’t offered
Data visualisations
* (A d): have graphs linking data
* (A P d): would help to trace causes and correlations based on patterns of occurrences 
* (A P d): “…with the accumulation of data…you begin to see connections in your own life – and that adds value, you know you were talking about increments of value, but increments of value going both ways”
* Be able to share page with others
* (A d): make it something that an autistic person could use with their mentor – help create plans.

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

About Page: community recommendations

(R T d) show videos of people contributing in different ways and maybe for different reasons on the about page – “I’m imagining a vignette…of three different people…who take part for different reasons, with the idea that you should totally see some aspect of yourself across those three”)
**Include lots of useful information**
* Up-to-date with current research and proposals
* Info about individuals involved 
* Info about participatory science and how it wa built
* Refer to other website for crisis management tools, calm, help etc. 
**Make clear not interested in profit**
* (A g): Concerns about commercial use: “[put] a ringfence around potential commercial uses, because this is intelligence which commercial interests might want to get their hands on” 
* (A i): “people might be wary of contributing, because they might think people just want to make money out of my vulnerabilities”
Lots of people prone to information overload – make this clean, and divide into near, clear sections! 
p) What would help?
(A d): “if you were concerned about the welfare of someone… a section if you need advice or if you need help”

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

### Additional design considerations: community recommendations

* (A P d): “that actually matters to me because I… switch between android and iPad, and It’s how I choose to live my life, but it can be annoying when things don’t work out”
* (A d): bring one thing up at a time
* (A d): “just one thing or question or visual per page, and then…press next”
Back-to-top button
* (A d): “the words used, or any writing used” should be “well-spaced out and in a good font that anyone could read - and obviously a screen reader could pick out as well”
* (A d): make a button you can press for help to come up
* (P d): Have a tagline: “this is what we’re looking for, this is what we want from you, and this is what we’re going to do, and don’t be afraid to repeat yourself just literally on every page like, this is what we want, this is what we need from you, this is what we expect from you”
* (A d): “I’m very prone to information overload, so I would want from my point of view this default interface to be as plain and un-distracting as possible…I wouldn’t want something that was busy and distracting, it just needs to be focussed on the content.

Blog by an autistic UX designer: https://uxmastery.com/researching-designing-for-autism/

Jiraslama's Accessibility Menu: https://5wwsja.axshare.com/#g=1&p=1-settings
Screen reader options: https://5wwsja.axshare.com/#g=1&p=0-home-light-screen-reader-option-2
