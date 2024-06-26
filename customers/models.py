from django.db import models

from account.models import CustomUser

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(
        CustomUser, related_name="customers", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.first_name + " " + self.last_name
