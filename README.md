# django-rest-api-advanced

Udemy's Build a Backend REST API with Python &amp; Django - Advanced course

# Running flake8

```bash
docker-compose run --rm app sh -c "python manage.py test && flake8"
```

# Running unit tests

```bash
docker-compose run --rm app sh -c "python manage.py test"
```

# Important things to note while writing test cases:

1. Test cases should be independent of each other.
2. Test cases should be isolated from each other.
3. Test cases should be repeatable.
4. Test cases should be self-validating.
5. Test cases should be timely.
6. Test cases should have the word "test" in their names.
7. Check for indentations in test cases.
8. Check for ImportErrors in test cases.
9. Use test directory or tests.py file for writing test cases.
