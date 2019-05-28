# clsite

[correspondence.legal](https://correspondence.legal) site, which
is [spec'ed
here](https://docs.google.com/document/d/1l4YzSrk06nKaHGVJzOCbBEWKw9peXhWLhETk6y3_9wM/edit).

## Initial setup

```
heroku apps:create ftwcl-yourhandle
git push heroku master
heroku run python manage.py migrate
```

## Further Reading

- [pipenv](https://docs.pipenv.org/en/latest/)
- [Gunicorn](https://warehouse.python.org/project/gunicorn/)
- [WhiteNoise](https://warehouse.python.org/project/whitenoise/)
- [dj-database-url](https://warehouse.python.org/project/dj-database-url/)
