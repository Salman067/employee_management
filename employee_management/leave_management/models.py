from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission,AbstractBaseUser, BaseUserManager



class Department(models.Model):
    department_name = models.CharField(max_length=100, unique=True)
    department_short_name = models.CharField(max_length=100,default='unknown')
    
    def __str__(self):
        return self.department_name
    
    
class AdminManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        admin = self.model(username=username, **extra_fields)
        admin.set_password(password)  # Hashes the password
        admin.save(using=self._db)
        return admin

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(username, password, **extra_fields)

class Admin(AbstractBaseUser):
    admin_name = models.CharField(max_length=100)
    admin_email = models.EmailField(max_length=100)
    designation = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, blank=True)
    role = models.CharField(max_length=100, default='admin')
    objects = AdminManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    

class User(AbstractUser):
    USER_TYPES = [
        ('employee', 'Employee'),
        ('reliever', 'Reliever'),
        ('supervisor', 'Supervisor'),
        ('hr', 'HR')
    ]
    full_name = models.CharField(max_length=100,blank=False)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    employee_id = models.CharField(max_length=255, unique=True, default='unknown') 
    thumbnail = models.URLField()
    designation = models.CharField(max_length=100, null=True)  
    phone_number = models.CharField(max_length=15, null=True) 

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups", 
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions", 
        blank=True
    )

    def __str__(self):
        return f"{self.full_name} ({self.user_type})"
    
class LeaveType(models.Model):
    leave_name = models.CharField(max_length=50)
    max_days = models.IntegerField()
    description = models.TextField()


class LeaveApplication(models.Model):
    STATUS_CHOICES = [
        ('pending_reliever', 'Pending Reliever'),
        ('rejected_by_reliever', 'Rejected by Reliever'),
        ('pending_supervisor', 'Pending Supervisor'),
        ('rejected_by_supervisor', 'Rejected by Supervisor'),
        ('pending_hr', 'Pending HR'),
        ('rejected_by_hr', 'Rejected by HR'),
        ('approved', 'Approved')
    ]

    employee = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    reliever = models.ForeignKey(User, related_name='reliever_for', on_delete=models.CASCADE)
    supervisor = models.ForeignKey(User, related_name='supervisor_for', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days=models.IntegerField()
    reason = models.TextField()
    pdf_path = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending_reliever')
    created_at = models.DateTimeField(auto_now_add=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    leave_address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_number = models.CharField(max_length=15, blank=True, null=True)
    reliever_name = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type} ({self.status})"
    


class LeaveHistory(models.Model):
    application = models.ForeignKey(LeaveApplication, related_name='history', on_delete=models.CASCADE)
    action_by = models.ForeignKey(User, on_delete=models.CASCADE)
    action_timestamp = models.DateTimeField(auto_now_add=True)
    old_status = models.CharField(max_length=50, blank=True)
    new_status = models.CharField(max_length=50)
    comments = models.TextField(blank=True, null=True)

class LeaveBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    year = models.IntegerField()
    available_days = models.IntegerField()
    used_days = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'leave_type', 'year')

