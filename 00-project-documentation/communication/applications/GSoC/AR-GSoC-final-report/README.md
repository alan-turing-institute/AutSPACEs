
GSoC Work Report - Building a Working Prototype for the AutSPACEs website
===

## Table of Contents
* <a href="#about-me">About Me</a>  
* <a href="#overview">Overview</a>
* <a href="#details-on-pages-developed">Details on Pages Developed</a>
* <a href="#major-pull-requests">Major Pull Requests</a>
* <a href="#issues-createddetails-added">Issues Created/Details Added</a>
* <a href="#reviewed-prs">Reviewed PRs</a>
* <a href="#reflections">Reflections</a>
* <a href="#future-work">Future Work</a>
* <a href="#conclusion">Conclusion</a>


## About Me
Hi! I'm Anoushka Ramesh, a Computer Science undergraduate from India studying at Amrita Vishwa Vidyapeetham, Amritapuri. During Google Summer of Code 2021, I've been an active contributor to AutSPACEs where I worked on building a working prototype of their website. 


## Overview
AutSPACEs is a participatory, citizen science project aiming to develop a platform which gathers the experiences of autistic people and how their sensory processes are impacted whilst navigating public environments. This will create a qualitative dataset that serves two purposes:

* Contribute to making the world more inclusive of autistic people by urging policy-makers to make changes based on evidence and recommendations from a large number of lived experiences.
* Educate non-autistic people on how they can be better allies for autistic individuals and destigmatize autism in our society.

AutSPACEs is entirely open source and involves a diverse community of autistic collaborators, platform developers and project managers. It focuses on the reproducibility of data and aids researchers to progress in the field of autism. 

This project aims to build and implement a working prototype of the AutSPACEs website in collaboration with the autistic community. The approach to this project would be to:

