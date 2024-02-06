from django.contrib import admin
from django.urls import path, include
from shop_app.views import register, auth, catalog, profile, logOut, book_detail, add_to_cart, cart, purchase
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', auth, name='auth'),
    path('', catalog, name='catalog'),
    path('profile/', profile, name='profile'),
    path('logout/', logOut, name='logout'),
    path('book_detail/<int:book_id>/', book_detail, name='book_detail'),
    path('add_to_cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('purchase/', purchase, name='purchase'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
