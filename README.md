# AutSPACEs
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-7-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

*Code respository for AutSPACEs: the Autistica/Turing citizen science platform*

## Welcome.

This repository **holds the code** for AutSPACEs. AutSPACEs is a citizen science platform co-created by autistic people and their supporters alongside researchers and the open source community. 

It is linked to the [Autistica/Turing Citizen Science](https://github.com/alan-turing-institute/AutisticaCitizenScience) repository, which is used for **project management and to hold resources**. If you'd like to take part in anything which isn't directly related to building the platform, take a look there. There are lots of ways to get involved. You can find out more in the contributing guidelines. 

The platform is currently being developed using the Python/Django web development framework. You can [Skip to Development Information](#development-information) or continue reading for more information about the project in general. 

## Get the platform running

To get the current website to run on your local device please follow [these steps](/dev_readme.md).

Here is a useful resource for learning Django: https://tutorial.djangogirls.org/en/

## How to work with us

The issues list contains all the work that is still to be done to finish the platform. It also lists extra features that are not essential but which would make the platform better. Every issue is labelled to show what skills we think will be required to contribute to the platform. 

Everyone is asked to follow our code of conduct and to look at the contributing guidelines for more information on how to get started.

You can also join our community by [getting in touch](#get-in-touch) with the research team. 

## About the platform

AutSPACEs is a citizen science platform which will be used to investigate how sensory processing differences affect the ways autistic people navigate the world around them. 

### Goals

The platform has four main goals:

1. **Collect**: to collect together the stories of autistic people and their supporters about how they are affected by sensory processing in their daily lives. This will form a qualitative dataset for research.
2. **Share**: to create a safe, autism-voice-first online environment for autistic people and their supporters to share their stories. These can then be read by others who can benefit from their experiences and insights. 
3. **Educate**: to educate non-autistic people about the experiences of autistic people so that they can become better supporters to them, and to reduce misunderstandings and stigmas about autism. 
4. **Change**: use research done on the dataset to inform policy-makers and people who build and design environments how to make those spaces better for autistic people.

### How it works 

![How-it-works](/Citscicartoon.png)

Users of the platform have the option to view other's stories or to submit their own. They must sign in to submit. All users have the option of submitting their story for research, publishing their story on the platform itself, neither, or both. If it is published, it will first be moderated to make sure it follows the platform's code of conduct. While logged in, users will be able to view their own stories and change their consent options.

### How it is built

The platform is being developed using the Python/Django web development framework. Users will be able to share experiences through a website which will then be deposited into a backend database supported by [Open Humans.](https://github.com/OpenHumans). A demo website for data transfer based on Open Humans and deployed using Django, can be found in the [Filemanagement Demo Repository](https://github.com/alan-turing-institute/autistica-filemanagement-demo).

The platform is entirely open source. All code is available to be used and adapted. Eveyone is invited to contribute. 

The design for the platform is created according to specifications made by autistic people and their supporters. It is build with, for, and by the autistic community. You can find out more about this at the [Autistica/Turing Citizen Science](https://github.com/alan-turing-institute/AutisticaCitizenScience) repository. 

**To be succesful, the platform must be accessible to diverse autistic users and meet the priorities and recommendations of the autistica/turing citizen science community.**

It has been built on work from the following repositories:

* Project Management: [Autistica/Turing Citizen Science](https://github.com/alan-turing-institute/AutisticaCitizenScience)
* Code for earlier version: [AutisticaPlatformPrototype](https://github.com/alan-turing-institute/AutisticaPlatformPrototype)
* Code for earlier version: [alan-turing-institute/autistica-filemanagement-demo](https://github.com/alan-turing-institute/autistica-filemanagement-demo)

## About the project

The Autistica/Turing citizen science project is a collaboration between the autism research charity Autistica and the UK's national institute for AI and data science, The Alan Turing Institute.

It is a research project which is pioneering new methods of participatory science to enable an empowered autistic community and break down the division between researcher and research "subject". To find out more about participatory science and why it matters, visit the [Autistica/Turing Citizen Science](https://github.com/alan-turing-institute/AutisticaCitizenScience) repository. 

## Get in touch

There are lots of ways to get in touch and stay updated. You can:

* Anonymously, publicly share suggestions via the "always open" google form: https://bit.ly/AutisticaTuringCitSciForm
* Say hello in our public slack channel: https://slackin.openhumans.org 
* Subscribe to our mailing list for monthly project updates: https://tinyletter.com/AutisticaTuringCitizenScience
* Join the discussion in our issues and pull requests 

We welcome all contributions and feedback! 

# Development Information 

Autistica Turing Citizen Science Platform

This project was generated with [`wemake-django-template`](https://github.com/wemake-services/wemake-django-template). Current template version is: [04e22278c3d0ac862ac4a4ce841212b2f8e938d4](https://github.com/wemake-services/wemake-django-template/tree/04e22278c3d0ac862ac4a4ce841212b2f8e938d4). See what is [updated](https://github.com/wemake-services/wemake-django-template/compare/04e22278c3d0ac862ac4a4ce841212b2f8e938d4...master) since then.


[![wemake.services](https://img.shields.io/badge/%20-wemake.services-green.svg?label=%20&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC%2FxhBQAAAAFzUkdCAK7OHOkAAAAbUExURQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP%2F%2F%2F5TvxDIAAAAIdFJOUwAjRA8xXANAL%2Bv0SAAAADNJREFUGNNjYCAIOJjRBdBFWMkVQeGzcHAwksJnAPPZGOGAASzPzAEHEGVsLExQwE7YswCb7AFZSF3bbAAAAABJRU5ErkJggg%3D%3D)](https://wemake.services) 
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)


## Prerequisites

You will need:

- `python3.8` (see `pyproject.toml` for full version)
- `postgresql` with version `9.6`
- `docker` with [version at least](https://docs.docker.com/compose/compose-file/#compose-and-docker-compatibility-matrix) `18.02`


## Development

When developing locally, we use:

- [`editorconfig`](http://editorconfig.org/) plugin (**required**)
- [`poetry`](https://github.com/python-poetry/poetry) (**required**)
- `pycharm 2017+` or `vscode`

To get the current website to run on your local device please follow [these steps](/dev_readme.md).

## Documentation

Full documentation is available here: [`docs/`](docs).

## Contributors 

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/jhlink"><img src="https://avatars2.githubusercontent.com/u/1872836?v=4?s=100" width="100px;" alt=""/><br /><sub><b>James </b></sub></a><br /><a href="#infra-jhlink" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/alan-turing-institute/AutSPACEs/commits?author=jhlink" title="Tests">⚠️</a> <a href="https://github.com/alan-turing-institute/AutSPACEs/commits?author=jhlink" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/GeorgiaHCA"><img src="https://avatars1.githubusercontent.com/u/46889966?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Georgia</b></sub></a><br /><a href="#content-GeorgiaHCA" title="Content">🖋</a> <a href="https://github.com/alan-turing-institute/AutSPACEs/commits?author=GeorgiaHCA" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/Angelsaur"><img src="https://avatars.githubusercontent.com/u/67108701?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Angelsaur</b></sub></a><br /><a href="https://github.com/alan-turing-institute/AutSPACEs/commits?author=Angelsaur" title="Documentation">📖</a> <a href="#design-Angelsaur" title="Design">🎨</a> <a href="#ideas-Angelsaur" title="Ideas, Planning, & Feedback">🤔</a> <a href="#userTesting-Angelsaur" title="User Testing">📓</a></td>
    <td align="center"><a href="https://github.com/JamesSCTJ"><img src="https://avatars.githubusercontent.com/u/60160241?v=4?s=100" width="100px;" alt=""/><br /><sub><b>JamesSCTJ</b></sub></a><br /><a href="#ideas-JamesSCTJ" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/alan-turing-institute/AutSPACEs/commits?author=JamesSCTJ" title="Tests">⚠️</a> <a href="https://github.com/alan-turing-institute/AutSPACEs/pulls?q=is%3Apr+reviewed-by%3AJamesSCTJ" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="http://www.brainonsilicon.com"><img src="https://avatars.githubusercontent.com/u/42813259?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sophia Batchelor</b></sub></a><br /><a href="#ideas-BrainonSilicon" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://tzovar.as"><img src="https://avatars.githubusercontent.com/u/674899?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Bastian Greshake Tzovaras</b></sub></a><br /><a href="#infra-gedankenstuecke" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a> <a href="https://github.com/alan-turing-institute/AutSPACEs/commits?author=gedankenstuecke" title="Tests">⚠️</a> <a href="https://github.com/alan-turing-institute/AutSPACEs/commits?author=gedankenstuecke" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/mridubhatnagar"><img src="https://avatars.githubusercontent.com/u/16894718?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Mridu Bhatnagar</b></sub></a><br /><a href="https://github.com/alan-turing-institute/AutSPACEs/commits?author=mridubhatnagar" title="Code">💻</a> <a href="#infra-mridubhatnagar" title="Infrastructure (Hosting, Build-Tools, etc)">🚇</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->
