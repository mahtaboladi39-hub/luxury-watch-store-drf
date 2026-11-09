from django.contrib import admin
from catalog.models import Brand, Category, Comment, Customer, Product, ProductColor, ProductImage, WishList

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'category', 'price', 'is_available', 'is_luxury', 'is_special')
    list_filter = ('is_available', 'is_luxury', 'is_special', 'brand', 'category')
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProductImageInline, ProductColorInline]

admin.site.register([Brand, Category, Comment, Customer, ProductImage, ProductColor, WishList])
