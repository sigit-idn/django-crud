# Generated by Django 3.2.12 on 2022-10-30 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.task')),
            ],
        ),
    ]
