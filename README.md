# clsite

[correspondence.legal](https://correspondence.legal) site, which
is [spec'ed
here](https://docs.google.com/document/d/1l4YzSrk06nKaHGVJzOCbBEWKw9peXhWLhETk6y3_9wM/edit).

## Initial setup

Install [heroku-cli](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

```
heroku login
heroku create
git push heroku master
# Use admin / admin@correspondence.legal / asdfasdf
heroku run python manage.py createsuperuser
```

Make sure that `heroku addons` shows that you have
heroku-postgresql, hobby-dev plan, enabled.

## Local setup

Make sure you have Postgres [running
locally](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup),
the same version as when you run `heroku pg`.

Run:
```
pipenv install
pipenv shell
python manage.py migrate
# Use admin / admin@correspondence.legal / asdfasdf
python manage.py createsuperuser
# For fresh pgsql install, use heroku suggested url
# If you have preconfigured pgsql, use your database username and password
# export DATABASE_URL=postgres://USER:PASSWORD@127.0.0.1:5432/postgres
export DATABASE_URL=postgres://$(whoami)
python manage.py runserver
```

(I am not able to get `heroku local` to work.)

If you want to sync from the remote Heroku DB, use `heroku pg:pull`.

## Deployment

### S3

We use S3 to store profile avatars.

If you don't have pre-existing S3 bucket, you will need to create it first:

1. Go to AWS S3 console - https://s3.console.aws.amazon.com/s3/home
2. Create bucket
    * *Name and region* - Unique name
    * *Set permissions* - Allow public access
    * Remember your `bucket name`!
3. Go to AWS IAM console - https://console.aws.amazon.com/iam/home
4. Users -> Add User
    * Unique name
    * Programmatic access
    * Attach existing policies directly -> **AmazonS3FullAccess**
    * Remember `Access key` and `Secret key`!

Add following environment variables in your environment:
* `AWS_ACCESS_KEY_ID` - Access key
* `AWS_SECRET_ACCESS_KEY` - Secret key
* `AWS_STORAGE_BUCKET_NAME` - Bucket name

Optionally, you can use default filestorage by not specifying `AWS_ACCESS_KEY_ID` in `settings.py` 

### Assets

Whitenoise caching crashes if assets has relative urls that leads outside of staticfiles (for example `../../`).  
This will cause `SuspiciousFileOperation` with `collectstatic` or `heroku push`.  
Make sure that new css/js code doesn't violate it.

### Theme

We use [Material Kit](https://demos.creative-tim.com/material-kit/index.html) theme. Github repo is located [here](https://github.com/creativetimofficial/material-kit)

Current version of Material Kit theme is 2.0.5.  
Has css modified to remove all relative urls (carousel arrows).

All images are not stored here and instead linked from demo website. SCSS files are also not part of this repo, but present in theme repo.

Iconset is [Font Awesome v.5](https://fontawesome.com/), downloaded via CDN.

## Testing

To run all tests:
```
python manage.py test
```

All tests requires `@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')`
decorator to be set for each test class or `python manage.py collectstatic`. Otherwise it will fail because there is no whitenoise manifest.  
More info can be found in this [SO question](https://stackoverflow.com/questions/44160666/valueerror-missing-staticfiles-manifest-entry-for-favicon-ico)

## Further Reading

To update `Pipfile.lock`:
```
pipenv lock
```

- [pipenv](https://docs.pipenv.org/en/latest/)
- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
