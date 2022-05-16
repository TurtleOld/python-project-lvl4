# Generated by Django 4.0.4 on 2022-05-16 03:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('statuses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('executor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='works', to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(blank=True, related_name='tasks', to='labels.label')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tasks', to='statuses.status')),
            ],
        ),
    ]
