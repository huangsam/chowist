# AGENTS.md

## Project Overview

**Chowist** is a Django-based web app replicating Yelp features: user auth, restaurant discovery, reviews, profiles. Uses Django 5.2+, Bootstrap 5, django-crispy-forms, django-filters, PostgreSQL/SQLite, Docker.

**Key Features:**
- Auth & profiles
- Restaurant search/filtering
- 1-5 star reviews
- Categories, geolocation, pagination
- Permission-based access

## Project Structure

### Core (`chowist/`)
- `settings/base.py` - Apps, middleware, templates, static, logging
- `settings/dev.py`, `local.py`, `test.py` - Env settings
- `urls.py` - Routes to portal/places
- `wsgi.py` - Production entry

**Installed Apps:** Django builtins, crispy_forms, django_filters, portal, places.

**URLs:** `/admin/`, `/accounts/`, `/`, `/places/`.

### Places App (`places/`)
**Models:**
- [`Restaurant`](places/models.py): name, desc, addr, lat/lng, min/max_party, yelp_link; methods: [`get_average_rating()`](places/models.py), [`get_distance_to()`](places/models.py), [`get_absolute_url()`](places/models.py); relations: reviews (1:N), categories (M:N); unique: addr, yelp_link.
- [`Review`](places/models.py): title, body, rating (1-5); relations: FK to Restaurant/User; unique: (place, author).
- [`Category`](places/models.py): name; M:N with Restaurant.

**Views:**
- [`HomeView`](places/views.py) - Search form redirect
- [`RestaurantListView`](places/views.py) - Paginated list (15/page) w/ filters
- [`RestaurantDetailView`](places/views.py) - Details + reviews
- [`RestaurantUpdateView`](places/views.py) - Edit (login + perm)
- [`RestaurantRandomView`](places/views.py) - Random pick
- [`RestaurantReviewView`](places/views.py) - Create/update review (login)

**Forms:** [`ReviewForm`](places/forms.py), [`RestaurantForm`](places/forms.py).

**Filters:** [`RestaurantFilter`](places/filters.py) - name (icontains), category (icontains), min_party (>=), max_party (<=).

**URLs:** `/places/` (home), `/restaurants/` (list), `/<pk>/` (detail), `/<pk>/update/`, `/random/`, `/<id>/review/`.

**Mgmt Cmd:** [`loaddemo.py`](places/management/commands/loaddemo.py) - Load demo data (users: admin/john/jane, restaurants, categories, reviews).

**Templates:** home.html, restaurant_list.html, restaurant_detail.html, restaurant_review.html, restaurant_update.html.

**Tests:** models/, views/, forms/.

### Portal App (`portal/`)
**Models:** [`Profile`](portal/models.py) - user (1:1), bio, addr, birth_date; auto-created via signal.

**Views:**
- [`HomeView`](portal/views.py) - Landing
- [`ProfileSignupView`](portal/views.py) - Signup w/ profile
- [`ProfileDetailView`](portal/views.py) - View profile (login)
- [`ProfileUpdateView`](portal/views.py) - Edit profile (login)

**Forms:** [`UserForm`](portal/forms.py), [`ProfileForm`](portal/forms.py).

**URLs:** `/` (home), `/signup/`, `/profile/`, `/profile/update/`.

**Template Tags:** [`navbar_extras.py`](portal/templatetags/navbar_extras.py) - nav_active; [`query_extras.py`](portal/templatetags/query_extras.py) - query utils.

**Templates:** home.html, profile_detail.html, profile_signup.html, profile_update.html.

### Templates (`templates/`)
- `core/base.html` - Layout w/ Bootstrap, nav, footer
- `core/navigation.html` - Nav bar
- Error pages: 400-500.html
- Auth: registration/ (login, logout, pwd reset)
- Reusable: form.html, simple.html

### Static (`staticfiles/`)
- CSS: bootstrap.min.css, style.css
- JS: bootstrap.min.js, popper.min.js
- Icons: favicons
- Download: download.sh

## Database Schema

```
User (builtin)
  ├─ 1:1 → Profile
  └─ 1:N → Review

Restaurant
  ├─ 1:N → Review
  └─ M:N → Category
```

**Constraints:** Review unique (place, author); Restaurant unique addr/yelp_link; Profile auto via signal.

## Auth & Permissions

- Django auth; login req for profiles, updates, reviews
- LOGIN_REDIRECT_URL: portal:home
- Pwd reset via email
- Perms: places.change_restaurant for updates
- User types: Anon (browse), Auth (reviews/profile), Staff/Admin (edit)

## Development Workflow

**Setup:** venv, pip install, migrate, loaddemo, runserver.

**Demo Users:** admin/admin, john/john, jane/jane.

**Docker:** docker-compose up --build.

**Testing:** python manage.py test (80% coverage).

**Code Quality:** ruff format/check, isort (pyproject.toml).

## Key Patterns

- CBVs w/ mixins (LoginRequired, PermissionRequired)
- Signals for profile creation
- Crispy forms, django-filters
- Template inheritance, URL namespaces

## Data Details

- Restaurant: Geo decimals, party constraints, avg rating calc, distance (Pythag), Yelp link
- Review: Rating enum (1-5), unique per user/restaurant, ordered by rating
- Profile: Optional fields, 1:1 w/ User

## Workflows

- Discovery: Search → filter → paginated list
- Review: Detail → review link → form → save
- Signup: Form → User + Profile → home
- Profile: View → update → save

## Important Files

- Config: chowist/settings/base.py, urls.py, manage.py, requirements.txt, pyproject.toml
- Data: places/models.py, portal/models.py
- Logic: places/views.py, portal/views.py, places/filters.py
- UI: templates/core/base.html, places/templates/, portal/templates/
- Data: places/management/commands/loaddemo.py

## Extensions

- New models: Add to models.py, migrate
- New views: Add CBV/FBV, update urls.py
- New templates: Extend base.html
- New filters: Add to filters.py
- New forms: ModelForm/Form

**Customizations:** Review photos, geo search, social features, rating breakdown, owner claims.

## Testing

- Models: Constraints, methods, signals
- Views: URLs, perms, forms, filters, pagination
- Forms: Validation, rendering
- Coverage: 80%, focus biz logic/integration

## Production

- Deploy: Gunicorn, Nginx/Apache static, DEBUG=False, ALLOWED_HOSTS, env SECRET_KEY
- DB: PostgreSQL, migrate, collectstatic
- Security: CSRF, pwd validators, auth flow, ORM protection
- Logging: Console/file/mail admins, timed rotation

## Quick Ref

**Cmds:**
```
python manage.py runserver
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddemo .demo/places.json
python manage.py test
python manage.py collectstatic
docker-compose up --build
```

**Validation:**
```
ruff check
mypy chowist places portal
```

**Install:** Virtual environment with latest Python possible at `./venv`. Use `requirements.txt` to install dependencies.

**URLs:** /admin/, /, /places/, /places/restaurants/, /profile/, /accounts/login/

**Relations:** restaurant.reviews.all(), user.reviews.all(), restaurant.categories.all(), user.profile, restaurant.get_average_rating()

**Context:** {{ user }}, {{ request }}, {% static %}, {% url %}, {% load navbar_extras %} or query_extras

---

*For AI agents/developers on Chowist. User docs: README.md.*
