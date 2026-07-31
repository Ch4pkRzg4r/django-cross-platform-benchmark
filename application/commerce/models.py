# commerce/models.py
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    sizes = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/')
    category = models.CharField(max_length=255, default='')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class AdditionalImage(models.Model):
    product = models.ForeignKey(Product, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/additional/')

    def __str__(self):
        return f"Additional Image for {self.product.name}"

class Feature(models.Model):
    FEATURE_SECTIONS = [
        ('index', 'Index Page'),
        ('about', 'About Page'),
    ]

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='features/')
    section = models.CharField(max_length=50, choices=FEATURE_SECTIONS, default='index')

    def __str__(self):
        return f"{self.title} - {self.get_section_display()}"

class Banner(models.Model):
    MAIN = 'main'
    THIRD = 'third'
    PROMOTIONAL = 'promo'

    BANNER_SECTION_CHOICES = [
        (MAIN, 'Main Banner'),
        (THIRD, 'Third Banner'),
        (PROMOTIONAL, 'Promotional Banner')
    ]

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='banners/')
    section = models.CharField(
        max_length=50,
        choices=BANNER_SECTION_CHOICES,
        default=MAIN
    )
    button_text = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_section_display()})"

class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

# Define the AboutPage model to fix the ImportError
class AboutPage(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    heading = models.CharField(max_length=200)
    description = models.TextField()
    marquee_text = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='about_images/', blank=True, null=True)
    video = models.FileField(upload_to='about_videos/', blank=True, null=True)

    def __str__(self):
        return self.title


# commerce/models.py




# commerce/models.py

from django.db import models
from django.contrib.auth.models import User  # Import User model for associating cart with user
from decimal import Decimal




class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        total = sum(item.subtotal for item in self.cartitems.all())
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cartitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)  # Optional: If you have a size attribute


    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size})" if self.size else f"{self.quantity} x {self.product.name}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
    
    
# commerce/models.py

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# Signal to create or update a profile automatically
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


# models.py
from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"


class ContactInfo(models.Model):
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    office_hours = models.CharField(max_length=50)

    def __str__(self):
        return f"Contact Information"

class ContactPerson(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    image = models.ImageField(upload_to='contact_person_images/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.role}"
    


    # commerce/models.py

from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    is_paid = models.BooleanField(default=False)  # Track payment status

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


# Payment Model
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.amount_paid}"



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=50, blank=True, null=True)  # Optional size field
    price = models.DecimalField(max_digits=10, decimal_places=2)

   
    @property
    def subtotal(self):
        # Safely handle None values
        if self.price is None or self.quantity is None:
            return 0
        return self.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.size})" if self.size else f"{self.quantity} x {self.product.name}"