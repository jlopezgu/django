from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.DateTimeField(null=True, blank=True)
    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['created']
