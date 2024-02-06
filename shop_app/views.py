from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import Book, Cart, PurchaseRequest
from django.db.models import Q


def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth')
        return view_func(request, *args, **kwargs)
    return wrapper

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('profile')
    return render(request, 'registration/register.html')

def auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
    return render(request, 'registration/login.html')

def logOut(request):
    logout(request)
    return redirect(auth)


def catalog(request):
    query = request.GET.get('q')

    if query:
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__icontains=query))
    else:
        books = Book.objects.all()

    return render(request, 'catalog.html', {'books': books, 'query': query})


@login_required
def profile(request):
    user = request.user
    confirmed_purchases = PurchaseRequest.objects.filter(user=user, confirmed=True)
    return render(request, 'profile.html', {'user': user, 'confirmed_purchases': confirmed_purchases})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'book_detail.html', {'book': book})

def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    user = request.user

    cart, created = Cart.objects.get_or_create(user=user)

    if book not in cart.books.all():
        cart.books.add(book)
        cart.save()

    return redirect('book_detail', book_id=book.id)


@login_required
def cart(request):
    user = request.user
    try:
        cart = Cart.objects.get(user=user)
        books_in_cart = cart.books.all()
        total_cost = cart.total_cost()
    except Cart.DoesNotExist:
        books_in_cart = []
        total_cost = 0

    return render(request, 'cart.html', {'books_in_cart': books_in_cart, 'total_cost': total_cost})

@login_required
def purchase(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.get(user=user)
        

        for book in cart.books.all():
            PurchaseRequest.objects.create(user=user, book=book, confirmed=False)
        cart.books.clear()

        return redirect('profile')

    return redirect('cart')

@login_required
def purchase(request):
    if request.method == 'POST':
        user = request.user
        cart = Cart.objects.get(user=user)
        
        for book in cart.books.all():
            PurchaseRequest.objects.create(user=user, book=book, confirmed=False)

        cart.books.clear()

        return redirect('profile')

    return redirect('cart')
