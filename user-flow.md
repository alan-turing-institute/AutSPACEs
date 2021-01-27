## User and user data flow

This file contains user flows for navigating the platform, and shows how data is handled as it is entered. 

### Open Humans & Joining the project

![](https://i.imgur.com/Lme25tv.png)

### Platform interactions

![](https://i.imgur.com/JFkJDBF.png)

### Data Management using Open Humans

### General Storage

All experiences are stored on Open Humans as a simple *JSON* file, at this point just containing the timestamp of posting the experience and the experience text.

```
{
    "text": "add another test",
    "timestamp": "2019-07-18 10:43:56.549079"
}
```

Furthermore the application deposits additional metadata in Open Humans when uploading a file:

```
{
    "id": 1234,
    "basename": "testfile.json",
    "created": "2019-07-18T10:43:59.709964Z",
    "download_url": "https://www.openhumans.org/data-management/datafile-download/XXXXXX/?key=access_key",
    "metadata":
    {
        "tags":
        [
            "viewable",
            "non-research"
        ],
        "uuid": "f1790562-a948-11e9-8161-8c859069dbc5",
        "description": "this is a test file"
    },
    "source": "direct-sharing-267"
}
```

The `uuid` is used to correctly link publicly shared experiences to the files on Open Humans. The `tags` describe whether a file is marked as publicly shared or not and whether research use of the data is permitted.


### Public Storage
When a user flags an experience as publicly availble a copy of it will be deposited in this applications own database. The `Django` model to store those is found in `main/models.py`. In addition to linking it to the user, it also stores the `uuid`, linking it to the deposited data in Open Humans.

**In all cases the data should be stored on Open Humans and be considered the canonical copy. The data stored in this application's database (e.g. public experiences) is just done as a way to cache the data for faster loading times**
