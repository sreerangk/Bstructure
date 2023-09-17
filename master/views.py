from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from master.fomrs import EmployeeForm

from master.models import Employee

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

