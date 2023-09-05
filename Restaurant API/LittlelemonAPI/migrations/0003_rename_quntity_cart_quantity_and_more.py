# Generated by Django 4.2 on 2023-05-21 09:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LittlelemonAPI', '0002_cart_category_menuitem_order_orderitem_delete_book_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='quntity',
            new_name='quantity',
        ),
        migrations.RemoveField(
            model_name='menuitem',
            name='Category',
        ),
        migrations.AddField(
            model_name='menuitem',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='LittlelemonAPI.category'),
        ),
    ]
