from django.db import models
from  django.contrib.auth.models import User

class Product(models.Model):
    CAT =((0,'stationary'),(1,'mobile'),(2,'electronic'),(3,'random'))
    name = models.CharField(max_length=30, verbose_name='product name')
    price = models.IntegerField()
    cat = models.IntegerField(verbose_name='Categary', choices=CAT)
    pdetail = models.CharField(max_length=300, verbose_name='Product detail')
    is_active = models.BooleanField(default=True)
    pimage = models.ImageField(upload_to = 'image')

    def __str__(self):
        return self.name   ### for showing in admin string

class Cart(models.Model):
    uid = models.ForeignKey('auth.User',on_delete= models.CASCADE,db_column='uid')
    pid = models.ForeignKey('product',on_delete= models.CASCADE,db_column='pid')
    qty = models.IntegerField(default=1)

class Order(models.Model):
    uid = models.ForeignKey('auth.User',on_delete= models.CASCADE,db_column='uid')
    pid = models.ForeignKey('product',on_delete= models.CASCADE,db_column='pid')
    qty = models.IntegerField(default=1)
    amt = models.IntegerField()


