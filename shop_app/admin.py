from django.contrib import admin
from .models import Book, PurchaseRequest, Cart

class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'confirmed']
    
    def get_queryset(self, request):

        queryset = super().get_queryset(request)
        return queryset.filter(confirmed=False)

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'has_books']

    def has_books(self, obj):
        return obj.books.exists()

    has_books.boolean = True
    has_books.short_description = 'Есть книги'
    
admin.site.register(Book)
admin.site.register(Cart, CartAdmin)
admin.site.register(PurchaseRequest, PurchaseRequestAdmin)
