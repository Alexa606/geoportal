from django.contrib.auth import get_user_model
from django.contrib.gis.db import models

User = get_user_model()


class TestGeometry(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    geometry = models.GeometryField(srid=4326, verbose_name="Geometria")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creacion",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Test de Geometria"
        verbose_name_plural = "Tests de Geometria"


class UploadedLayer(models.Model):
    FORMAT_CHOICES = (
        ("shp", "Shapefile ZIP"),
        ("geojson", "GeoJSON"),
    )

    STATUS_CHOICES = (
        ("pending", "Pendiente"),
        ("valid", "Valido"),
        ("processed", "Procesado"),
        ("error", "Error"),
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Nombre de la capa",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripcion",
    )
    source_file = models.FileField(
        upload_to="layers/%Y/%m/",
        verbose_name="Archivo geoespacial",
    )
    file_format = models.CharField(
        max_length=20,
        choices=FORMAT_CHOICES,
        blank=True,
        editable=False,
        verbose_name="Formato",
    )
    source_epsg = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
        verbose_name="EPSG original",
    )
    storage_epsg = models.IntegerField(
        default=4326,
        editable=False,
        verbose_name="EPSG de almacenamiento",
    )
    geometry_type = models.CharField(
        max_length=50,
        blank=True,
        editable=False,
        verbose_name="Tipo de geometria",
    )
    feature_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        verbose_name="Numero de elementos",
    )
    file_hash = models.CharField(
        max_length=64,
        unique=True,
        editable=False,
        verbose_name="SHA-256",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        editable=False,
        verbose_name="Estado",
    )
    validation_message = models.TextField(
        blank=True,
        editable=False,
        verbose_name="Resultado de validacion",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="uploaded_layers",
        verbose_name="Usuario que realizo la carga",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de carga",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ultima actualizacion",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Capa cargada"
        verbose_name_plural = "Capas cargadas"
        ordering = ("-created_at",)


class UploadedFeature(models.Model):
    layer = models.ForeignKey(
        UploadedLayer,
        on_delete=models.CASCADE,
        related_name="features",
        verbose_name="Capa",
    )
    geometry = models.GeometryField(
        srid=4326,
        spatial_index=True,
        verbose_name="Geometria",
    )
    properties = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Atributos",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creacion",
    )

    def __str__(self):
        return f"{self.layer.name} - {self.pk}"

    class Meta:
        verbose_name = "Elemento geografico"
        verbose_name_plural = "Elementos geograficos"
