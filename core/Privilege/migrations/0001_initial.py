# Generated by Django 3.2.12 on 2022-09-05 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivilegeUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_stamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('modified_stamp', models.DateTimeField(auto_now=True)),
                ('archived_stamp', models.DateTimeField(null=True)),
                ('archived_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'privilege_user',
            },
        ),
        migrations.CreateModel(
            name='PrivilegeMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1024)),
                ('privilege_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='Privilege.privilegeuser')),
            ],
            options={
                'db_table': 'privilege_message',
            },
        ),
    ]