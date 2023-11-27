# Generated by Django 4.2 on 2023-11-25 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakebox', '0002_rename_is_active_category_is_available'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cakes',
            old_name='Category',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='cakes',
            name='flavour',
            field=models.CharField(choices=[('chocolate', 'chocolate'), ('vancho', 'vancho'), ('redbee', 'redbee'), ('black forest', 'black forest'), ('red velvet', 'red velvet'), ('cheese cake', 'cheese cake'), ('rainbow cake', 'rainbow cake'), ('coffee cake', 'coffee cake'), ('non-alcoholic', 'non-alcoholic'), ('butter  scotch', 'butter scotch'), ('vanilla', 'vanilla'), ('mango', 'mango'), ('pineapple', 'pineapple'), ('dates', 'dates'), ('plum', 'plum'), ('dry-fruits', 'dry-fruits'), ('mixed-fruits', 'mixed-fruits'), ('blueberry', 'blueberry'), ('strawberry', 'strawberry')], default='chocolate', max_length=200),
        ),
    ]