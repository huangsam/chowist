# AGENTS.md

## Project Overview

**Chowist** is a Django-based web application that replicates core features of Yelp with additional functionality. It allows users to discover restaurants, write reviews, and manage their profiles. The application emphasizes user-generated content and social features around restaurant discovery.

**Tech Stack:**
- Django 5.2+ (Python web framework)
- Bootstrap 5 (Frontend CSS framework)
- django-crispy-forms with Bootstrap 5 support
- django-filters (for dynamic filtering)
- PostgreSQL-ready (with SQLite for development)
- Docker support for containerized deployment

**Key Features:**
- User authentication and profile management
- Restaurant browsing with search and filtering
- Review and rating system (1-5 star ratings)
- Category-based restaurant organization
- Geolocation support (latitude/longitude)
- Pagination for restaurant listings
- Permission-based access control

## Project Structure

### Core Django Configuration (`chowist/`)

The main Django project directory containing settings and URL routing:

**Files:**
- `settings/base.py` - Base configuration with installed apps, middleware, templates, static files, and logging
- `settings/dev.py`, `settings/local.py`, `settings/test.py` - Environment-specific settings
- `urls.py` - Root URL configuration mapping to portal and places apps
- `wsgi.py` - WSGI application entry point for production deployment

**Installed Apps:**
1. Django built-in apps (admin, auth, sessions, etc.)
2. `crispy_forms` + `crispy_bootstrap5` - Form rendering
3. `django_filters` - Dynamic filtering
4. `portal` - User management app
5. `places` - Restaurant and review app

**URL Structure:**
- `/admin/` - Django admin interface
- `/accounts/` - Authentication (login, logout, password reset)
- `/` - Portal home page
- `/places/` - Restaurant features

### Places App (`places/`)

The core business logic app handling restaurants, reviews, and categories.

**Models (`models.py`):**

1. **Restaurant**
   - Fields: name, description, address, latitude, longitude, min_party, max_party, yelp_link
   - Methods: `get_average_rating()`, `get_distance_to()`, `get_absolute_url()`
   - Relationships: Has many reviews and categories (ManyToMany)
   - Unique constraints: address, yelp_link

2. **Review**
   - Fields: title, body, rating (1-5 using Rating.IntegerChoices)
   - Relationships: ForeignKey to Restaurant and User
   - Unique constraint: One review per user per restaurant
   - Related name: `reviews` on both Restaurant and User

3. **Category**
   - Fields: name
   - Relationships: ManyToMany with Restaurant
   - Related name: `categories` on Restaurant

**Views (`views.py`):**

1. **HomeView** - Search form for restaurants with redirect to filtered list
2. **RestaurantListView** - Paginated list (15 per page) with filtering support
3. **RestaurantDetailView** - Individual restaurant details with reviews
4. **RestaurantUpdateView** - Edit restaurant (requires login + permission)
5. **RestaurantRandomView** - Random restaurant discovery
6. **RestaurantReviewView** - Create or update review (requires login)

**Forms (`forms.py`):**
- `ReviewForm` - ModelForm for creating/editing reviews
- `RestaurantForm` - Search form with category, name, min_party, max_party filters

**Filters (`filters.py`):**
- `RestaurantFilter` - Uses django-filters for dynamic querying:
  - name: case-insensitive contains
  - category: case-insensitive contains on category name
  - min_party: greater than or equal
  - max_party: less than or equal

**URLs (`urls.py`):**
```
/places/ - Home (search form)
/places/restaurants/ - List view
/places/restaurants/<pk>/ - Detail view
/places/restaurants/<pk>/update/ - Update view
/places/restaurants/random/ - Random restaurant
/places/restaurants/<restaurant_id>/review/ - Review creation/editing
```

**Management Commands:**
- `loaddemo.py` - Loads demo data from JSON file, creates users (admin, john, jane), restaurants, categories, and random reviews

**Templates:**
- `home.html` - Search interface
- `restaurant_list.html` - Paginated grid of restaurant cards
- `restaurant_detail.html` - Detailed restaurant information with reviews
- `restaurant_review.html` - Review form
- `restaurant_update.html` - Restaurant edit form

**Tests:**
- `tests/models/` - Model validation and methods
- `tests/views/` - View logic and permissions
- `tests/forms/` - Form validation

### Portal App (`portal/`)

User profile and authentication management app.

**Models (`models.py`):**

1. **Profile**
   - Fields: user (OneToOne), bio, address, birth_date
   - Auto-created via post_save signal when User is created
   - Extends Django's built-in User model

**Views (`views.py`):**

1. **HomeView** - Portal landing page
2. **ProfileSignupView** - User registration with automatic profile creation
3. **ProfileDetailView** - View own profile (requires login)
4. **ProfileUpdateView** - Edit profile information (requires login)

**Forms (`forms.py`):**
- `UserForm` - User registration form
- `ProfileForm` - Profile editing form

**URLs (`urls.py`):**
```
/ - Portal home
/signup/ - User registration
/profile/ - View profile
/profile/update/ - Edit profile
```

