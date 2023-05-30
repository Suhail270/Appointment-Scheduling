# Generated by Django 4.1.6 on 2023-05-30 11:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sales", "0003_remove_customer_organization_customer_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="customer",
            name="organization",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="sales.userprofile",
            ),
        ),
        migrations.AlterField(
            model_name="timechoices",
            name="choice",
            field=models.CharField(max_length=19),
        ),
    ]
