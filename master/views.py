from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from master.fomrs import EmployeeForm
from django.contrib.auth import authenticate, login

from master.models import Employee

from django.contrib import messages
from django.contrib.auth.models import User,auth

# Create your views here.



def index(request):
    return HttpResponse("The Server is up!!")




def display_employee_hierarchy(request):
    # Assuming have a CEO instance as the root of the hierarchy
    ceo = Employee.objects.get(position_name='ceo')

    return render(request, 'employee_tree.html', {'employee': ceo})



def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})



def edit_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'edit_employee.html', {'form': form})



def custom_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
        else:
            # Check if the username is unique
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken.')
            else:
                # Create the user
                user = User.objects.create_user(username=username, password=password1)
             
                user.save()
                messages.success(request, 'Registration successful.')
                return redirect('employee_list') 

    return render(request, 'register.html')

   
def userpro(request):
    if request.user.is_authenticated:
        data=User.objects.all()
       
        context={'data':data}
        return render(request, 'userpro.html',context)
    auth.logout(request)     
    return render(request, 'login.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        #request.session.flush()
        return redirect(login)
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:           
            auth.login(request,user)
            return redirect('userpro')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'login.html') 

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
 
from .serializers import ChangePasswordSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user

            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)