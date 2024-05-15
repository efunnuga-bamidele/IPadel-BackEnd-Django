from django.db import migrations
from api.user.models import CustomUser


class Migration(migrations.Migration):
    def seed_data(apps, schema_editor):
        user = CustomUser(displayName="Super Admin",
                          email="admin@ipadel.com", is_staff=True, is_superuser=True, isVerified=True, agreeToTerms=True, is_active=True)
        user.set_password("d8iMlgw5JldCd1D")
        user.save()

    dependencies = [

    ]

    operations = [
        migrations.RunPython(seed_data),
    ]
