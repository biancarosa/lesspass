# Generated by Django 3.0.7 on 2020-07-25 23:26
import uuid
import binascii
import bcrypt

from django.conf import settings
from django.db import migrations, models
from backports.pbkdf2 import pbkdf2_hmac
import django.db.models.deletion


def generate_password_profiles_encryption_key():
    salt = bcrypt.gensalt()
    passwd = bcrypt.gensalt()
    iterations = 50000
    derived_key_len = 32
    key = pbkdf2_hmac("sha256", passwd, salt, iterations, derived_key_len)
    return binascii.hexlify(key)


def populate_with_default_key(apps, schema_editor):
    User = apps.get_model("lesspass", "User")
    db_alias = schema_editor.connection.alias
    total = User.objects.using(db_alias).count()
    objs = [{'default_encryption_key': generate_password_profiles_encryption_key()}
            for i in range(total)]
    User.objects.using(db_alias).bulk_update(objs, ['default_encryption_key'])


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_change_default_password_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesspassuser',
            name='has_password_profile_encrypted',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='EncryptedPasswordProfiles',
            fields=[
                ('created', models.DateTimeField(
                    auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(
                    auto_now=True, verbose_name='modified')),
                ('id', models.UUIDField(default=uuid.uuid4,
                                        editable=False, primary_key=True, serialize=False)),
                ('password_profile', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='encrypted_password_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(generate_encryption_key),
    ]
