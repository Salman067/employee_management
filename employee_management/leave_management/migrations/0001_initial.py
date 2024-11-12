# Generated by Django 3.2.25 on 2024-11-11 19:16

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('full_name', models.CharField(max_length=100)),
                ('user_type', models.CharField(choices=[('employee', 'Employee'), ('reliever', 'Reliever'), ('supervisor', 'Supervisor'), ('hr', 'HR')], max_length=10)),
                ('employee_id', models.CharField(default='unknown', max_length=255, unique=True)),
                ('thumbnail', models.URLField()),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('admin_name', models.CharField(max_length=100)),
                ('admin_email', models.EmailField(max_length=100)),
                ('designation', models.CharField(max_length=100)),
                ('username', models.CharField(blank=True, max_length=100, unique=True)),
                ('role', models.CharField(default='admin', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(max_length=100, unique=True)),
                ('department_short_name', models.CharField(default='unknown', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('total_days', models.IntegerField()),
                ('reason', models.TextField()),
                ('pdf_path', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(choices=[('pending_reliever', 'Pending Reliever'), ('rejected_by_reliever', 'Rejected by Reliever'), ('pending_supervisor', 'Pending Supervisor'), ('rejected_by_supervisor', 'Rejected by Supervisor'), ('pending_hr', 'Pending HR'), ('rejected_by_hr', 'Rejected by HR'), ('approved', 'Approved')], default='pending_reliever', max_length=25)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LeaveType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leave_name', models.CharField(max_length=50)),
                ('max_days', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LeaveHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_timestamp', models.DateTimeField(auto_now_add=True)),
                ('old_status', models.CharField(blank=True, max_length=50)),
                ('new_status', models.CharField(max_length=50)),
                ('comments', models.TextField(blank=True, null=True)),
                ('action_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='leave_management.leaveapplication')),
            ],
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='leave_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_management.leavetype'),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='reliever',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reliever_for', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='leaveapplication',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_for', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_management.department'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='custom_user_groups', to='auth.Group'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='custom_user_permissions', to='auth.Permission'),
        ),
        migrations.CreateModel(
            name='LeaveBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('available_days', models.IntegerField()),
                ('used_days', models.IntegerField(default=0)),
                ('leave_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='leave_management.leavetype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'leave_type', 'year')},
            },
        ),
    ]