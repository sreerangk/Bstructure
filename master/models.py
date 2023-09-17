from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    report_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    position_name = models.CharField(max_length=100) 

    def __str__(self):
        return self.user.username