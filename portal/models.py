from django.db import models

class Control(models.Model):
    control_id = models.CharField(max_length=50, verbose_name="ID")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.control_id} - {self.title}"

class Risk(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