* Solve issues from milestones [2](https://github.com/alan-turing-institute/AutSPACEs/milestone/2?closed=1) and [3](https://github.com/alan-turing-institute/AutSPACEs/milestone/7) which aim to increase the accessibility of the website and make it into a minimum viable product.
* Test and review PRs to ensure that they meet their purpose.
* Make appropriate documentation for the code.
* Send the final working prototype to the autistic community for feedback and make additonal issues based on it.

### Changes in the Project Plans
* [Milestone 2](https://github.com/alan-turing-institute/AutSPACEs/milestone/2?closed=1) became the primary focus of the project i.e. making an MVP of the website and delivering it to the autistic community for feedback.
* [Milestone 3](https://github.com/alan-turing-institute/AutSPACEs/milestone/7) changed to integrating the website with Open Humans - a backend database that stores all user experiences.
* Implementing accessibility of the website got shifted to [Milestone 4](https://github.com/alan-turing-institute/AutSPACEs/milestone/5).


## Details on pages developed
The first priority of the project was to develop the static pages for the website with reference to the simplified wireframes previously created. 

### Landing Page - Issue [#15](https://github.com/alan-turing-institute/AutSPACEs/issues/15)
This is the landing page I developed with reference to its [simplified wireframe](https://www.figma.com/file/HxqTSdeyAUNMualnBV0PET/Autspace-(WIP)?node-id=172%3A641).

![Landing Page](https://i.imgur.com/KO8nMK1.png)

The navbar contains:
* **Home** - This navigates the user to the landing page if they're logged out and to the home page if they're logged in.
* **View Experiences** - This navigates the user to the page where all the public experiences are displayed.

The **sign in** button directs the user to the Open Humans authorisation page and is linked to `OpenHumansMember.get_auth_url()`

The **sign up** button enables the user to create an account on AutSPACEs after filling out a questionnaire to check whether they're autistic or not. They will then be directed to Open Humans where they can create an account to authorize the AutSPACEs project to use their data.
    

### Share Experiences Page - Issue [#16](https://github.com/alan-turing-institute/AutSPACEs/issues/16)
This is the share experiences page I developed with reference to the first frame of the [simplified wireframe](https://www.figma.com/file/HxqTSdeyAUNMualnBV0PET/Autspace-(WIP)?node-id=128%3A0).
![Share Experiences](https://i.imgur.com/U0uA7Tx.png)

When the user is signed in, this is the extended navbar that they can see which contains:
* **Home** - This navigates the user to the landing page if they're logged out and to the home page if they're logged in.
* **View Experiences** - This navigates the user to the page where all the public experiences are displayed.
* **Moderate Experiences** - This is only visible to moderators where they can approve or decline experiences according to the AutSPACEs Code of Conduct.
* **Share Experiences** - This navigates the user to a page where they can share their experiences and decide to send it for research or make it visible to the public.
* **My Stories** - This navigates the user to a page where they can view their personal experiences and view the moderation status on each experience.
* **Logout** - The user logs out of their account.

On submitting their experience, the site generates a JSON file which is stored in the Open Humans database for researchers and moderators to use.

Below is an example of one of the Open Humans database JSON files:
``` gherkin=
{
 "text": "*Whenever I go on public transport, especially at peak times, it can be quite challenging and it is very off-putting,I would like to avoid it completely to travel during peak times.*",
 "wish_different": "*If I could change one thing about the use of public transport I go on, it would probably be a higher frequency of trains, maybe every 8 or 10 minutes, so there are not so many people that go on each train.*",
 "timestamp": "2021-06-06 18:58:22.958543"
}

```

## Major Pull Requests
Below is a list of all major pull requests that I created that were merged into the code:  
[#114](https://github.com/alan-turing-institute/AutSPACEs/pull/114) - **Add Landing Page**  
[#115](https://github.com/alan-turing-institute/AutSPACEs/pull/115) - **Add Share Experiences Page**  
[#143](https://github.com/alan-turing-institute/AutSPACEs/pull/143) - **Navigation: Share Experiences**  
[#146](https://github.com/alan-turing-institute/AutSPACEs/pull/146) - **Navigation: Home Page**  
[#147](https://github.com/alan-turing-institute/AutSPACEs/pull/147) - **Navigation: View Experiences**  
[#151](https://github.com/alan-turing-institute/AutSPACEs/pull/151) - **Navigation: View Experiences (Revert Changes)**

### Other PRs
[#116](https://github.com/alan-turing-institute/AutSPACEs/pull/116) - **Adding Experiences Page**   
I redirected the page to the `list_public_experiences` view as initially the old pages were getting rendered instead of the newly created ones.  

[#117](https://github.com/alan-turing-institute/AutSPACEs/pull/117) - **Adding Moderation Page**  
I redirected the page to the `list_moderate_public_experiences` view because the new pages weren't getting rendered on the screen.

### Commits
Here's the link to my list of commits - https://github.com/alan-turing-institute/AutSPACEs/commits?author=anoura12&before=05f67b39a355c4796c2e174152fe98e5d157b904+35

## Issues Created/Details Added
These are the issues I created and added details to for Milestone 2 and Milestone 3 after learning how to scope a task.

[#153](https://github.com/alan-turing-institute/AutSPACEs/issues/153) - **Render a User's Personal Experiences in the `My Stories` Page**   
[#119](https://github.com/alan-turing-institute/AutSPACEs/issues/119) - **Integrate all pages together to produce final MVP**

## Reviewed PRs
This is one of the skills I developed with the project where I liased with other developers to improve their PRs and provide feedback on what changes they could make.

[#116](https://github.com/alan-turing-institute/AutSPACEs/pull/116) - **Adding Experiences Page**  
[#117](https://github.com/alan-turing-institute/AutSPACEs/pull/117) - **Adding Moderation Page**

## Reflections
### Community Bonding to First Evaluation
* I got introduced to the team in my very first AutSPACEs community call where I understood the overall workflow of the project and how new contributors can solve issues. 
* The project had a lot of elements which seemed overwhelming at first. So, I used Slack at my disposal and went around asking various questions to not only my mentors but also other people related to the project.
* After talking to the lead developer, I took up my [first issue](https://github.com/alan-turing-institute/AutSPACEs/issues/15) which was creating the landing page with Bootstrap according to simplified wireframes designed earlier.
* I took up another [issue](https://github.com/alan-turing-institute/AutSPACEs/issues/16) related to creating the Share Experiences page.
* Every alternate week, we have our AutSPACEs community calls where I co-facilitated the platform development breakout room with Sowmya who was another contributor. I gave updates on the project to the team and clarified their doubts and questions regarding the source code and project repository.
* During the development co-working sessions and community calls, I helped other contributors with their issues and the website setup with Docker. I also briefly explained how the backend database(Open Humans) worked with the site.
* After all the pages were done, I set up the MVP and presented it to the entire AutSPACEs community during one of our community calls where I got feedback on how we could further improve upon the site.

### First Evaluation to Second Evaluation
* During this period, Sowmya's internship came to an end. From then onwards, I facilitated the entire development breakout room and brought about effective discussions on how to progress AutSPACEs through Milestone 2.
* I took up three issues related to the [navigation](https://hackmd.io/gKc4yWQgTh2eGf8oCbm7bA?both#Major-Pull-Requests) of the website and sent PRs which got merged.
* We finally completed Milestone 2 after my final [PR](https://github.com/alan-turing-institute/AutSPACEs/pull/151) was merged.
* We had key discussions on the integration of Open Humans and how to proceed with Milestone 3 in our community calls.
* I scoped and created an issue for Milestone 3 about rendering a user’s personal experiences on the my_stories page after learning about project scoping. 

Here are my status updates for each week - [Weekly Status Updates](https://github.com/alan-turing-institute/AutisticaCitizenScience/tree/master/applications/GSoC/AR-weekly-updates)

### Lessons Learnt
I had a wonderful experience with this project and learned a lot  in these 3 months of GSoC. Here are some of the main skills I acquired during this time:

* **Git** - Prior to my GSoC journey, my knowledge of GitHub was basic, however, due to the needs of the programme, I developed key understanding and practical knowledge of using Github to ensure efficient project management, task completion and reproducibility. Learning how to resolve merge conflicts, cherry picking, contributing to another branch, splitting a PR into two separate ones are just some of the Git skills I learnt both independently and from others. I also learnt how to make concise commit messages rather than clubbing all the changes in one commit.
* **Project Scoping** - This is one of the most important skills I acquired in the project. This included creating an abstract list of requirements for a particular page in the site based on a page’s different states, what data it receives and what output it displays. Getting the correct level of technical detail is a key skill that I developed to ensure the tasks was accurately scoped. This was a personal goal of mine to achieve and therefore I'm glad to have had the exposure and guidance from other contributors on the project.
* **Effective Communication** - My ability to effectively communicate with other contributors improved significantly over these three months. I actively sought and took on opportunities during my meetings and community calls to work on these skills such as explaining a particular concept of the project, helping a contributor with their issue or presenting my work to the community. I ensured my communication techniques accurately portrayed the audience and their needs. I also developed the ability to ask precise, effective and thought-provoking questions.
* **Reviewing Pull Requests** - I reviewed other PRs and gave concise feedback on what changes could be incorporated. 
* **Guiding New Contributors** - I helped the new new contributors take up issues in the project repository and came on calls with them individually to address their queries.

## Future Work
Currently, the project stands at Milestone 3 which involves the integration of the site with Open Humans. I will be continuing with the project to ensure that this integral stage of the website is complete. I will also be helping Kirstie and Lotty by aiding other contributors with their work and progressing the website through different milestones.


## Conclusion
I had a wonderful experience with AutSPACEs and the autistic community during these three months. The community was very welcoming when I first joined AutSPACEs. I really loved the collaborative atmosphere in the community calls where I was free to express my ideas and interests in the project.

My mentors, Kirstie Whitaker and Charlotte Coupat, have constantly guided me throughout the project and helped me grow as a person. Before AutSPACEs, my knowledge of computer science was rather limited to academics. I was unknown to the world of open source and how organisations functioned in the real world. This project opened my eyes to the various possibilties open source has to offer. It gave me the opportunity to apply my existing knowledge to help create a better world for autistic individuals. I also understood how an organisation functions and recieved hands-on experience while working with project managers and platform developers.

I am highly grateful to the project’s lead developer, James Kim, for teaching me good coding practices, Git skills and project scoping. As I kept contributing to the code and solving issues, my initial apprehension in sending a PR in hopes of not breaking the site, disappeared. I also learnt new principles like DRY(Don't Repeat Yourself) and creating concise commit messages.

All in all, I thoroughly enjoyed my time here and would recommend AutSPACEs to anyone seeking for a good learning experience and access to one of the best communities I have ever seen.






















