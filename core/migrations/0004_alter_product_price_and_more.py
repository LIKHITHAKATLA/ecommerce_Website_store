# Generated by Django 4.2.17 on 2025-01-14 12:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0003_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(default='0.0'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_available_count',
            field=models.IntegerField(default='0'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ordered', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered', models.BooleanField(default=False)),
                ('order_id', models.CharField(blank=True, default=None, max_length=100, null=True, unique=True)),
                ('datetime_odpayment', models.DateTimeField(auto_now_add=True)),
                ('order_delivered', models.BooleanField(default=False)),
                ('order_received', models.BooleanField(default=False)),
                ('razorpay_order_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=500, null=True)),
                ('razorpay_signature', models.CharField(blank=True, max_length=500, null=True)),
                ('items', models.ManyToManyField(to='core.orderitem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
