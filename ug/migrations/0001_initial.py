# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('staff_id', models.IntegerField()),
                ('email_id', models.EmailField(max_length=254)),
                ('designation', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='AdmissionDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.CharField(max_length=4)),
                ('commence_date', models.DateField(auto_now_add=True)),
                ('application_deadline', models.DateField()),
                ('cutoff_marks', models.IntegerField()),
                ('no_of_rounds', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AllotedSeat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=10)),
                ('father_name', models.CharField(max_length=30, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_birth', models.DateField()),
                ('jee_main_marks', models.IntegerField(validators=[django.core.validators.MaxValueValidator(360), django.core.validators.MinValueValidator(-90)])),
                ('jee_main_rank', models.IntegerField()),
                ('high_school_marks', models.IntegerField()),
                ('is_valid', models.BooleanField()),
                ('eligible_for_next_round', models.IntegerField(default=0)),
                ('fees_status', models.IntegerField(default=0)),
                ('applicant', models.ForeignKey(to='ug.Applicant')),
                ('session', models.ForeignKey(to='ug.AdmissionDetail')),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('seats_left', models.IntegerField()),
                ('abbreviation', models.CharField(max_length=3)),
                ('no_of_seats', models.IntegerField()),
                ('session', models.ForeignKey(to='ug.AdmissionDetail')),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.IntegerField()),
                ('application', models.ForeignKey(to='ug.Application')),
                ('branch', models.ForeignKey(to='ug.Branch')),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('roundNumber', models.IntegerField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('fees_deadline', models.DateField()),
                ('concluded', models.BooleanField(default=False)),
                ('part_of', models.ForeignKey(to='ug.AdmissionDetail')),
            ],
        ),
        migrations.CreateModel(
            name='WaitingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('waiting', models.IntegerField()),
                ('application', models.ForeignKey(to='ug.Application')),
                ('branch', models.ForeignKey(to='ug.Branch')),
                ('councelling_round', models.ForeignKey(to='ug.Round')),
            ],
        ),
        migrations.AddField(
            model_name='allotedseat',
            name='application',
            field=models.ForeignKey(to='ug.Application'),
        ),
        migrations.AddField(
            model_name='allotedseat',
            name='branch',
            field=models.ForeignKey(to='ug.Branch'),
        ),
        migrations.AddField(
            model_name='allotedseat',
            name='councelling_round',
            field=models.ForeignKey(to='ug.Round'),
        ),
        migrations.AddField(
            model_name='adminprofile',
            name='session',
            field=models.ForeignKey(to='ug.AdmissionDetail'),
        ),
        migrations.AddField(
            model_name='adminprofile',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='preference',
            unique_together=set([('application', 'branch')]),
        ),
        migrations.AlterUniqueTogether(
            name='application',
            unique_together=set([('applicant', 'session')]),
        ),
    ]
