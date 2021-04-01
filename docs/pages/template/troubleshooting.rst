Troubleshooting
===============

This section is about some of the problems you may encounter and
how to solve these problems.


Docker
------

Pillow
~~~~~~

If you want to install ``Pillow`` that you should
add this to dockerfile and rebuild image:

- ``RUN apk add jpeg-dev zlib-dev``
- ``LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "poetry install ..."``

See `<https://github.com/python-pillow/Pillow/issues/1763>`_

Root owns build artifacts
~~~~~~~~~~~~~~~~~~~~~~~~~

This happens on some systems.
It happens because build happens in ``docker`` as the ``root`` user.
The fix is to pass current ``UID`` to ``docker``.
See `<https://github.com/wemake-services/wemake-django-template/issues/345>`_.

MacOS performance
~~~~~~~~~~~~~~~~~

If you use the MacOS you
know that you have problems with disk performance.
Starting and restarting an application is slower than with Linux
(it's very noticeable for project with large codebase).
For particular solve this problem add ``:delegated`` to each
your volumes in ``docker-compose.yml`` file.

.. code:: yaml

  volumes:
    - pgdata:/var/lib/postgresql/data:delegated

For more information, you can look at the
`docker documents <https://docs.docker.com/docker-for-mac/osxfs-caching/>`_
and a good `article <https://medium.com/@TomKeur/how-get-better-disk-performance-in-docker-for-mac-2ba1244b5b70>`_.

Open Humans Mismatch Redirect URI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The URL that you've defined under `Redirect URL` when creating your Oauth2 Open Humans project is incorrect. If you've followed the `dev_readme.md`, it should be something like `http://localhost:8000/openhumans/complete`.

Django Problems
~~~~~~~~~~~~~~~

NoReverseMatch Errors
---------------------
Django is saying that it cannot find a matching URL pattern for the URL you've provided in any of your installed app's urls. (i.e. urls.py, views.py, etc.) See (here)[https://stackoverflow.com/questions/38390177/what-is-a-noreversematch-error-and-how-do-i-fix-it] for more information.

Styling is All Wrong!
---------------------
This is because the CSP settings within the project are quite strict. The css, scripts, and other static assets used to make the website look pretty isn't allowed for security reasons. You can see these errors when opening up the `Inspector` (Right Click -> Inspect Element) and viewing the Console tab within your browser of choice. See the following for more information.
(Django CSP)[https://django-csp.readthedocs.io/en/latest/configuration.htm://django-csp.readthedocs.io/en/latest/configuration.html]
(Unsafe-Inline)[https://content-security-policy.com/unsafe-inline/]
(Managing Static Files)[https://docs.djangoproject.com/en/2.2/howto/static-files/]

