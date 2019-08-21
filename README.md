# clsite

[correspondence.legal](https://correspondence.legal) site, which
is [spec'ed
here](https://docs.google.com/document/d/1l4YzSrk06nKaHGVJzOCbBEWKw9peXhWLhETk6y3_9wM/edit).

While you are following this README, if you find it confusing or
needs clarifications or should be structured in a more logical
order, please create an MR to update the README to help future
developers!

## Initial setup

Install
[heroku-cli](https://devcenter.heroku.com/articles/heroku-cli#download-and-install). On OSX:

```
brew tap heroku/brew && brew install heroku
```

Then:

```
heroku login
heroku create
# Or, if you want to use an existing heroku:
#heroku git:remote -a ftwcl
```

Make sure that `heroku addons` shows that you have
heroku-postgresql, hobby-dev plan, enabled.

Note that you have to set
[buildpacks](https://devcenter.heroku.com/articles/buildpacks) for
both django and nodejs to get dependencies for both backend and
frontend. It will also build frontend assets, as our repo does not
include them:

```
# Set buildpacks for heroku
# It will first install all python dependencies
heroku buildpacks:set heroku/python
# And then will install node-js dependencies and build code
heroku buildpacks:add --index 1 heroku/nodejs
```

Finally, deploy:

```
git push heroku master
# Use admin / admin@correspondence.legal / asdfasdf
heroku run python app/manage.py createsuperuser
```

Our `Procfile` for Heroku will run `python app/manage.py migrate`
on Heroku automatically. Occasionally, Heroku might prompt you to
do run `makemigrations`, in which case you should do:

```
heroku run python app/manage.py makemigrations
heroku run python app/manage.py migrate
```

## Local setup

Make sure you have Postgres [running
locally](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup),
the same version as when you run `heroku pg`. Make sure to start a
new shell and that command `psql` works.

Requires [Pipenv](https://docs.pipenv.org/en/latest/) and
[Nodejs](https://nodejs.org/en/). We need nodejs (and npm) to
manage frontend dependencies. On OSX:

```
brew install pipenv npm
```

Django app requires several environment variables, which you should
put in `~/.bashrc` or `~/.bash_profile`. If you are using pycharm,
you can set them in Run -> Edit configurations -> Environment
variables.

* `DATABASE_URL` - uri to your database. Should be in form of
`postgres://USER:PASSWORD@HOST:PORT/DATABASE_NAME`. On OSX:
```
export DATABASE_URL=postgres://postgres@localhost/postgres
```
* `DEBUG` - set if you want to turn debug mode on.
For local testing, but *not* on Heroku, you should use:
```
export DEBUG=1
```

Nodejs comes with 2 commands to build frontend, which we show you
how to use below:
1. `npm run watch` - will build development version of frontend and
watch for changes;
2. `npm run build` - will build optimized version;

Run:
```
# Install django dependencies
pipenv install
pipenv shell

# Install and build frontend dependencies
npm install
npm run build

# If for some reason you want to recreate the DB from scratch:
#dropdb postgres
#createdb postgres

python app/manage.py migrate

# Install fixtures and dummy users
python app/manage.py loaddata admin dummy handcrafted
# Alternatively use fixtures which is described in fixtures section
# Use admin / admin@correspondence.legal / asdfasdf
#python app/manage.py createsuperuser

python app/manage.py runserver
```

(I am not able to get `heroku local` to work.)

If you want to sync from the remote Heroku DB, use `heroku pg:pull`.

## Fixtures

**Optionally** you can populate database with pregenerated data:

```bash
python app/manage.py loaddata admin handcrafted
```

* `admin` - adds admin profile. For login Email is
**admin@correspondence.legal** and Password is **asdfasdf**.
* `handcrafted` - adds real-life manually crafted profiles for
display purposes. For login Email is **celia@celialerman.com**
Password is their first name + last name lowercase. For example,
**celialerman**.

**Dummy data** can be added to the database using faker. You can use the command
`python app/manage.py generateprofiles 100` to generate 100 dummy profiles, where 1000
can be any integer number.

**Note:** those fixtures has predefined `id`, so it might overwrite
existing data. Those `id` are forced to properly populate related
tables.

## CI/CD

We are using gitlab CI/CD to automate testing and deployment to
heroku.

### Setup

Requires 2 env variables, that is set in gitlab settings -> CI/CD
-> Variables:

* `HEROKU_APP_NAME` - Your heroku app name
* `HEROKU_STAGING_API_KEY` - Your heroku API key.

In order to get long-living api key, run `heroku authorizations:create`
on machine that is authorized via `heroku login`.

### Flow

Consist of 2 jobs - `test` and `deploy`.

#### Test

Runs all tests to make sure that code is working before even consider
merging. Testing is done on gitlab side, using postgres database.
It doesn't require working webserver, since we don't use selenium.

#### Deploy

Uses [`dpl`](https://github.com/travis-ci/dpl) to push code to
heroku via api. Works only on `master` branch. Always done after
`test` (since merging itself can break code) and if tests passes,
code will be deployed.

## Deployment

### S3

We use S3 to store profile avatars.

Our project supports **either** [Heroku
CloudCube](https://devcenter.heroku.com/articles/cloudcube) or [AWS
S3 Bucket](https://aws.amazon.com/s3/).

Optionally, you can use default filestorage by not specifying
`AWS_ACCESS_KEY_ID` in `settings.py`

#### Heroku CloudCube

1. Install heroku CloudCube from heroku dashboard.  
    * It will add 3 environment variables: `CLOUDCUBE_ACCESS_KEY_ID`,
    `CLOUDCUBE_SECRET_ACCESS_KEY`, `CLOUDCUBE_URL`.
2. Add 2 environment variables to heroku based on `CLOUDCUBE_URL`.
Check out [CloudCube
docs](https://devcenter.heroku.com/articles/cloudcube#s3-api-and-bucket-name)
about how it is constructed.
    * `CLOUDCUBE_STORAGE_BUCKET_NAME` should be bucket name.  
    * `CLOUDCUBE_LOCATION` should be CUBENAME + `/public`  
    For example:
    ```bash
    heroku config
    # ...
    # CLOUDCUBE_ACCESS_KEY_ID:       AKIA37SVVXBHRH5CEJ5N
    # CLOUDCUBE_SECRET_ACCESS_KEY:   zCmoQYKx4IJz/UQ37jwXWv1pFncX61Gvz7735hQD
    # CLOUDCUBE_URL:                 https://cloud-cube.s3.amazonaws.com/jsnymx6p2qoc
    # ...
    heroku config:set CLOUDCUBE_STORAGE_BUCKET_NAME=cloud-cube
    heroku config:set CLOUDCUBE_LOCATION=jsnymx6p2qoc/public
    ```
    
#### AWS

**Don't do this part if you use CloudCube!**  

If you don't have pre-existing S3 bucket, you will need to create
it first:

1. Go to AWS S3 console - https://s3.console.aws.amazon.com/s3/home
2. Create bucket
    * *Name and region* - Unique name
    * *Set permissions* - Allow public access
    * Remember your `bucket name`!
3. Go to AWS IAM console - https://console.aws.amazon.com/iam/home
4. Policies -> Add Policy
    * *JSON* - replace `YOUR_BUCKET_NAME` with your bucket name
    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "s3:GetObjectAcl",
                    "s3:GetObject",
                    "s3:ListBucket",
                    "s3:DeleteObject",
                    "s3:PutObjectAcl"
                ],
                "Resource": [
                    "arn:aws:s3:::YOUR_BUCKET_NAME/*",
                    "arn:aws:s3:::YOUR_BUCKET_NAME"
                ]
            }
        ]
    }
    ```
    * *name* - Unique name
5. Users -> Add User
    * Unique name
    * Programmatic access
    * Attach existing policies directly -> your policy name
    * Remember `Access key` and `Secret key`!

Add following environment variables in your environment:
* `AWS_ACCESS_KEY_ID` - Access key
* `AWS_SECRET_ACCESS_KEY` - Secret key
* `AWS_STORAGE_BUCKET_NAME` - Bucket name

### Assets

Whitenoise caching crashes if assets has relative urls that leads
outside of staticfiles (for example `../../`).

This will cause `SuspiciousFileOperation` with `collectstatic` or `heroku push`.

Make sure that new css/js code doesn't violate it.

### Theme

We use [Material
Kit](https://demos.creative-tim.com/material-kit/index.html) theme.
Github repo is located
[here](https://github.com/creativetimofficial/material-kit)

Current version of Material Kit theme is 2.0.5.  
Has css modified to remove all relative urls (carousel arrows).

All images are not stored here and instead linked from demo website.
SCSS files are also not part of this repo, but present in theme
repo.

Iconset is [Font Awesome v.5](https://fontawesome.com/), downloaded via CDN.

## Testing

To run all tests:
```
python app/manage.py test
```

All tests requires
`@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')`
decorator to be set for each test class or `python manage.py
collectstatic`. Otherwise it will fail because there is no whitenoise
manifest.  More info can be found in this [SO
question](https://stackoverflow.com/questions/44160666/valueerror-missing-staticfiles-manifest-entry-for-favicon-ico)

## Manipulating law-type-tag ontology:

You can manipulate the law-type-tags ontology by editing this json
file: `profiles/tags/law-type-tag.json`.

Every tag has a name and a subarea, at this time we are supporting
two levels only.

## Further Reading

To update `Pipfile.lock`:
```
pipenv lock
```

- [pipenv](https://docs.pipenv.org/en/latest/)
- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)

## Generating fixtures

### Faker

`faker.py` is a module to generate model instances with random data.
We are using it to populate database with data and use it to test
our website.

We are using [Faker module](https://github.com/joke2k/faker) to
generate random data that makes sense for different field types.

In order to use it with Django Models, we extend Faker `BaseProvider`
for example with `profiles.faker.ProfileProvider`.

`ProfileProvider` has multiple methods, each will return a **non-saved**
django model instance with randomly populated fields.

For example, you can generate models:
```python
from faker import Faker
from profiles.faker import ProfileProvider

# Load Faker instance
fake = Faker()

# Attach our provider, allowing faker to generate Django Instances
fake.add_provider(ProfileProvider)

# Generate simple profile without any related models
profile = fake.profile()
# <Profile: corey93@gmail.com>

# Generate tuple with profile and all related models
full_profile = fake.full_profile()
# (<Profile: englishcheryl@wood-kirk.org>, <Address: Address object (None)>, <Education: Education object (None)>, <Admissions: Admissions object (None)>, <LawSchool: LawSchool object (None)>, <WorkExperience: WorkExperience object (None)>, <Organization: Organization object (None)>, <Award: Award object (None)>)
```

`ProfileProvider` django instances are not saved in database, so
`faker.py` comes with `generate_profiles(count)` method that generate
set number of profiles and populate it into current database. It
uses `bulk_create` to do it efficiently and not stress database.

```python
from profiles.faker import generate_profiles

# populate database with 50 profiles with related models
generate_profiles(50)
```

### Fixtures

When you populate your database, you can export it into *fixtures*
for other developers to easily import them into their databases.

```bash
# dump all models from `profiles` app
python manage.py dumpdata profiles

# dump only awards from `profiles` app
python manage.py dumpdata profiles.Award

# dump only awards from `profiles` app and save into dump.json
# might contain terminal logs, so don't forget to clean it from any non-json lines
python manage.py dumpdata profiles.Award > profiles/fixtures/dump.json

# load fixture to database
python manage.py loaddata dump
```

Remember that those fixtures will have id predefined, as they are currently in your database. Different fixture files with same models will overwrite each other if they contain models with same id.
