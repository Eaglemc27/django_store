from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name.replace('_', ' ')

    class Meta:
        verbose_name_plural = 'categories'


class State(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class DeliveryType(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=32)
    category = models.ForeignKey(Category)
    price = models.IntegerField()
    in_stock = models.BooleanField()

    def __str__(self):
        return self.title


class BoardGame(models.Model):
    players = models.IntegerField()
    playing_time = models.IntegerField()
    age = models.CharField(max_length=16)
    complexity = models.FloatField()
    product = models.ForeignKey(Product)

    def __str__(self):
        return self.product.title


class Review(models.Model):
    product = models.ForeignKey(Product)
    date = models.DateField()
    region = models.CharField(max_length=32)


class Customer(models.Model):
    username = models.CharField(max_length=16)
    first_name = models.CharField(max_length=16)
    last_name = models.CharField(max_length=16)
    address = models.CharField(max_length=16)
    email = models.CharField(max_length=16)


class Order(models.Model):
    state = models.ForeignKey(State)
    date = models.DateField()
    delivery_type = models.ForeignKey(DeliveryType)
    product = models.ForeignKey(Product)
    customer = models.ForeignKey(Customer)
    price = models.IntegerField()

