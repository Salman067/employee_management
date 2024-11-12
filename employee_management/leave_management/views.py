
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User,Admin,Department,LeaveType
from .serializers import UserSerializer,DepartmentSerializer,LeaveTypeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash


# Department
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_department(request):
    if request.user.user_type == 'admin':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'id':serializer.data.get('id'),"message":"Department created successfully"},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors)
    else:
        return Response(
            {"error": "Only Admin can create new department"},
            status=status.HTTP_403_FORBIDDEN
        )
        
@api_view(["PUT",'DELETE'])
@permission_classes([IsAuthenticated])   
def updated_deleted_department(request,id):
    if request.user.user_type == 'admin':
        if request.method == 'PUT':
            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(department, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Department updated successfully"},status=status.HTTP_200_OK)
            print(serializer.errors)
            return Response(serializer.errors)
        elif request.method == 'DELETE':
            department = Department.objects.get(id=id)
            department.delete()
            return Response({"message": "Department deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response(
            {"error": "Only Admin can update or delete department"},
            status=status.HTTP_403_FORBIDDEN
        )



    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_department(request,id=None):
    
    if id:
         try:
            department = Department.objects.get(id=id)
            serializer = DepartmentSerializer(department)
            return Response(serializer.data)
         except Department.DoesNotExist:
            return Response(
                {"error": "Department not found."},
                status=status.HTTP_404_NOT_FOUND
            )
    else:
         try:
            department = Department.objects.all()
            serializer = DepartmentSerializer(department,many=True)
            return Response(serializer.data)
         except Department.DoesNotExist:
            return Response(
                {"error": "Department not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        

# user 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_get_view(request,username):
         try:
            user = User.objects.get(username=username)
            serializer = UserSerializer(user)
            return Response(serializer.data)
         except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_get_list(request):
    if request.user.user_type in ['hr', 'admin']:
        department_id = request.query_params.get('department_id')
        
        if department_id:
            users = User.objects.filter(department=department_id)
        else:
            users = User.objects.all()
        
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    else:
        return Response(
            {"error": "Only Admin or HR can get users."},
            status=status.HTTP_403_FORBIDDEN
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_by_user_id(request, id):
         try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
         except Department.DoesNotExist:
            return Response(
                {"error": "Employee not found."},
                status=status.HTTP_404_NOT_FOUND
            )

    
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def register_user(request):
    if request.user.user_type in ['hr', 'admin']:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"id":serializer.data.get('id'),"message":"Employee registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"error": "Only Admin or HR can register new users."},
            status=status.HTTP_403_FORBIDDEN 
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    print(f"Received username: {username}, password: {password}")

    try:
        user = User.objects.get(username=username)
        if user.check_password(password): 
            refresh = RefreshToken.for_user(user)
            refresh['user_type'] = user.user_type  
            refresh['username'] = user.username
            refresh['email'] = user.email
            
            response = Response({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            })
            response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True)
            return response
        else:
            return Response({"error": "Invalid username or password"}, status=400)
    except User.DoesNotExist:
        return Response({"error": "User does not exist"}, status=400)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsAuthenticated])   
def updated_deleted_user(request, id):
    if request.method == 'PATCH':
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"id": serializer.data.get('id'), "message": "Employee updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        if request.user.user_type in ['hr', 'admin']:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
            user.delete()
            return Response({"message": "User deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {"error": "Only Admin or HR can delete users."},
                status=status.HTTP_403_FORBIDDEN
            )

# admin login
@api_view(['POST'])
@permission_classes([AllowAny])
def login_admin(request):
    username = request.data.get("username")
    password = request.data.get("password")
    print(f"Received username: {username}, password: {password}")

    try:
        admin = Admin.objects.get(username=username)
        if admin.check_password(password): 
            refresh = RefreshToken.for_user(admin)
            response = Response({
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
            })
            response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True)
            return response
        else:
            return Response({"error": "Invalid credentials"}, status=400)
    except Admin.DoesNotExist:
        return Response({"error": "Admin does not exist"}, status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)
    old_password = request.data.get("old_password")
    new_password = request.data.get("new_password")

    if not old_password or not new_password:
        return Response({"error": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not user.check_password(old_password):
        return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

    if old_password == new_password:
        return Response({"error": "New password cannot be the same as the old password"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()

    update_session_auth_hash(request, user)

    return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
        response=Response()
        response.delete_cookie('access_token')
        response.data={'message':'logout successful'}
        return response


# Leave Type
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def create_leave_type(request):
    if request.user.user_type in ['hr', 'admin']:
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"id":serializer.data.get('id'),"message":"Leave type create successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(
            {"error": "Only Admin or HR can create new leave type."},
            status=status.HTTP_403_FORBIDDEN 
        )
