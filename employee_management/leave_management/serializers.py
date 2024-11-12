from rest_framework import serializers
from .models import Department, User, LeaveType, LeaveApplication, LeaveHistory, LeaveBalance,Admin

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id','department_name','department_short_name']


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields ='__all__'
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        admin = Admin(**validated_data)
        admin.set_password(password)  
        admin.save()
        return admin
    

class UserSerializer(serializers.ModelSerializer):
    department_name = serializers.SerializerMethodField() 
    department_short_name = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True) 

    class Meta:
        model = User
        fields = [
            'id', 'employee_id', 'username', 'first_name', 'last_name', 'email', 
            'user_type', 'department','department_name', 'department_short_name', 
            'is_active', 'date_joined', 'password','thumbnail'
        ]
        extra_kwargs = {'password': {'write_only': True}}
    
    def get_department_name(self, obj):
        try:
            department = obj.department
            return department.department_name
        except AttributeError:
            return "No Department"  

    def get_department_short_name(self, obj):
        try:
            department = obj.department
            return department.department_short_name
        except AttributeError:
            return "No Department" 
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        return user
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['user_type'].required = False
            self.fields['department'].required = False
            self.fields['password'].required = False
            
            

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'
        

class LeaveApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveApplication
        fields = '__all__'

class LeaveHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveHistory
        fields = '__all__'

class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = '__all__'
