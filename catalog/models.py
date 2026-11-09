from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Brand(TimeStampedModel):
    name = models.CharField(max_length=120, unique=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    @property
    def name(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Customer(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.user.get_username()


class Product(TimeStampedModel):
    class Gender(models.TextChoices):
        MEN = 'men', 'Men'
        WOMEN = 'women', 'Women'
        UNISEX = 'unisex', 'Unisex'
    class Origin(models.TextChoices):
        SWISS = 'swiss', 'Swiss'
        JAPANESE = 'japanese', 'Japanese'
        OTHER = 'other', 'Other'
    class StrapMaterial(models.TextChoices):
        LEATHER = 'leather', 'Leather'
        STEEL = 'steel', 'Steel'
        RUBBER = 'rubber', 'Rubber'
        OTHER = 'other', 'Other'
    class Usage(models.TextChoices):
        DAILY = 'daily', 'Daily'
        FORMAL = 'formal', 'Formal'
        SPORT = 'sport', 'Sport'
    class Design(models.TextChoices):
        CLASSIC = 'classic', 'Classic'
        MODERN = 'modern', 'Modern'
        SPORT = 'sport', 'Sport'
    class Engine(models.TextChoices):
        AUTOMATIC = 'automatic', 'Automatic'
        QUARTZ = 'quartz', 'Quartz'
        MECHANICAL = 'mechanical', 'Mechanical'

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    is_discount = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_special = models.BooleanField(default=False)
    gender = models.CharField(max_length=12, choices=Gender.choices, default=Gender.UNISEX)
    origin = models.CharField(max_length=20, choices=Origin.choices, default=Origin.OTHER)
    strap_material = models.CharField(max_length=20, choices=StrapMaterial.choices, default=StrapMaterial.OTHER)
    usage = models.CharField(max_length=20, choices=Usage.choices, default=Usage.DAILY)
    design = models.CharField(max_length=20, choices=Design.choices, default=Design.CLASSIC)
    engine = models.CharField(max_length=20, choices=Engine.choices, default=Engine.QUARTZ)
    main_image = models.URLField(blank=True)
    features = models.JSONField(default=dict, blank=True)
    is_luxury = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    meta_title = models.CharField(max_length=160, blank=True)
    meta_description = models.TextField(blank=True)
    stash = models.PositiveIntegerField(default=0)
    click_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['is_available', 'is_special', 'is_luxury'])]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)
            candidate = base
            n = 2
            while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f'{base}-{n}'
                n += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.URLField()


class ProductColor(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='colors')
    color = models.CharField(max_length=60)
    hex_code = models.CharField(max_length=7)


class Comment(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()


class WishList(TimeStampedModel):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlisted_by')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['product', 'customer'], name='unique_customer_product_wishlist')]
        ordering = ['-created_at']
