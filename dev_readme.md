# How to start website

#### 1. Download and install [Docker](https://www.docker.com/products/docker-desktop) for your operating system.

#### 2. Clone the repository into your local directory.

  1. **Fork** the repository by clicking on the Fork icon at the top right hand corner of the page. 
  2. Above the list of files, click the green **Code** button.
  3. Clone the repository into your local directory. 
  4. Open terminal to the project directory.
  5. Type 'git clone', and then paste the URL you copied earlier. It will look like this, with your GitHub username instead of YOUR-USERNAME:
  >$ git clone https://github.com/YOUR-USERNAME/AutSPACEs
  7. Press enter. Your local clone will be created. 

#### 3. Open up Terminal or Command Line in the root level of the repository and type in the following command: `docker-compose up`

*If you aren't sure how to get to the root repository, you can find it more easily by doing the following steps:* 

  1. Type `git config --global alias.root 'rev-parse --show-toplevel` into your terminal. This will create a simpler command to take you to the root repository. 
  2. Type `cd $(git root)` into your terminal. This will take you to the root of the repository you are in. 

#### 4. Open your browser to `https://localhost:8000`

*This will display the AutSPACEs website.*

## Glossary 

* Clone: make a copy of all the files and folder in the repository on your computer
* Docker: a tool which creates an individual place (called a 'container') for a software project which is set up for that project to run.
* Fork: your fork is your own personal copy of the repository, where you can make changes without affecting the main repository until you make a pull request. 
* Git: is a free, open source tool that is useful for version control (keeping a record of and managing changes to software code)
* GitHub: GitHub is an online tool which makes it easier for people to work collaboratively using Git. 
* Repository: this is a place which holds all the files and folders specific to one project. On GitHub, this is where people can work on a project together. 
* Root level: this is the level of the project which contains all the others as files and subfolders
* Terminal: this is an application on your computer which allows you to use code to modify your computer's software and files. 
