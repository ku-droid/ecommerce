from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
STATE_CHOICES=(
    ('1','1'),
    ('2','2'),
    ('3','3'),
    ('4','4'),
    ('5','5'),
    ('6','6'),
    ('7','7'),
)

#M2O relationship with User---Customer Model
class Customer(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    locality=models.CharField(max_length=200)
    city=models.CharField(max_length=50)
    zipcode=models.IntegerField()
    state=models.CharField(choices=STATE_CHOICES,max_length=200)

    def __str__(self):
        return str(self.id)

#Product Model
# CATEGORY_CHOICES=(
#     ('OP','One Piece'),
#     ('TP','Top Wears'),
#     ('B','Bags'),
# )

CATEGORY_CHOICES=(
    ('E','electronics'),
    ('C','clothing'),
    ('G','grocery'),
)

class Product(models.Model):
    title=models.CharField(max_length=100)
    selling_price=models.FloatField()
    discounted_price=models.FloatField()
    description=models.TextField()
    brand=models.CharField(max_length=100)
    category=models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    product_image=models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    
#Cart Model
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)

    def __str_(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
        
#Order Placed Model
STATUS_CHOICES=(
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
)

class OrderPlaced(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    ordered_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField( max_length=50,choices=STATUS_CHOICES,default='Pending')
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price

# class Wishlist(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     product=models.ForeignKey(Product,on_delete=models.CASCADE)

class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    mode_of_contact = models.CharField('Conatct by', max_length=50)
    question_categories = models.CharField('How can we help you?', max_length=50)
    message = models.TextField(max_length=3000)

    def __str__(self):
        return self.email