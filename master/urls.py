from django.urls import path, include
from django.views import View
from .import views

urlpatterns = [
    path("", views.index, name="index"),
    path("tree",views.display_employee_hierarchy, name="employee"),
    path('employeet/', views.employee_list, name='employee_list'),
    path('edit-employee/<int:employee_id>/', views.edit_employee, name='edit_employee'),


]