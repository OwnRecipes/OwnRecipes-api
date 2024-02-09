# OwnRecipes API

This is the API that powers OwnRecipes. It uses Django/Django Rest Framework to power the API. The core responsibilities of the API are:

- OwnRecipes REST API
- Django User management with Django REST token auth
- Django Admin panel for creating new users and administration
- Static Media Management (AKA Recipe Images)

See [the homepage](https://github.com/OwnRecipes/OwnRecipes) for more information about OwnRecipes.

This project was forked from OpenEats. See [it's homepage](https://github.com/open-eats/OpenEats) for more information about OpenEats.

# Contributing
Please read the [contribution guidelines](https://github.com/OwnRecipes/OwnRecipes/blob/master/CONTRIBUTING.md) in order to make the contribution process easy and effective for everyone involved.

# Dev Tips

#### Running tests
To run tests locally:

```bash
cd ownrecipes-api
docker-compose -f test.yml -p test build
docker-compose -f test.yml -p test up -d db
docker-compose -f test.yml -p test run --rm --entrypoint sh api
python manage.py test
```

Or without docker:
```bash
cd ownrecipes-api
/bin/bash -ac '. .env.service.local; exec python3 manage.py test'
```

Note: Running the test for the first time may need some time, as the DB is doing some internal stuff.

#### REST Endpoints

You can access the API roots via there app names:

* Recipes - http://localhost:8000/api/v1/recipe
* Ingredients - http://localhost:8000/api/v1/ingredient/
* Recipe groups - http://localhost:8000/api/v1/recipe_groups/
* News - http://localhost:8000/api/v1/news/
* Lists - http://localhost:8000/api/v1/list/

You can also check the [OpenAPI document](docs/ownrecipes-api.json) for more detailed information.

#### Debug DB calls

```python
from django.db import reset_queries
from django.db import connection

reset_queries()
# Run your query here
print(connection.queries)
>>> []
```

#### Run commands

You can run commands (like the test command to run the tests).

E. g. without docker:
```bash
cd ownrecipes-api
/bin/bash -ac '. .env.service.local; exec python3 manage.py calc_ratings'
```

Commands:

* test - run tests
* calc_ratings - (re-)calculate recipe rating fields (rating, rating_count)
