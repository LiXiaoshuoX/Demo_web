# Generated by Django 5.1.6 on 2025-02-11 01:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Dash", "0002_alter_permission_perm_code"),
    ]

    operations = [
        migrations.RenameField(
            model_name="userinfo",
            old_name="role",
            new_name="roles",
        ),
    ]
