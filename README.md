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

The project uses SQLite by default. `django-debug-toolbar` is enabled automatically when installed; visit `/__debug__/` locally. Set `DEBUG=False`, configure `SECRET_KEY` and `ALLOWED_HOSTS` from environment variables before production deployment.

## API

- `GET /api/products/` — product list with brand/category using `select_related`.
- `GET /api/products/{slug}/` — product details with images, colors and comments prefetched; increments `click_count` atomically.
- `GET /api/luxury-special/` — available products marked special and luxury, with the global average price across luxury products annotated in SQL.
- `GET /api/me/wishlist/` — authenticated user's wishlist with product/customer relationships selected efficiently.

The wishlist endpoint expects a `Customer` profile for the signed-in user. Add products and related content through Django admin.

