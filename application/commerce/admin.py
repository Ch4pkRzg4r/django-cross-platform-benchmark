# commerce/admin.py
from django.contrib import admin
from .models import Product, Feature, Banner, AdditionalImage, Blog, ContactInfo, ContactPerson, Cart, CartItem
from .models import Profile, ContactMessage
from django.contrib import admin
from .models import Order, Payment



# Custom Admin classes (optional)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtitle', 'section')
    list_filter = ('section',)
    search_fields = ('title', 'subtitle', 'section')

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'size', 'subtotal')  # Include size in CartItemAdmin

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'total_price')

from django.contrib import admin
from .models import Product, Feature, Banner, AdditionalImage, Blog, ContactInfo, ContactPerson, Cart, CartItem, Profile, ContactMessage, Order, OrderItem, Payment

# Custom admin class for OrderItems (inline display)
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'size', 'quantity', 'price', 'subtotal')  # Include subtotal as readonly
    can_delete = False
    extra = 0


# Custom admin class for Orders
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_amount', 'created_at', 'status', 'is_paid')  # Show these fields in the order list view
    list_filter = ('status', 'is_paid')  # Add filters for status and payment
    search_fields = ('user__username', 'status')  # Allow searching by user and status
    readonly_fields = ('user', 'total_amount', 'created_at')  # Make certain fields read-only
    inlines = [OrderItemAdmin]  # Include OrderItemAdmin inline
    fieldsets = (
        (None, {
            'fields': ('user', 'total_amount', 'status', 'is_paid')  # Fields to display in the detail view
        }),
    )

# Register your models
admin.site.register(Product)
admin.site.register(Feature)
admin.site.register(Banner, BannerAdmin)
admin.site.register(AdditionalImage)
admin.site.register(Blog)
admin.site.register(ContactInfo)
admin.site.register(ContactPerson)
admin.site.register(Profile)
admin.site.register(ContactMessage)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)  # Use custom OrderAdmin
admin.site.register(Payment)


