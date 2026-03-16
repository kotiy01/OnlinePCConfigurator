from django.db import models
from components.models import CPU

class CPUPrice(models.Model):
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE, related_name='prices')
    shop_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)
    url = models.URLField(max_length=500)

    class Meta:
        unique_together = ('cpu', 'shop_name')