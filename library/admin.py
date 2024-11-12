########## import the models ##############
from django.contrib import admin
from .models import Students,Publishers,Book,BookCategories,Borrowers,Returns,Author,BoolAuthor,TransactionLogs
from django.contrib.auth.models import User

################# Register your models here.###############

#register the student to display username, course, year in admin panell
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user__username','course','year')


#register the model in django admin
admin.site.register(Students,StudentAdmin)
admin.site.register(Book)
admin.site.register(BookCategories)
admin.site.register(Publishers)
admin.site.register(Borrowers)
admin.site.register(Returns)
admin.site.register(Author)
admin.site.register(BoolAuthor)
admin.site.register(TransactionLogs)