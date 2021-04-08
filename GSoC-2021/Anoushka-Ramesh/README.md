# GSoC2021 Expression of Interest: Anoushka Ramesh
Email - anoushkaramesh21@gmail.com

## Assessment Step 1
Website - [https://gsocautspaces.herokuapp.com](https://gsocautspaces.herokuapp.com)

Activity page - [https://www.openhumans.org/activity/project-autspaces/#activity-panel-data](https://www.openhumans.org/activity/project-autspaces/#activity-panel-data)

UserData JSON file - 
![Screenshot from 2021-03-29 22-59-34](https://user-images.githubusercontent.com/73518403/112876035-a0388780-90e2-11eb-8e98-fd2a71a55d11.png)

## Assessment Step 2
[Todo-App](https://github.com/anoura12/todo-app) - A basic Django todo application where you can create and update tasks.
I've used HTML and Tailwind CSS for the frontend.
You can click [here](http://3.142.144.255:8000/todo/) to view the app

## Assessment Step 3
The development requirement that I would like to work on is the additional design requirements for the website.

Most of the world’s autistic population uses the web for their personal needs, and the number keeps increasing every year. Most websites contain bright colors, glary screens, ambiguous symbols, and cluttered layouts that overwhelm autistic users because this triggers their sensory processing sensitivities. Hence, I would like to create a simple but effective user interface that makes it easier for them to navigate the Autistica website. 

I have gone through Sprint No. 6 where the site was tested on autistic people/parents of autistic people and I have concluded that the website design can be broken down into 4 categories-
1. Layout
2. Color
3. Text
4. Symbols

**The pictures below are the pages I'm referring to while I'm talking about the design** 

### :book: Landing Page -
![Screenshot from 2021-03-29 23-51-58](https://user-images.githubusercontent.com/73518403/112881828-cada0e80-90e9-11eb-82f4-937600592b43.png)



### :writing_hand: Enter Experiences Page -
![Screenshot from 2021-03-29 23-17-00](https://user-images.githubusercontent.com/73518403/112880921-b5181980-90e8-11eb-8b74-0680a40c4e59.png)


### :eye: Views -
#### List View-
![Screenshot from 2021-03-29 23-41-13](https://user-images.githubusercontent.com/73518403/112880687-623e6200-90e8-11eb-8482-a32af7141892.png)


#### Table View-
![Screenshot from 2021-03-29 23-41-30](https://user-images.githubusercontent.com/73518403/112880697-65395280-90e8-11eb-85ef-3135cde426a8.png)




### Layout
* The card view on the landing and experiences page are nice but the size of each card could be increased so that the text doesn't look as congested.
* The How it Works card should be the biggest among the rest or it should be highlighted in some manner because a lot of test users said that the particular card was the first thing they focused on.
* In the experiences pages, the buttons on the enter experiences look clustered up as well. So either the card size could be increased or the buttons could be placed outside the card right next to it for better spacing 
* From the both the views, I believe the list view would be a much better option because:-
  1. The table view looks too mathematical as mentioned by one of the autistic test users in the sprint
  2. With a good amount of spaces and proper gridlines, the list view would be perfect. A similar card view like that in my todo-app can be done here


### Colour
* More pastel or muted colours like pale pink can be incorporated for the default settings of the page. Additional changes can be configured in the settings page.
* Colours like these could be included-
![Screenshot from 2021-03-30 07-49-46](https://user-images.githubusercontent.com/73518403/112926581-427f5c00-9131-11eb-800b-45b0d0268dcd.png)
![Screenshot from 2021-03-30 07-50-03](https://user-images.githubusercontent.com/73518403/112926585-44e1b600-9131-11eb-8c9c-3cd8e2d77c8c.png)


### Text
* In the enter experiences page, the text contained inside the card which tells the user what to enter needs to be darker.
* Some users were confused between the save and the upload button on the enter experiences page. Maybe one button for submitting the data could be used instead
* The 'Non-Verbal' button could be changed to 'Read the Page'

### Symbols
* In the landing page, the symbol for the Configure card was ambiguous for the users. Maybe a gear icon or a wrench tool could be used for configure and a book icon could be used for How It Works.
* The stack icon on the experiences page was vague as well.

### Accessibility Settings and Screen Reader
The accessibility of hte site can be increased to utilise all the user's senses to the maximum. The following can be implemented from Jiraslama's templates
* Configuring the colours on the website
* Changing font size, spacing between text and luminance
* Accessing the voice to text and screen reader commands

Since most ready made screen readers are specific to the browser or the OS, an initial disclaimer can be provided to inform them about the kind of browser they should use to access the screen reader.

### Implementation
Using TailWind CSS would be the best way to execute this as they have clear layouts and appropriate styling for this task with simple implementation. 





