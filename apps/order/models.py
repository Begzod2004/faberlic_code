from django.db import models
from django.conf import settings
from apps.product.models import Product
# from apps.accounts.models import User

CONTACT_STATUS = (
    (0,"New"),
    (1,"Prosess"),
    (2,"Canceled"),
    (3,"Finished")
)

class Order(models.Model):
    code = models.CharField(max_length=30,blank=True, unique=True)    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.IntegerField(choices=CONTACT_STATUS, default=0)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        orde = Order.objects.last()
        if orde is not None:
            code = str(orde.pk + 1)
        else:
            code = str(1) 
        nols = "0" * (7 - len(code)) + code
        self.code = f"{self.user.full_name[:1]}" + nols
        return super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.code)       

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
    count = models.PositiveIntegerField()
