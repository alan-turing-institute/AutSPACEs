# Next Steps for the AutSPACEs Development (2022.02.24)
> These are the current identified tasks for the AutSPACes platform. Please feel free to add new tasks or edit the current tasks here. 
## Frontend
* Refactor the code
* Separate the current codes into components for easy maintenance 
* Add responsive design for mobile and table viewing 
    * testing across different browsers  
* Implement `Question` section on the `Registration` page after being redirected from the OpenHumans 
* Implement `Moderate Stories` page
* Update links across the platform (`Share Stories`, `Moderate Stories`, `View Stories`, `Footer`)
* Add dynamic rendering for stories viewing on `View Stories` page
* Add error messages behavior when form is not complete on `Share Stories` page
* Fix `log in`and only be accessible through the `Homepage`now. One cannot log in from other pages, like `Vie Stories`or `About Us`
    * After logging in successfully, one should be re-directed back to their browsed pages instead of being re-directed to the `Homepage`

## Backend
* Decide the database location on the AutSPACEs side 
* Decide the hosted server of the platform 
* Integrate the registration steps with Open Humans together on `Registration` page
* Connect the `registration questions`to the database
* Update the database `Experience`model (newly added: titles, triggering labels, sharing for others) (Details see `Share Stories` page)
* Connect search & filter functions with the database on `View Stories` page
* Connect the experience model to the database 
* Build the `moderator`model 
    * `Moderate Stories` page should only visible to authenticated `moderators`
* Build the [`moderation workflow`](https://github.com/alan-turing-institute/AutisticaCitizenScience/tree/master/Moderation/strategy-process-moderation)
* Build messages data pipeline for `My Stories`page
* Establish approach to (unit) tests

## Test
* Test the responsive design & error states behaviors
* Agree wording of messages on test deployment about not entering sensitive data

## Content
* Proof-reading the platform contents 
