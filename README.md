# OwnRecipes API

This is the API that powers OwnRecipes. It uses Django/Django Rest Framework to power the API. The core responsibilities of the API are:

- OwnRecipes REST API
- Django User management with Django REST token auth
- Django Admin panel for creating new users and administration
- Static Media Manangemtn (AKA Recipe Images)

See [the homepage](https://github.com/OwnRecipes/OwnRecipes) for more information about OwnRecipes!

This project was forked from OpenEats. See [the homepage](https://github.com/open-eats/OpenEats) for more information about OpenEats!

# Contributing
Please read the [contribution guidelines](https://github.com/OwnRecipes/OwnRecipes/blob/master/CONTRIBUTING.md) in order to make the contribution process easy and effective for everyone involved.

# Dev Tips

#### Running tests
To run tests locally:

```bash
cd OwnRecipes-web
docker-compose -f test.yml -p test build
docker-compose -f test.yml -p test up -d db
docker-compose -f test.yml -p test run --rm --entrypoint sh api
python manage.py test
```

Note: If this is the first time you are running the tests, give the DB some time to build itself once it's build there is no need to wait again.

#### REST Endpoints

You can access the API roots via there app names:

* Recipes - http://localhost:8000/api/v1/recipe
* Ingredients - http://localhost:8000/api/v1/ingredient/
* Recipe groups - http://localhost:8000/api/v1/recipe_groups/
* News - http://localhost:8000/api/v1/news/
* Lists - http://localhost:8000/api/v1/list/