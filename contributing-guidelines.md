# Contributing to AutSPACEs

:tada::balloon::cake: **Welcome to The AutSPACEs repository!** :cake::balloon::tada:

:dizzy::hatched_chick::sunny: _We're excited that you're here and want to contribute._ :sunny::hatched_chick::dizzy:

We want to ensure that every user and contributor feels welcome, included and supported to participate in _AutSPACEs_ community.
We hope that the information provided in this document will make it as easy as possible for you to get involved.

We welcome all contributions to this project via GitHub issues and pull requests.
Please follow these guidelines to make sure your contributions can be easily integrated into the projects.
As you start contributing to _AutSPACEs_, don't forget that your ideas are more important than perfect pull requests. :heart:

If you have any questions that aren't discussed below, please let us know through one of the many ways to [get in touch](#get-in-touch).

## Table of contents

Been here before? Already know what you're looking for in this guide? Jump to the following sections:

- [Joining the community](#joining-the-community)
- [Inclusivity](#inclusivity)
- [Get in touch](#get-in-touch)
- [Contributing through GitHub](#contributing-through-github)
- [Writing in Markdown](#writing-in-markdown)
- [Where to start: issues](#where-to-start-issues)
  - [Issue labels](#issue-labels)
- [Making a change with a pull request](#making-a-change-with-a-pull-request)
- [Recognising Contributions](#recognising-contributions)

## Joining the community

_AutSPACEs_ is a community-led and collaboratively developed project. 
We, therefore, require that all our members and their contributions **adhere to our code of conduct**.
Please familiarize yourself with our code of conduct that lists the expected behaviours. 

## Inclusivity

_AutSPACEs_ aims to be inclusive to people from all walks of life and to all research fields.
These intentions must be reflected in the contributions that we make to the project.

In addition to the code of conduct, we encourage intentional, inclusive actions from contributors to _AutSPACEs_.
Here are a few examples of such actions:

- use respectful, gender-neutral and inclusive language (learn more about [inclusive writing](https://www2.le.ac.uk/offices/ld/all-resources/writing/writing-resources/inclusive), resource by University of Leicester).
- make sure that the colour palettes are accessible to colour-blind readers and contributors,

Here's a useful blog post on [tips for designing scientific figures for color blind readers](http://www.somersault1824.com/tips-for-designing-scientific-figures-for-color-blind-readers) by Luk at [Somersault 1824](http://www.somersault1824.com).

## Contributing through GitHub

[Git][git] is a really useful tool for version control. 
[GitHub][github] sits on top of Git and supports collaborative and distributed working.

We know that it can be daunting to start using Git and GitHub if you haven't worked with them in the past, but _AutSPACE_ maintainers are here to help you figure out any of the jargon or confusing instructions you encounter! :heart:

In order to contribute via GitHub, you'll need to set up a free account and sign in.
Here are some [instructions](https://help.github.com/articles/signing-up-for-a-new-github-account/) to help you get going.
Remember that you can ask us any questions you need to along the way.

## Writing in Markdown

GitHub has a helpful page on [getting started with writing and formatting on GitHub](https://help.github.com/articles/getting-started-with-writing-and-formatting-on-github).

Most of the writing that you'll do will be in [Markdown][markdown].
You can think of Markdown as a few little symbols around your text that will allow GitHub to render the text with a little bit of formatting.
For example, you could write words as **bold** (`**bold**`), or in _italics_ (`_italics_`), or as a [link][rick-roll] (`[link](https://youtu.be/dQw4w9WgXcQ)`) to another webpage.

Also when writing in Markdown, please start each new sentence on a new line.
While these formats in the same way as if the new line wasn't included, it makes the [diffs produced during the pull request](https://help.github.com/en/articles/about-comparing-branches-in-pull-requests) review easier to read! :sparkles:


## Where to start: issues

Before you open a new issue, please check if any of our open issues cover your idea already.

## Making a change with a pull request

We appreciate all contributions to _AutSPACEs_.

**THANK YOU** for helping us build this useful resource. :sparkles::star2::dizzy:

The following steps are a guide to help you contribute in a way that will be easy for everyone to review and accept with ease :sunglasses:.

### 1. Comment on existing issues or open a new issue referencing your addition.

This allows other members of the _AutSPACEs_ team to confirm that you aren't overlapping with work that's currently underway and that everyone is on the same page with the goal of the work you're going to carry out.

[This blog](https://www.igvita.com/2011/12/19/dont-push-your-pull-requests/) is a nice explanation of why putting this work in upfront is so useful to everyone involved.

### 2. [Fork][github-fork] AutSPACEs

This is now your own unique copy of _AutSPACEs_.
Changes here won't affect anyone else's work, so it's a safe space to explore edits to the code!

Make sure to [keep your fork up to date][github-syncfork] with the master repository, otherwise, you can end up with lots of dreaded [merge conflicts][github-mergeconflicts].
If you prefer working in the browser, [these instructions](https://github.com/KirstieJane/STEMMRoleModels/wiki/Syncing-your-fork-to-the-original-repository-via-the-browser) describe how to sync your fork to the original repository via GitHub.

### 3. Make the changes you've discussed

Try to keep the changes focused.
If you submit a large amount of work all in one go it will be much more work for whoever is reviewing your pull request.
[Help them help you.][jerry-maguire] :wink:

While making your changes, commit often and write good, detailed commit messages.
[This blog](https://chris.beams.io/posts/git-commit/) explains how to write a good Git commit message and why it matters.
It is also perfectly fine to have a lot of commits - including ones that break code.
A good rule of thumb is to push up to GitHub when you _do_ have passing tests then the continuous integration (CI) has a good chance of passing everything. 😸

If you feel tempted to "branch out" then please make a [new branch][github-branches] and a [new issue][turing-way-issues] to go with it. [This blog](https://nvie.com/posts/a-successful-git-branching-model/) details the different Git branching models.

Please do not re-write history!
That is, please do not use the [rebase](https://help.github.com/en/articles/about-git-rebase) command to edit previous commit messages, combine multiple commits into one, or delete or revert commits that are no longer necessary.

Are you new to Git and GitHub or just want a detailed guide on getting started with version control? Check out The Turing Way's chapter on [Version Control](https://the-turing-way.netlify.com/version_control/version_control.html).

### 4. Submit a [pull request][github-pullrequest]

We encourage you to open a pull request as early in your contributing process as possible.
This allows everyone to see what is currently being worked on.
It also provides you, the contributor, feedback in real-time from both the community and the continuous integration as you make commits (which will help prevent stuff from breaking).

If you have opened the pull request early and know that its contents are not ready for review or to be merged, add "[WIP]" at the start of the pull request title, which stands for "Work in Progress".
When you are happy with it and are happy for it to be merged into the main repository, change the "[WIP]" in the title of the pull request to "[Ready for review]".

A member of _AutSPACEs_ community will then review your changes to confirm that they can be merged into the main repository.
A [review][github-review] will probably consist of a few questions to help clarify the work you've done.
Keep an eye on your GitHub notifications and be prepared to join in that conversation.

You can update your [fork][github-fork] of _AutSPACEs_ and the pull request will automatically update with those changes.
You don't need to submit a new pull request when you make a change in response to a review.

You can also submit pull requests to other contributors' branches!
Do you see an open pull requeset that you find interesting and want to contribute to?
Simply make your edits on their files and open a pull request to their branch!

GitHub has a [nice introduction][github-flow] to the pull request workflow, but please [get in touch](#get-in-touch) if you have any questions :balloon:.

## Recognising Contributions

We welcome and recognise all kinds of contributions, from fixing small errors, to developing documentation, maintaining the project infrastructure, writing chapters or reviewing existing resources.

_AutSPACEs_ follows the [all-contributors][all-contributors] specifications.
The all-contributors bot usage is described [here](https://allcontributors.org/docs/en/bot/usage).
You can see a list of current contributors at the bottom of the repository's README page. 😍

To add yourself or someone else as a contributor, comment on the relevant Issue or Pull Request with the following:

```
@all-contributors please add <username> for <contributions>
```

You can see the [Emoji Key (Contribution Types Reference)](https://allcontributors.org/docs/en/emoji-key) for a list of valid `<contribution>` types.
The bot will then create a Pull Request to add the contributor and reply with the pull request details.

**PLEASE NOTE: Only one contributor can be added with the bot at a time!**
Add each contributor in turn, merge the pull request and delete the branch (`all-contributors/add-<username>`) before adding another one.
Otherwise, you can end up with dreaded [merge conflicts][github-mergeconflicts].
Therefore, please check the [open pull requests](https://github.com/alan-turing-institute/the-turing-way/pulls) first to make sure there aren't any open requests from the bot before adding another.

What happens if you accidentally run the bot before the previous run was merged and you got those pesky merge conflicts?
(Don't feel bad, we have all done it! 🙈)
Simply close the pull request and delete the branch (`all-contributors/add-<username>`).
If you are unable to do this for any reason, please let us know and we will be very happy to help!

Finally, don't forget to add yourself to the list of contributors!

---

_These Contributing Guidelines have been adapted from the [Contributing Guideleines](https://github.com/alan-turing-institute/the-turing-way/blob/master/CONTRIBUTING.md) of [The Turing Way](https://github.com/alan-turing-institute/the-turing-way), which were themselvse adapted from the [Contributing Guidelines](https://github.com/bids-standard/bids-starter-kit/blob/master/CONTRIBUTING.md) of the [BIDS Starter Kit](https://github.com/bids-standard/bids-starter-kit). (License: CC-BY)_