**Template Tags (`templatetags/`):**
- `navbar_extras.py` - `nav_active` tag for highlighting active navigation items
- `query_extras.py` - Template utilities for query parameter handling

**Templates:**
- `home.html` - Portal homepage
- `profile_detail.html` - Profile display
- `profile_signup.html` - Registration form
- `profile_update.html` - Profile edit form

### Templates (`templates/`)

Global template structure with Bootstrap 5 styling.

**Core Templates (`core/`):**
- `base.html` - Base template with:
  - Static file loading
  - Bootstrap CSS/JS
  - Responsive flexbox layout
  - Header with navigation
  - Main content area
  - Footer with copyright
- `navigation.html` - Navigation bar component

**Error Pages:**
- `400.html`, `403.html`, `404.html`, `500.html` - HTTP error handlers

**Auth Templates (`registration/`):**
- Complete authentication flow: login, logout, password reset, password change
- `password_reset_email.html` - Email template for password reset

**Reusable Templates:**
- `form.html` - Generic form rendering with crispy forms
- `simple.html` - Simple page layout extending base

### Static Files (`staticfiles/`)

Frontend assets organized by type:

**CSS:**
- `bootstrap.min.css` - Bootstrap 5 framework
- `style.css` - Custom application styles

**JavaScript:**
- `bootstrap.min.js` - Bootstrap functionality
- `popper.min.js` - Tooltip and popover positioning

**Icons:**
- Favicon files (ICO and SVG formats)

**Download:**
- `download.sh` - Script to fetch/update static dependencies

## Database Schema

**Core Relationships:**
```
User (Django built-in)
  ├─ 1:1 → Profile
  └─ 1:N → Review

Restaurant
  ├─ 1:N → Review
  └─ M:N → Category

Review (junction with data)
  ├─ N:1 → Restaurant
  └─ N:1 → User

Category
  └─ M:N → Restaurant
```

**Key Constraints:**
- Review: Unique together (place, author) - one review per user per restaurant
- Restaurant: Unique fields (address, yelp_link)
- Profile: Auto-created via signal on User creation

## Authentication & Permissions

**Authentication:**
- Django's built-in authentication system
- Login required for: profile views, restaurant updates, review creation
- LOGIN_REDIRECT_URL set to `portal:home`
- Complete password reset flow via email

**Permissions:**
- `RestaurantUpdateView` requires `places.change_restaurant` permission
- Profile management restricted to logged-in users viewing their own profile
- Reviews can only be created/edited by authenticated users

**User Types:**
1. **Anonymous** - Can browse restaurants and view reviews
2. **Authenticated** - Can create reviews and manage profile
3. **Staff/Admin** - Can edit restaurants and access admin panel

## Development Workflow

**Setup:**
1. Create virtualenv: `virtualenv venv && source venv/bin/activate`
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Load demo data: `python manage.py loaddemo .demo/places.json`
5. Start server: `python manage.py runserver`

**Demo Users:**
- `admin` / `admin` - Superuser with all permissions
- `john` / `john` - Normal user
- `jane` / `jane` - Normal user

**Docker Setup:**
```bash
docker-compose -f build/compose/compose.yml --project-directory=. up --build -d
```

**Testing:**
- Test suites in `places/tests/` and `portal/tests/`
- Coverage target: 80% (configured in pyproject.toml)
- Run tests: `python manage.py test`

**Code Quality:**
- Ruff for linting (line-length: 160)
- isort for import sorting
- Configuration in `pyproject.toml`

## Key Design Patterns

**Class-Based Views:**
- Extensive use of Django's generic views (ListView, DetailView, UpdateView, FormView)
- LoginRequiredMixin and PermissionRequiredMixin for access control
- Separation of GET/POST logic in custom View classes

**Model Signals:**
- Profile auto-creation on User post_save signal
- Ensures every user has a profile without manual intervention

**Form Handling:**
- django-crispy-forms for consistent Bootstrap 5 styling
- ModelForms for database-backed forms
- Custom forms for search functionality

**Filtering:**
- django-filters for declarative query filtering
- FilterSet classes define field-level filtering logic
- Integrated with ListView for clean separation

**Template Inheritance:**
- Base template provides consistent layout
- Block system for customization (meta, content, content_title, content_body)
- Reusable components (navigation, forms)

**URL Namespacing:**
- App-level namespaces (`portal:`, `places:`)
- Named URL patterns for reverse lookups
- Prevents URL conflicts between apps

## Data Models Details

**Restaurant Model:**
- Geolocation support with decimal fields (high precision)
- Party size constraints (min_party, max_party)
- Calculated average rating from related reviews
- Distance calculation using Pythagorean theorem (simple 2D distance)
- Integration with Yelp via yelp_link field

**Review Model:**
- Integer choices enum (Rating.IntegerChoices) for star ratings (1-5)
- Composite unique constraint prevents duplicate reviews
- ForeignKey cascades on delete (delete restaurant → delete reviews)
- Ordered by rating by default

