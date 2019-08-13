from django.db import models


class Cinema(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True)
    theater = models.ForeignKey('Theater', on_delete=models.CASCADE)

    def __str__(self):
        return self.name or self.code


class Theater(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name or self.code
