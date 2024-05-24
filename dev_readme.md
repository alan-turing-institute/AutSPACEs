# How to start website locally

If you're interested in building and running the AutSPACE platform, read on!

## Setup
Before starting, please check that the following minimum requirements have been completed.

1. Install [Docker](https://www.docker.com/products/docker-desktop). (Latest stable release, version 20.10.5 or greater)
2. Install [Docker Compose](https://docs.docker.com/compose/install/). (Latest stable release, version 1.28.5 or greater)
3. Create an [Open Humans](https://www.openhumans.org/) account.
4. Some version of Python 3.x.x.

## Installation
Project installation can be tricky, but like all things, progress is made one step at a time. 

1. [Clone](#cloning-the-repository) the repository at [AutSPACEs](https://github.com/alan-turing-institute/AutSPACEs)
2. Within the `config` directory, copy `.env.template` to `.env`. 
  Note: ***DO NOT UPLOAD THESE .ENV FILES ONTO GITHUB*** It's the equivalent of posting your passport ID on Twitter. Don't do it.

### Open Humans Project Creation
This step is a little tricky, but you're almost there. 

1. Login to [OpenHumans](openhumans.org). 
2. Navigate to [Manage Project](https://www.openhumans.org/direct-sharing/projects/manage/).
3. Create a new Oauth2 Data Request Project on Open Humans. 
4. Populate the required fields as directed. 
5. In the `Redirect URL` field, enter `http://localhost:8000/openhumans/complete`.
6. Click `Create Project`.

You'll need to obtain the Client ID and Client Secret for the OAuth project you've created. 

1. Navigate to [Manage Project](https://www.openhumans.org/direct-sharing/projects/manage/).
2. Click the newly created project. 
3. Copy and paste somewhere safe the `Client ID` and `Client Secret` under `OAuth2 Credentials`. 

### Project Configuration 
Within `.env` there are four different fields that must be populated for the project to build.

#### Django Secret Key Generation
1. Open `.env` in your favorite editor, and using `python3`, follow the instructions under the `django` header to copy/paste the generated secret key to `DJANGO_SECRET_KEY` 

The following...
`DJANGO_SECRET_KEY=__CHANGEME__`

should look something like this, where XXXXXXXXXXXXXXXXXXXXXX is the generated key. 
`DJANGO_SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXX`

#### Configuring OpenHumans
Further down the `.env` file, you should see three texts: `OPENHUMANS_CLIENT_ID`, `OPENHUMANS_CLIENT_SECRET`, and `OPENHUMANS_APP_BASE_URL`.

1. Copy the `Client ID` and `Client Secret` that you've copied previously into `OPENHUMANS_CLIENT_ID` and `OPENHUMANS_CLIENT_SECRET`, respectively.
It should look something like this, where XXXXXXXXXXXXXXXXXXXXXX are the inputted information. 
```
OPENHUMANS_CLIENT_ID=XXXXXXXXXXXXXXXXXXXXXX
OPENHUMANS_CLIENT_SECRET=XXXXXXXXXXXXXXXXXXXXXX
````

2. Type the following url into `OPENHUMANS_APP_BASE_URL`.
It should look like this!

```
OPENHUMANS_APP_BASE_URL="http://localhost:8000"
```

3. You're done!

## Running the Project
The project builds and runs in a self-contained environment called Docker. This means developer environments are preserved, and you don't need to mess with any dependency management or installation.

1. Open up Terminal or Command Line in the root level of the repository and execute the following command: `./docker-run.sh`
   Note that if you're using an M1 Mac the docker-run.sh script will force the use of an x84 linux image running using
   QEMU, which will reduce performance but avoids compatability issues.

2. Open your browser to `http://localhost:8000`

*This will display the AutSPACEs website.* Yay!

Note: Please note that certain aspects of the website may not be fully functional. ;)

## Glossary 

* Clone: make a copy of all the files and folder in the repository on your computer
* Docker: a tool which creates an individual place (called a 'container') for a software project which is set up for that project to run.
* Fork: your fork is your own personal copy of the repository, where you can make changes without affecting the main repository until you make a pull request. 
* Git: is a free, open source tool that is useful for version control (keeping a record of and managing changes to software code)
* GitHub: GitHub is an online tool which makes it easier for people to work collaboratively using Git. 
* Repository: this is a place which holds all the files and folders specific to one project. On GitHub, this is where people can work on a project together. 
* Root level: this is the level of the project which contains all the others as files and subfolders
* Terminal: this is an application on your computer which allows you to use code to modify your computer's software and files. 

## How-Tos 

### Cloning the Repository
  1. **Fork** the repository by clicking on the Fork icon at the top right hand corner of the page. 
  2. Above the list of files, click the green **Code** button.
  3. Clone the repository into your local directory. 
  4. Open terminal to the project directory.
  5. Type 'git clone', and then paste the URL you copied earlier. It will look like this, with your GitHub username instead of YOUR-USERNAME:
  >$ git clone https://github.com/YOUR-USERNAME/AutSPACEs
  7. Press enter. Your local clone will be created. 

### Accessing the database

To access the PostgreSQL database:

Make sure that the docker container runs (`./docker-run.sh`) and then use `docker exec -it autspaces-db-1 psql --username=autspaces` to access the database shell. 

### Accessing the Django shell

Django provides a way to load a Python shell that has pre-loaded all Django settings. This allows loading models, executing database queries etc. for testing purposes. To access the shell run the following command while the `./docker-run.sh` is still active in a different terminal:

`docker exec -it autspaces-web-1 python manage.py shell`

### Running tests locally

The easiest way to run the tests locally is to run them inside the Docker container. While the container is running via `./docker-run.sh`, run the following command to run all tests:

`docker exec -it autspaces-web-1 python manage.py test`

If you also want to locally run the `coverage` command to see if/how your changes have affected how much of the AutSPACEs code is covered by tests, you can use the following: 

```
docker exec -it autspaces-web-1 coverage run manage.py test
docker exec -it autspaces-web-1 coverage html
# You can now open the newly-generated htmlcov/index.html
```

### Making an admin/superuser

AutSPACEs comes with the default Django `admin` backend activated. This admin backend can be accessed at `http://localhost:8000/admin`. To use this backend, an admin account is needed. The account can be created using the Django management command `createsuperuser`. While the `./docker-run.sh` is still running, run the following command in another terminal: `docker exec -it autspaces-web-1 python manage.py createsuperuser`

### Making a user a moderator

User accounts are made moderators by being added to the `Moderators` group. The easiest way to do this is through the admin backend at `http://localhost:8000/admin/auth/user/` (note that you will need to be logged in with an admin account, see above). 

Select the user account you would like to be a moderator. On the resulting page you can see the current groups the user is a member off. By default there are no groups and the user belongs to no groups. Click the little green plus sign and on the resulting page use "Moderators" as the _Name_ and save both that "add group" dialogue and the user account. 

From now on the user should be able to see the Moderator pages in the front-end of AutSPACEs.

### Test deployment for user testing

The repo provides a simple `Dockerfile` and `fly.toml` for quick and free deployments for testing to _fly.io_ (which provides very small compute resources for free). This setup is not designed for an actual production deployment, but to allow people to interact with the prototype for e.g. user testing purposes. 

On a Mac with `brew` installed the following set of commands should be enough to deploy: 

To prepare the repo: 

```
brew install flyctl
fly launch
fly deploy
```

Before running the deploy step, one will have to add all the information that otherwise resides in the `.env` (see above) on the fly.io web interface.


## Extra Tips

*If you aren't sure how to get to the root repository, you can find it more easily by following these steps:* 

1. Type `git config --global alias.root 'rev-parse --show-toplevel` into your terminal. This will create a simpler command to take you to the root repository. 
2. Type `cd $(git root)` into your terminal. This will take you to the root of the repository you are in. 

## Docker overview 

You might find the chapter on [reproducible computational environments](https://the-turing-way.netlify.app/reproducible-research/renv.html) and spectifically the section on [containers](https://the-turing-way.netlify.app/reproducible-research/renv/renv-containers.html) in _The Turing Way_ useful!

# Managing the deployment

AutSPACEs will be deployed through the Microsoft Azure Cloud as a _Azure Web App_, which similar to the local development environment is based around Docker containers. But as it's being deployed in production we can not rely on the _Django_ internal development web server, but rather use `gunicorn` for serving the pages. 

## Dockerfile for production

For the actual deployment, we are not using `docker compose` and the `docker-compose.yml` files, but rather we use the `Dockerfile` that is in the repository root. This file has been adapted to work in the production environment, by using `docker/django/gunicorn.sh` as the entrypoint that runs when the container is launched. 

The GH repository for AutSPACEs is set up to automatically build this container every time the `main` branch is pushed to, by automatically running the `.workflows/push_docker.yml`, which in turns pushes the container to Docker Hub. On Docker Hub, the AutSPACEs production container can be found as [`gedankenstuecke/autspaces`](https://hub.docker.com/r/gedankenstuecke/autspaces), which is currently [managed by Bastian](https://github.com/gedankenstuecke/). 

You can find all the [changes made for the deployment in this PR](https://github.com/alan-turing-institute/AutSPACEs/pull/681). 

## Static handling

In the `development` environment, the static files (such as CSS, images and JS) are served directly by the development server, without having to collect them and serve them from a particular location. In production this is not an appropriate way of serving the files. Instead, bigger projects typically have a dedicated webserver for handling those files. 

Given our scope, we have taken an intermediate solution, which is using the Python library `whitenoise`, which is why the `gunicorn.sh` script runs the static collection. 

## Environment variables

On Azure, we need to set a number of environment variables that go beyond those used in the `.env` for development. Most importantly: 

1. `DJANGO_ENV` needs to be set to `production`, to ensure that we go into the right deployment path
2. `DOMAIN_NAME` needs to be set to the actual domin name where it's being deployed to, as in production we have set Django to reject all requests coming from other places for security reasons
3. `WEBSITES_PORT` should be set to `8000`, which is where our `gunicorn` serves to, so that Azure can bridge the connections. 