**Profile Model:**
- Optional fields (bio, address, birth_date) for gradual user onboarding
- One-to-one relationship with User for clean separation
- Related name `profile` allows `user.profile` access

## Common Workflows

**Restaurant Discovery:**
1. User visits `/places/` (search form)
2. Submits search criteria (name, category, party size)
3. Redirected to `/places/restaurants/` with query parameters
4. RestaurantFilter applies filters to queryset
5. Paginated results displayed with 15 per page

**Review Creation:**
1. User browses to restaurant detail page
2. Clicks review link → `/places/restaurants/<id>/review/`
3. Form pre-populated if existing review found
4. On submit, review created/updated with unique constraint check
5. Redirect back to restaurant detail page

**User Registration:**
1. Visit `/signup/`
2. Fill out UserForm (username, email, password)
3. On success, User created with hashed password
4. Profile auto-created via signal
5. Redirect to portal home

**Profile Management:**
1. Login required to access `/profile/`
2. View shows user info and profile details
3. Click update → `/profile/update/`
4. Edit bio, address, birth_date
5. Save updates profile instance

## Important Files

**Configuration:**
- `chowist/settings/base.py` - Core settings
- `chowist/urls.py` - URL routing
- `manage.py` - Django management script
- `requirements.txt` - Python dependencies
- `pyproject.toml` - Tool configuration

**Data Layer:**
- `places/models.py` - Restaurant, Review, Category
- `portal/models.py` - Profile

**Business Logic:**
- `places/views.py` - Restaurant operations
- `portal/views.py` - User operations
- `places/filters.py` - Query filtering

**Presentation:**
- `templates/core/base.html` - Layout foundation
- `places/templates/places/` - Restaurant UI
- `portal/templates/portal/` - Profile UI

**Data Management:**
- `places/management/commands/loaddemo.py` - Demo data loader

## Extension Points

**Adding Features:**
1. **New Models** - Add to relevant app's models.py, create migration
2. **New Views** - Add class-based or function views, update urls.py
3. **New Templates** - Create in app's templates directory, extend base.html
4. **New Filters** - Add to filters.py with FilterSet syntax
5. **New Forms** - Create ModelForm or Form in forms.py

**Common Customizations:**
- Add review photos (FileField on Review model)
- Restaurant search by geolocation (add distance filter)
- Social features (follow users, bookmark restaurants)
- Rating breakdown (count reviews by star rating)
- Restaurant owner claims (add owner field to Restaurant)

## Testing Strategy

**Model Tests:**
- Validation rules (unique constraints, required fields)
- Model methods (average rating calculation, distance)
- Signal handlers (profile creation)

**View Tests:**
- URL resolution and reverse lookups
- Permission checks (login required, object permissions)
- Form submission and validation
- Query filtering and pagination

**Form Tests:**
- Field validation rules
- Clean methods and custom validation
- Form rendering with crispy forms

**Coverage:**
- Target: 80% minimum (configured in pyproject.toml)
- Focus on business logic and edge cases
- Integration tests for multi-step workflows

## Production Considerations

**Deployment:**
- Use Gunicorn for WSGI server: `gunicorn -w 4 chowist.wsgi`
- Serve static files from web server (Nginx/Apache)
- Set DEBUG=False in production settings
- Configure ALLOWED_HOSTS appropriately
- Use environment variables for SECRET_KEY

**Database:**
- SQLite for development
- PostgreSQL recommended for production
- Run migrations: `python manage.py migrate`
- Collect static files: `python manage.py collectstatic`

**Security:**
- CSRF protection enabled by default
- Password validators configured
- Secure authentication flow
- SQL injection protection via ORM

**Logging:**
- Configured in base.py with console and file handlers
- Audit log with timed rotation (hourly, 6 backups)
- Mail admins handler for errors (production only)
- Verbose formatting for debugging

## Quick Reference

**Common Commands:**
```bash
# Start development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load demo data
python manage.py loaddemo .demo/places.json

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic

# Start with Docker
docker-compose -f build/compose/compose.yml --project-directory=. up --build -d
```

**Key URLs:**
- Admin: `/admin/`
- Portal home: `/`
- Places search: `/places/`
- Restaurant list: `/places/restaurants/`
- User profile: `/profile/`
- Login: `/accounts/login/`

**Model Relationships:**
- Access restaurant reviews: `restaurant.reviews.all()`
- Access user reviews: `user.reviews.all()`
- Access restaurant categories: `restaurant.categories.all()`
- Access user profile: `user.profile`
- Get average rating: `restaurant.get_average_rating()`

**Template Context:**
- User: Available as `{{ user }}` in all templates
- Request: Available as `{{ request }}` when context processor enabled
- Static files: Use `{% load static %}` and `{% static 'path' %}`
- URLs: Use `{% url 'app:name' %}` for reverse lookups
- Custom tags: Load with `{% load navbar_extras %}` or `{% load query_extras %}`

---

*This document is intended for AI agents and developers working on the Chowist project. For user-facing documentation, see README.md.*
