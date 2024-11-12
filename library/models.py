########### import the modul
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

################# Create your models here######################


########### Student Model ############
class Students(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    course=models.CharField(max_length=30)
    year=models.CharField(max_length=5)
    contact=models.CharField(max_length=11)
    birth=models.DateTimeField(default=None)
    gender=models.CharField(max_length=10)


    def __str__(self):
        return f"{self.user.username}-{self.course}"


############ Categories Model ##############
class BookCategories(models.Model):
    category_name=models.CharField(max_length=30)

############ Publisher Model ##############
class Publishers(models.Model):
    publisher_name=models.CharField(max_length=100)


############ Author Model ############
class Author(models.Model):
    author_name=models.CharField(max_length=100)

 ########### Book Model #################
class Book(models.Model):
    name=models.CharField(max_length=100)
    edition=models.IntegerField()
    cost=models.IntegerField()
    copies=models.IntegerField()
    category_id=models.ForeignKey(BookCategories,on_delete=models.CASCADE,related_name='books')
    publisher_id=models.ForeignKey(Publishers,on_delete=models.CASCADE,related_name='books')


############ Borrowers Model #############
class Borrowers(models.Model):
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='borrowed_books')
    student=models.ForeignKey(Students,on_delete=models.CASCADE,related_name='borrowed_by')
    release_date=models.DateTimeField(default=None)
    due_date=models.DateTimeField(default=None)

############ Returns Model ###############
class Returns(models.Model):
    borrowers_id=models.ForeignKey(Borrowers,on_delete=models.CASCADE,related_name='return_by')
    return_date=models.DateTimeField(default=None)
    fine_amount=models.CharField(max_length=10)

############ Book And Author Model ###########
class BoolAuthor(models.Model):
    book_id=models.ForeignKey(Book,on_delete=models.CASCADE,related_name='author_book')
    auhtor_id=models.ForeignKey(Author,on_delete=models.CASCADE,related_name='author_id')

############ Transaction Model ###############
class TransactionLogs(models.Model):
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='transaction_logs')
    stud_id = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='transaction_log_students')
    action=models.CharField(max_length=20)
