# How to start website

#### 1. Download and install [Docker](https://www.docker.com/products/docker-desktop) for your operating system. 

#### 4. Download and Install [Django](https://www.djangoproject.com/) for your operating system.

#### 3. Clone this repository.

  1. **Fork** the repository by clicking on the Fork icon at the top right hand corner of the page. 
  2. Above the list of files, click the green **Code** button.
  3. Choose how you would like to clone the repository To clone the repository using HTTPS, under "Clone with HTTPS", click. To clone the repository using an SSH key, click Use SSH, then click the rectangular file icon. 
  4. Open terminal
  5. Change the current working directory to the location where you want the cloned directory.
  6. Type git clone, and then paste the URL you copied earlier. It will look like this, with your GitHub username instead of YOUR-USERNAME:
  >$ git clone https://github.com/YOUR-USERNAME/AutSPACEs
  7. Press enter. Your local clone will be created. 

#### 4. Open up Terminal or Command Line in the root level of the repository and type in the following command: `docker-compose up`

*If you aren't sure how to get to the root repository, you can find it more easily by doing the following steps:* 

  1. Type `git config --global alias.root 'rev-parse --show-toplevel` into your terminal. This will create a simpler command to take you to the root repository. 
  2. Type `cd $(git root)` into your terminal. This will take you to the root of the repository you are in. 

#### 5. Open your browser to `https://localhost:8000`

*This will display the AutSPACEs website.*

## Glossary 

* Clone: make a copy of all the files and folder in the repository on your computer 
* Django: a free, open source framework for making websites which is especially useful for websites managing a lot of data. 
* Docker: a tool which creates an individual place (called a 'container') for a software project which is set up for that project to run.
* Fork: your fork is your own personal copy of the repository, where you can make changes without affecting the main repository until you make a pull request. 
* Git: is a free, open source tool that is useful for version control (keeping a record of and managing changes to software code)
* GitHub: GitHub is an online tool which makes it easier for people to work collaboratively using Git. 
* Repository: this is a place which holds all the files and folders specific to one project. On GitHub, this is where people can work on a project together. 
* Root level: this is the level of the project which contains all the others as files and subfolders
* Terminal: this is an application on your computer which allows you to use code to modify your computer's software and files. 
