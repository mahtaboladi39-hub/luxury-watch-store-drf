from django.db import migrations, models


def clear_url_values(apps, schema_editor):
    """Old rows stored image URLs; those strings are not files under MEDIA_ROOT."""
    Product = apps.get_model('catalog', 'Product')
    ProductImage = apps.get_model('catalog', 'ProductImage')
    Product.objects.exclude(main_image='').update(main_image='')
    ProductImage.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_remove_wishlist_unique_customer_product_wishlist_and_more'),
    ]

    operations = [
        migrations.RunPython(clear_url_values, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='product',
            name='main_image',
            field=models.ImageField(blank=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='products/'),
        ),
    ]
