from django.contrib.gis.db import models

# Create your models here.
class TestGeometry(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Nombre"
    )

    geometry = models.GeometryField(
        srid=4326,
        verbose_name="Geometría"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Test de Geometría"
        verbose_name_plural = "Tests de Geometría"
