from django.db import migrations


def create_defaults(apps, schema_editor):
    Location = apps.get_model('dashboard', 'Location')
    AppearanceSetting = apps.get_model('dashboard', 'AppearanceSetting')
    order = [
        ('TRANS', 'trans'),
        ('P1', 'p1'),
        ('P2', 'p2'),
        ('P3', 'p3'),
        ('P4', 'p4'),
        ('STREFY', 'strefy'),
    ]
    for index, (name, slug) in enumerate(order):
        Location.objects.get_or_create(slug=slug, defaults={'name': name, 'order': index})
    AppearanceSetting.objects.get_or_create(key='default', defaults={'data': {}})


def reverse_defaults(apps, schema_editor):
    Location = apps.get_model('dashboard', 'Location')
    AppearanceSetting = apps.get_model('dashboard', 'AppearanceSetting')
    Location.objects.filter(slug__in=['trans', 'p1', 'p2', 'p3', 'p4', 'strefy']).delete()
    AppearanceSetting.objects.filter(key='default').delete()


class Migration(migrations.Migration):
    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_defaults, reverse_defaults),
    ]
