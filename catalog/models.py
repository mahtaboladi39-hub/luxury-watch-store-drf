from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

GENDER_CHOICES = [
    ('men', 'Men'),
    ('women', 'Women'),
    ('unisex', 'Unisex'),
]

ORIGIN_CHOICES = [
    ('swiss', 'Swiss'),
    ('japanese', 'Japanese'),
    ('other', 'Other'),
]

STRAP_MATERIAL_CHOICES = [
    ('leather', 'Leather'),
    ('steel', 'Steel'),
    ('rubber', 'Rubber'),
    ('other', 'Other'),
]

USAGE_CHOICES = [
    ('daily', 'Daily'),
    ('formal', 'Formal'),
    ('sport', 'Sport'),
]

DESIGN_CHOICES = [
    ('classic', 'Classic'),
    ('modern', 'Modern'),
    ('sport', 'Sport'),
]

ENGINE_CHOICES = [
    ('automatic', 'Automatic'),
    ('quartz', 'Quartz'),
    ('mechanical', 'Mechanical'),
]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SluggedMixinModel(models.Model):
    """Abstract mixin that fills `slug` from `slug_source_field`."""

    slug_source_field = 'title'
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(getattr(self, self.slug_source_field)) or 'item'
            candidate, n = base, 2
            while type(self).objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f'{base}-{n}'
                n += 1
            self.slug = candidate
        super().save(*args, **kwargs)


class Brand(BaseModel):
    name = models.CharField(max_length=120, unique=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(BaseModel, SluggedMixinModel):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    @property
    def name(self):
        return self.title

    def __str__(self):
        return self.title


class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone_number = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.user.get_username()


class Product(BaseModel, SluggedMixinModel):
    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)
    gender = models.CharField(max_length=12, choices=GENDER_CHOICES, default='unisex')
    origin = models.CharField(max_length=20, choices=ORIGIN_CHOICES, default='other')
    strap_material = models.CharField(max_length=20, choices=STRAP_MATERIAL_CHOICES, default='other')
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, default='daily')
    design = models.CharField(max_length=20, choices=DESIGN_CHOICES, default='classic')
    engine = models.CharField(max_length=20, choices=ENGINE_CHOICES, default='quartz')
    main_image = models.URLField(blank=True)
    features = models.JSONField(default=dict, blank=True)
    is_luxury = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(blank=True)
    stash = models.PositiveIntegerField(default=0)
    click_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()


class ProductColor(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color = models.CharField(max_length=60)
    hex_code = models.CharField(max_length=7)


class Comment(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()


class WishList(BaseModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['product', 'customer'], name='unique_customer_product_wishlist')]
        ordering = ['-created_at']
