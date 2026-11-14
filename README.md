# Luxury Watch Store API

Django REST Framework API for a luxury watch catalog, based on the supplied assignment.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The project uses **PostgreSQL** by default. Create the database and role once:

```sql
CREATE ROLE watch_store LOGIN PASSWORD 'watch_store' CREATEDB;
CREATE DATABASE watch_store OWNER watch_store;
```

Then copy `.env.example` to `.env` and adjust it if your server is not on `127.0.0.1:5432`
(SQLite is still available with `DB_ENGINE=django.db.backends.sqlite3`).
`django-debug-toolbar` is enabled automatically when installed; visit `/__debug__/` locally.

Configuration is read from environment variables (or the optional `.env` file):

| Variable | Default | Purpose |
|---|---|---|
| `DJANGO_SECRET_KEY` | insecure dev key | production secret key |
| `DJANGO_DEBUG` | `1` | set to `0` to disable debug mode |
| `DJANGO_ALLOWED_HOSTS` | empty | comma-separated hostnames, e.g. `example.com,www.example.com` |
| `DB_NAME` | `watch_store` | database name |
| `DB_USER` | `watch_store` | database user |
| `DB_PASSWORD` | `watch_store` | database password |
| `DB_HOST` | `127.0.0.1` | database host |
| `DB_PORT` | `5432` | database port |
| `DB_ENGINE` | PostgreSQL | set to `django.db.backends.sqlite3` to use SQLite |

## API

- `GET /api/products/` — product list with nested `brand: {name}` and `category: {name}`, using `select_related` (single query).
- `POST /api/products/create/` — create a product; the slug is generated from the title.
- `GET /api/products/{slug}/` — product details with images, colors and comments prefetched; increments `click_count` atomically.
- `GET /api/luxury-special/` — available products marked special and luxury, with the global average price across luxury products annotated in SQL.
- `GET /api/me/wishlist/` — authenticated user's wishlist with product/customer relationships selected efficiently.

Product images are real file uploads: send `main_image` as `multipart/form-data` when creating a product (or add `ProductImage` rows in Django admin). Files are stored under `MEDIA_ROOT` and served from `/media/` while `DEBUG=True`.

The wishlist endpoint expects a `Customer` profile for the signed-in user. Products can be created through the `POST /api/products/create/` endpoint or Django admin.

