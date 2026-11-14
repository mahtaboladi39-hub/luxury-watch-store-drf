from rest_framework import serializers
from catalog.models import Brand, Category, Comment, Customer, Product, ProductColor, ProductImage, WishList


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'meta_title', 'meta_description']


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title', read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'title', 'slug']


class BrandNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class CategoryNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Category
        fields = ['name']


class ProductListSerializer(serializers.ModelSerializer):
    # طبق صورت تمرین: Brand.name و Category.name به‌صورت تودرتو.
    brand = BrandNameSerializer(read_only=True)
    category = CategoryNameSerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'price', 'brand', 'category', 'is_available', 'stash']


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'brand', 'category', 'price',
            'is_discount', 'is_available', 'is_special', 'is_luxury',
            'gender', 'origin', 'strap_material', 'usage', 'design', 'engine',
            'main_image', 'features', 'description', 'meta_title', 'meta_description',
            'stash',
        ]
        # slug از عنوان ساخته می‌شود (SluggedMixinModel)، پس ورودی نیست.
        read_only_fields = ['id', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductColor
        fields = ['id', 'color', 'hex_code']


class CommentSerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source='customer.user.username', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'customer', 'body', 'created_at']


class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    colors = ProductColorSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = '__all__'


class LuxuryProductSerializer(serializers.ModelSerializer):
    average_luxury_price = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    class Meta:
        model = Product
        fields = ['title', 'price', 'gender', 'strap_material', 'engine', 'average_luxury_price']


class WishlistProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'slug', 'price', 'stash', 'main_image']


class WishlistSerializer(serializers.ModelSerializer):
    product = WishlistProductSerializer(read_only=True)
    customer = serializers.SerializerMethodField()
    class Meta:
        model = WishList
        fields = ['id', 'product', 'customer', 'created_at']
    def get_customer(self, obj):
        user = obj.customer.user
        return {'username': user.username, 'email': user.email, 'phone_number': obj.customer.phone_number}
