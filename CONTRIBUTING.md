# Contributing

Thanks for taking the time to understand how you can contribute to the Chowist project!

There are three general roles for contributing:

- As a submitter
- As a reviewer
- As a contributor

Look below for guidelines on each type of role.

## Submitters

Feel free to create pull requests for the following changes:

- Enhancements to Django application logic
- Enhancements to Django templates
- Enhancements to documentation
- Additions to static files (JPG, SVG, etc.)
- Additions to restaurant fixture

Before submitting a pull request, follow the steps below to ensure that the review process goes smoothly.

### Check Python formatting

Run `ruff format chowist places portal` to cleanup formatting inconsistencies.

Run `ruff check chowist places portal` to look for remaining code to fix manually.

### Check HTML formatting

Verify that HTML uses two-space indents.

Verify that CSS IDs and classes follow the `kebab-case` convention.

### Check application correctness

Run `python manage.py test` to verify core logic.

Run `python manage.py runserver` and click through pages to verify workflows.

## Reviewers

Follow the repository code of conduct while reviewing pull requests.

## Contributors

Create a pull request indicating interest in becoming a project contributor.
