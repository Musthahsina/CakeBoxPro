from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class User(AbstractUser):

    phone=models.CharField(max_length=100,unique=True)
    address=models.CharField(max_length=200)


class Category(models.Model):

    name=models.CharField(max_length=200,unique=True)
    is_available=models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class Cakes(models.Model):
    name=models.CharField(max_length=200)


    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    options=(
        ('chocolate','chocolate'),
        ('vancho','vancho'),
        ('redbee','redbee'),
        ('black forest','black forest'),
        ('red velvet','red velvet'),
        ('cheese cake','cheese cake'),
        ('rainbow cake','rainbow cake'),
        ('coffee cake','coffee cake'),
        ('non-alcoholic','non-alcoholic'),
        ('butter  scotch','butter scotch'),
        ('vanilla','vanilla'),
        ('mango','mango'),
        ('pineapple','pineapple'),
        ('dates','dates'),
        ('plum','plum'),
        ('dry-fruits','dry-fruits'),
        ('mixed-fruits','mixed-fruits'),
        ('blueberry','blueberry'),
        ('strawberry','strawberry')
    )
    flavour=models.CharField(max_length=200,choices=options,default="chocolate")

    image=models.ImageField(upload_to="images")
    
    @property
    def varients(self):
        qs=self.cakevarients_set.all()
        return qs


    def __str__(self):
        return self.name

class CakeVarients(models.Model):
    price=models.PositiveIntegerField()
    
    options=(
        (".5kg",".5kg"),
        ("1kg","1kg"),
        ("2kg","2kg"),
        ("3kg","3kg"),
        ("4kg","4kg"),
        ("5kg","5kg")
       
    )

    size=models.CharField(max_length=200,choices=options,default="1kg")
    option=(
        ("round","round"),
        ("square","square"),
        ("rectangle","rectangle"),
        ("heart","heart"),
        ("cylindrical","cylindrical"),
        ("tier","tier")


    )
    shape=models.CharField(max_length=200,choices=option,default="round")
    cake=models.ForeignKey(Cakes,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.cake.name

class Offers(models.Model):
    cakevarient=models.ForeignKey(CakeVarients,on_delete=models.CASCADE)
    price=models.PositiveIntegerField()
    start_date=models.DateTimeField()
    due_date=models.DateTimeField()


class Carts(models.Model):
    cakevarient=models.ForeignKey(CakeVarients,on_delete=models.DO_NOTHING)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    options=(
        ("in-cart","in-cart"),
        ("order-placed","order-placed"),
        ("cancelled","cancelled")
    )

    status=models.CharField(max_length=200,choices=options,default="in-cart")
    date=models.DateTimeField(auto_now_add=True)


class Orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cakevarient=models.ForeignKey(CakeVarients,on_delete=models.CASCADE)
    options=(
      
        ("order-placed","order-placed"),
        ("cancelled","cancelled"),
        ("dispatced","dispatched"),
        ("in-transit","in-transit"),
        ("delivered","delivered")
    )
    status=models.CharField(max_length=200,choices=options,default="order-placed")
    orderd_date=models.DateTimeField(auto_now_add=True)
    expected_date=models.DateField(null=True)
    address=models.CharField(max_length=200)

from django.core.validators import MinValueValidator,MaxValueValidator

class Reviews(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cake=models.ForeignKey(Cakes,null=True,on_delete=models.SET_NULL)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    comment=models.CharField(max_length=300)