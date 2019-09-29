from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    department = models.ForeignKey('Department', null=False, on_delete=models.CASCADE)
    skills_set = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}_{}".format(self.pk, self.name)
