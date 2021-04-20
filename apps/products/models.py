from django.db import models
from django.db.models.deletion import CASCADE
from simple_history.models import HistoricalRecords

from apps.base.models import BaseModel

class MeasureUnit(BaseModel):
    """Model definition for Measure."""

    # TODO: Define fields here
    description = models.CharField('Descripción',max_length=50,blank=False,null=False,unique=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        """Meta definition for Measure."""

        verbose_name = 'Unidad de Medida'
        verbose_name_plural = 'Unidades de Medida'

    def __str__(self):
        """Unicode representation of Measure."""
        return self.description

class CategoryProduct(BaseModel):
    """Model definition for CategoryProduct."""

    # TODO: Define fields here
    description = models.CharField('Descripción',max_length=50,blank=False,null=False,unique=True)
    measure_unit = models.ForeignKey(MeasureUnit,on_delete=CASCADE,verbose_name='Unida de MEdida')
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        """Meta definition for CategoryProduct."""

        verbose_name = 'Categoria de Producto'
        verbose_name_plural = 'Categorias de Productos'

    def __str__(self):
        """Unicode representation of CategoryProduct."""
        return self.description

class Indicator(BaseModel):
    """Model definition for Indicator."""

    # TODO: Define fields here
    discount_value = models.PositiveSmallIntegerField(default=0)
    category_product = models.ForeignKey(CategoryProduct, verbose_name="Indicador de oferta", on_delete=models.CASCADE)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value

    class Meta:
        """Meta definition for Indicator."""

        verbose_name = 'Indicador de Oferta'
        verbose_name_plural = 'Indicadores de Ofertas'

    def __str__(self):
        """Unicode representation of Indicator."""
        return f'Oferta de la categoria {self.category_product}: {self.discount_value}%'

class Product(BaseModel):
    """Model definition for Product."""

    # TODO: Define fields here
    name = models.CharField('Nombre de Producto', max_length=150,unique=True,blank=False,null=False)
    description = models.TextField('Descripción de Producto',blank=False,null=False)
    image = models.ImageField('Imagen del Producto', upload_to='products/',blank=True,null=True)
    historical = HistoricalRecords()

    @property
    def _history_user(self):
        return self.changed_by

    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value


    class Meta:
        """Meta definition for Product."""

        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        """Unicode representation of Product."""
        return self.name


