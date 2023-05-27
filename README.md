# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/alan-turing-institute/AutSPACEs/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                                                      |    Stmts |     Miss |   Cover |   Missing |
|-------------------------------------------------------------------------- | -------: | -------: | ------: | --------: |
| manage.py                                                                 |       11 |        2 |     82% |     20-21 |
| server/\_\_init\_\_.py                                                    |        0 |        0 |    100% |           |
| server/apps/\_\_init\_\_.py                                               |        0 |        0 |    100% |           |
| server/apps/main/\_\_init\_\_.py                                          |        0 |        0 |    100% |           |
| server/apps/main/admin.py                                                 |        4 |        0 |    100% |           |
| server/apps/main/apps.py                                                  |        3 |        0 |    100% |           |
| server/apps/main/context\_processors.py                                   |        4 |        0 |    100% |           |
| server/apps/main/forms.py                                                 |       73 |        1 |     99% |       135 |
| server/apps/main/helpers.py                                               |      146 |        2 |     99% |  135, 356 |
| server/apps/main/migrations/0001\_initial.py                              |        6 |        0 |    100% |           |
| server/apps/main/migrations/0002\_add\_fields\_to\_public\_experiences.py |        4 |        0 |    100% |           |
| server/apps/main/migrations/0003\_publicexperience\_title\_text.py        |        4 |        0 |    100% |           |
| server/apps/main/migrations/0004\_update\_publicexperience\_class.py      |        4 |        0 |    100% |           |
| server/apps/main/migrations/0005\_auto\_20230105\_1303.py                 |        4 |        0 |    100% |           |
| server/apps/main/migrations/0006\_auto\_20230123\_1209.py                 |        4 |        0 |    100% |           |
| server/apps/main/migrations/0007\_auto\_20230123\_1341.py                 |        4 |        0 |    100% |           |
| server/apps/main/migrations/0008\_experiencehistory.py                    |        5 |        0 |    100% |           |
| server/apps/main/migrations/0009\_auto\_20230327\_1226.py                 |        5 |        0 |    100% |           |
| server/apps/main/migrations/\_\_init\_\_.py                               |        0 |        0 |    100% |           |
| server/apps/main/models.py                                                |       27 |        1 |     96% |        42 |
| server/apps/main/templatetags/\_\_init\_\_.py                             |        0 |        0 |    100% |           |
| server/apps/main/templatetags/custom\_tags.py                             |       12 |        3 |     75% |     13-16 |
| server/apps/main/tests/\_\_init\_\_.py                                    |        0 |        0 |    100% |           |
| server/apps/main/tests/test\_helpers.py                                   |      173 |        0 |    100% |           |
| server/apps/main/tests/test\_models.py                                    |       25 |        0 |    100% |           |
| server/apps/main/tests/test\_moderate\_views.py                           |      168 |        0 |    100% |           |
| server/apps/main/tests/test\_my\_stories.py                               |       28 |        0 |    100% |           |
| server/apps/main/tests/test\_views.py                                     |      131 |        0 |    100% |           |
| server/apps/main/tests/tests\_2023.py                                     |       12 |        7 |     42% |     11-35 |
| server/apps/main/urls.py                                                  |        4 |        0 |    100% |           |
| server/apps/main/views.py                                                 |      156 |       19 |     88% |71, 131, 225-231, 342-389 |
| server/settings/\_\_init\_\_.py                                           |        8 |        0 |    100% |           |
| server/settings/components/\_\_init\_\_.py                                |        4 |        0 |    100% |           |
| server/settings/components/caches.py                                      |        2 |        0 |    100% |           |
| server/settings/components/common.py                                      |       38 |        0 |    100% |           |
| server/settings/components/csp.py                                         |        5 |        0 |    100% |           |
| server/settings/components/logging.py                                     |        3 |        0 |    100% |           |
| server/settings/environments/\_\_init\_\_.py                              |        1 |        0 |    100% |           |
| server/settings/environments/development.py                               |       27 |        0 |    100% |           |
| server/settings/environments/local.py                                     |        0 |        0 |    100% |           |
| server/urls.py                                                            |       11 |        0 |    100% |           |
|                                                                 **TOTAL** | **1116** |   **35** | **97%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/alan-turing-institute/AutSPACEs/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/alan-turing-institute/AutSPACEs/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/alan-turing-institute/AutSPACEs/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/alan-turing-institute/AutSPACEs/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Falan-turing-institute%2FAutSPACEs%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/alan-turing-institute/AutSPACEs/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.