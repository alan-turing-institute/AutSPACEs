# Building A Working Prototype of the AutSPACEs Website

## Contact Details:
Full Name - Anoushka Ramesh  
Email Address - anoushkaramesh21@gmail.com  
Location - Maharashtra, India  
Institution - Amrita Vishwa Vidyapeetham, Amritapuri  
Portfolio - [https://anoura12.github.io/](https://anoura12.github.io/)  
GitHub - [https://github.com/anoura12](https://github.com/anoura12)  
Hangouts ID - anoushkaramesh21@gmail.com  

## Project Abstract:
The project aims to build and implement a working prototype of the AutSPACEs website in collaboration with the autistic community.  
  
AutSPACEs is a citizen science platform that captures an autistic person’s experiences with sensory processing differences and challenges and generates a qualitative dataset. This data serves two purposes:
1. Contribute to making the world more inclusive of autistic people by urging policy-makers to make changes based on evidence and recommendations from
a large number of lived experiences.
2. Educate non-autistic people on how they can be better allies for autistic individuals and destigmatize autism in our society.   


There are two milestones for the website previously defined by the web developers. They include several issues that focus on increasing the accessibility of the website and making it into a minimum viable product. **My approach is to solve issues from these milestones, test and review the pull requests, create documentation for the code and finally deliver the prototype to the autistic community for feedback.**

*The top priorities for this proposal are:*
* To build the prototype by solving issues from milestone 2 and milestone 3 on the
AutSPACEs repository where:  
  * Milestone 2 is creating a minimum viable product (MVP) of the platform
with required pages and features [[1]](https://github.com/alan-turing-institute/AutSPACEs/milestone/2)
  * Milestone 3 is increasing the accessibility of the platform [[2]](https://github.com/alan-turing-institute/AutSPACEs/milestone/3)
* Testing and improving the prototype based on feedback from the autistic
community.

## Project in Detail:
This is a basic overview of how the user will go through the website-
![website flow](https://user-images.githubusercontent.com/73518403/114704760-99e21680-9d44-11eb-9bda-18948fab0e2b.png)  


I would be progressing the prototype through milestones 2 and 3 by solving these four main issues as a starting point:

### Issue #[32](https://github.com/alan-turing-institute/AutSPACEs/issues/32) - MVP - Basic Accessibility
This issue is about establishing some basic accessibility to the website by ensuring that it meets the official WCAG (Web Content Accessibility Guidelines) guidelines.  
To implement this, a web accessibility tool called [aXe](https://www.deque.com/axe/) can be used. It’s a Chrome extension that easily detects accessibility issues on your website.  
![Untitled Diagram](https://user-images.githubusercontent.com/73518403/114705300-360c1d80-9d45-11eb-92f6-fc004872c354.png)  

*What needs to be done?*
* Check if it meets the Autism accessibility guidelines.
* Check if it meets the basic checklist which is:  

| Checklist Question | Possible Solution |
| ------------------ | ----------------- |
| Is the colour contrast of text readable by people with low vision? | *aXe shouldn’t detect any colour contrast issues* |
| Is the colour alone used to convey important information? | *View the page in grayscale to see whether the information is still conveyed correctly* |
| Do all images have alternative text? | *aXe would be able to detect issues related to alt text if any* |
| Does the alternative text make sense? | *See if the purpose of the image is met if all images are replaced with the alt text* |
| If the image is a link, does the alternative text clearly identify the link destination? | Replace the image with the alt text and see if it still makes sense* |
| Are all CSS background images either pure decoration or have alternative text? | *See if page is still informative if all images are removed* |
| Is any text embedded in images? | *See if there are any images used to present text* |
| Does the tab order make sense? | *Check if order is sequential and makes sense when tabbed through the page* |
| Can you always see where the keyboard focus is? | *Check if element in focus is properly highlighted* |
| Does the user have full access to the page using the keyboard alone? | *All functionality should be covered with the keyboard* |
| Do all form fields have proper labels? | *aXe should not find any ambiguity in labels* |
| Is all content and functionality available to a screen reader? | *See whether all content and features of the page is covered. Try using the screen reader with your eyes closed* |  

### Issue #[20](https://github.com/alan-turing-institute/AutSPACEs/issues/20) - Place-Holder Moderation Page
This issue involves creating a place-holder moderation page.

*What needs to be done?*
* Make sure the page is private to signed-in moderators.
* If an experience is submitted with ‘shared publicly’ permissions, it should be automatically displayed on the moderator page.
* Option to approve or deny publication.
* If approved, story needs to be displayed on the "view experiences" page.
* Changes to story status; pending, approved and published, blocked should be updated on the "my stories" page for relevant user.  

I will work closely with community members Susanna Fantoni and James Scott to make sure that this page is developed with the needs of the moderators in mind.  

### Issue #[73](https://github.com/alan-turing-institute/AutSPACEs/issues/73) - Create a glossary for the website
In order to make the platform more inclusive, it would help to include a glossary of technical terms, as well as a glossary of appropriate, inclusive language relating to autism and intersectional issues.  

*What needs to be done?*
* Either compile into glossary in markdown and add to appropriate place in the repository, or add glossary of terms to each page of the website.
* List words that are technical and which may be confusing to non-technical people throughout the repository and website.
* List exclusionary language and appropriate language.

I will work closely with community manager Lotty Coupat to make sure that this effort is harmonised across the project in the GitHub documentation and linked from the code of conduct and regular meetup welcome notes.

### Issue #[60](https://github.com/alan-turing-institute/AutSPACEs/issues/60) - Navigate using only a keyboard
The issue requires us to do some checks to see how easy it is for users to navigate the site using only a keyboard. The main keys used to navigate the screen are the ‘spacebar’, ‘Tab’, ‘Enter’ and ‘Esc’ keys. ‘Tab’ lets you jump between page elements.‘Enter’ and ‘Esc’ let you interact with and dismiss those page elements. The spacebar activates buttons, checkboxes and radio buttons.

What needs to be done?
* Check you can tell where you are on the page.
* Check you do not get stuck when navigating through content.
* Check forms are still usable without a mouse.
* Check users can skip to the main content on a page.
* Check the order makes sense when tabbing.
* Check nothing unexpected happens when tabbing through a page.  

## Project Deliverables
* Connect the website to Open Humans - site responsible for the backend
database
* Solve issues from milestones 2 and 3 which are -
  * Issue #32 - MVP - Basic Accessibility [[3]](https://github.com/alan-turing-institute/AutSPACEs/issues/32)
  * Issue #20 - Place-holder moderation page [[4]](https://github.com/alan-turing-institute/AutSPACEs/issues/20)
  * Issue #73 - Create a glossary for the website [[5]](https://github.com/alan-turing-institute/AutSPACEs/issues/73)
  * Issue #60 - Navigating using only a keyboard [[6]](https://github.com/alan-turing-institute/AutSPACEs/issues/60)
* Review PRs and test them in the website to see if they meet the desired
outcomes
* Add documentation to the code
* Test the prototype in collaboration with the autistic community
* Raise new issues based on the feedback from the community

## Project Timeline  

| Week | Tasks |
| --- | --- |
| Community Bonding (May 17 - June 7) | <ul><li>Get to know the AutSPACEs community and introduce myself there.</li><li>Meet the core development team to ensure that everyone is working towards the same goal.</li><li>Explore Open Humans to get an understanding on the backend database in order to integrate it to the frontend.</li></ul> | 
| **(June 7-August 16)** | <div align="center">**Coding Begins**</div> |
| Week 1 (June 7- June 13) | <ul><li>Build the existing prototype locally.</li><li>Understand existing features and elements of the website.</li></ul> |
| Week 2 (June 14-June 20) | <ul><li>Solve issue #32.</li><li>Review issues in milestone 2.</li></ul> |
| Week 3 (June 21-June 27) | <ul><li>Test the PRs on the website to check if it meets desired outcomes.</li><li>Add required documentation for said PR once merged.</li><li>College exams week so work here may be shared earlier or later as needed.</li></ul> |
| Week 4 (June 28-July 4) | <ul><li>Start solving issue #20.</li><li>Discuss the UI and working of the moderation page with community members.</li></ul> |
| Week 5 (July 5-July 11) | <ul><li>Work on Phase I report.</li><li>Buffer of 4 days to compensate for any work that I may have missed out.</li></ul> |
| **(July 12-July 16)** | <div align="center">**Phase I Evaluation**</div> |
| Week 6 (July 17-July 23) | <ul><li>Work on issues in milestone 3 by starting with issue #60.</li><li>Review PRs in milestone 3.</li></ul> |
| Week 7 (July 24-July 30) | <ul><li>Work on issue #73.</li><li>Buffer of 1-2 days to complete any remaining components of the prototype and make it ready to present to other people.</li></ul> |
| Week 8 (July 31-August 6) | <ul><li>Present the working prototype to the community to test it.</li><li>Write any issues after community feedback.</li></ul> |
| Week 9 (August 7-August 13) | <ul><li>Close out any open pull requests.</li><li>Review my entire work before writing a report.</li><li>Work on the most serious issues reported from the community.</li></ul> |
| Final Submission Period (August 14-August 23) | <ul><li>Continue working on any major issues as stated previously.</li><li>Work on the final report.</li><li>Buffer of 3 days to complete any remaining work.</li><li>Write about future contributions and how we can develop the platform further to better capture an autistic user’s experiences.</li></ul> |
| **(August 16-August 23)** | <div align="center">**Final Submission**</div> |  

**Stretch Goals:**  
I would be solving the following issues if time permits:  
1. Issue #71 - Add Autistica and Turing logos
2. Issue #69 - Brief explanation of explore stories page
3. Issue #47 - Check if images have proper descriptions  

## Plan for communication with mentors:
I would be giving regular status updates on Slack everyday updating my mentors about my work and progress. I will also attend weekly calls on Zoom with Lotty (community manager) and Kirstie (project lead), and regular calls with James Kim (lead developer) as needed. I will attend the fortnightly community meet-ups to build connections to the autistic contributors.  

## About Me
* **Why do you want to do this project?**  
This project combines my interest in design with a sense of purpose towards the community. I’ve always liked to draw and design and I do have good skills in web
development. This particular project gives me a good opportunity to create an accessible design specifically for autistic people which not only puts my skills to
the test but also gives me a sense of fulfillment.  
I have a friend with autism and have met some other autistic people in the past. I understand how small changes in their environment can trigger them and
frustrate them significantly. Hence, I realise that AutSPACEs can potentially improve the lives of so many autistic people and this project gives me a chance
to do just that.  

* **Projects I’ve worked on in the past**  
  * I have built my own Open Humans page which can successfully upload
user data. [[7]](http://3.142.144.255:8000/todo/)
  * To-Do App - This is a to-do application built with Django - the same
framework on which AutSPACEs is built.[[8]](https://github.com/anoura12/todo-app)

* **Is this the only project I’m working on?**  
Yes, this is the only project and INCF is the only organisation I’d be applying to. I have engaged with the project team through the Open Humans slack workspace
and lead mentor Kirstie Whitaker has provided 1:1 support in the development of this application.  

* **Working time and commitments**  
I would be utilising time after college to get this work done. On an average, I would be spending around 40-45 hours per week.  

* **Other plans for the summer**  
I would be having my end semester examinations from June 24 th . They will last for about a week and a half but I will be able to cover up any pending work during
the breaks I get between the exams or on the weekends. I will also put in extra work before and after my exams to make up for any backlogs.

* **Past experience**  
I am a university freshman currently pursuing a degree in Computer Science and Engineering. I am experienced with HTML, CSS, Python, Django and React. I am
also familiar with Git. I have made my own blog backend using Django.  
Currently, I am a part of a student-run open source club called amFOSS [[9]](https://amfoss.in/) where we contribute to open source software and learn a variety of technical and
non-technical skills.  
For further information, please feel free to get in touch via any of the means given in this proposal, or refer to my CV [[10]](https://anoura12.github.io/docs/Anoushka_Resume.pdf).  

## Appendix
[1] [https://github.com/alan-turing-institute/AutSPACEs/milestone/2](https://github.com/alan-turing-institute/AutSPACEs/milestone/2)  
[2] [https://github.com/alan-turing-institute/AutSPACEs/milestone/3](https://github.com/alan-turing-institute/AutSPACEs/milestone/3)  
[3] [https://github.com/alan-turing-institute/AutSPACEs/issues/32](https://github.com/alan-turing-institute/AutSPACEs/issues/32)  
[4] [https://github.com/alan-turing-institute/AutSPACEs/issues/73](https://github.com/alan-turing-institute/AutSPACEs/issues/20)  
[5] [https://github.com/alan-turing-institute/AutSPACEs/issues/20](https://github.com/alan-turing-institute/AutSPACEs/issues/73)  
[6] [https://github.com/alan-turing-institute/AutSPACEs/issues/60](https://github.com/alan-turing-institute/AutSPACEs/issues/60)  
[7] [https://gsocautspaces.herokuapp.com/](https://gsocautspaces.herokuapp.com/)  
[8] Link to repository - [https://github.com/anoura12/todo-app](https://github.com/anoura12/todo-app)  
    Link to app - [http://3.142.144.255:8000/todo/](http://3.142.144.255:8000/todo/)  
[9] [https://amfoss.in/](https://amfoss.in/)  
[10] [https://anoura12.github.io/docs/Anoushka_Resume.pdf](https://anoura12.github.io/docs/Anoushka_Resume.pdf)  















