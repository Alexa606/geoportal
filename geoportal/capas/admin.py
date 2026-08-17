from django.contrib import admin
from .models import TestGeometry

# Register your models here.
@admin.register(TestGeometry)
class TestGeometryAdmin(admin.ModelAdmin):
    list_display = ("id","name","created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)
