from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField('Название',max_length = 128)
    author = models.CharField('Автор',max_length = 128)
    genre = models.CharField('Жанр',max_length = 56)
    cost = models.IntegerField('Цена')
    release_date = models.DateField('Дата выпуска')
    file = models.FileField(null=True, upload_to='books/')
    description = models.TextField('Описание', null=True)
    cover = models.ImageField('Обложка', upload_to='covers/', null=True)
    
    def __str__(self):
        return self.title
    

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField('Book')

    def total_cost(self):
        return sum(book.cost for book in self.books.all())
    
class PurchaseRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
