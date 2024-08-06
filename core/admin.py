from django.contrib import admin
from core import models
# Register your models here.

admin.site.register(models.Ponto)
admin.site.register(models.Tarefa)
admin.site.register(models.Projeto)
admin.site.register(models.Estado)