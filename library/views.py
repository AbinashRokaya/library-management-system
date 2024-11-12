################## import models ###################
from unicodedata import category
from django.utils import timezone
from dbus.decorators import method
from django.shortcuts import render,HttpResponse,redirect
from dominate.tags import title
from mypyc.doc.conf import author
from .models import Students,Publishers,Book,BookCategories,Borrowers,Returns,Author,BoolAuthor,TransactionLogs
from datetime import datetime,timedelta
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import  login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
########################Create your views here ####################


############# Home view ###########
def home(request):
    book=Book.objects.all().order_by('name') # get all the book from Book to shown in home page
    if request.method=='GET': # for get word from search box
        bk=request.GET.get('search')
        if bk!=None:
            book=Book.objects.filter(name__icontains=bk).order_by('name') #filter all the word or letter which give in search box. __icontains tag is use to find the similar word in database

    #### Paginator to numering the page #####
    paginator=Paginator(book,10) #How many page is to show
    page_number=request.GET.get('page') #Get the page number
    bookfinal=paginator.get_page(page_number) #Get the final page number
    total_page=bookfinal.paginator.num_pages # Get the total page number

    return render(request,'index.html',{'book':bookfinal,'lastpage':total_page,'totalPagelist':[n+1 for n in range(total_page)]})


################ Register View ################
def register(request):
    if request.method=='POST':
        name=request.POST.get('name')
        birth=request.POST.get('birthday')
        gender=request.POST.get('gender')
        course=request.POST.get('course')
        year=request.POST.get('year')
        contact=request.POST.get('contact')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if not all([name, birth, gender, course, year, contact, email, pass1, pass2]): #if the form is blank
            messages.info(request,"There is blank in the form. You have to fill all.")
            return redirect('register')
        else:
            birth_day = datetime.strptime(birth, '%d/%m/%Y') # format in datetime
            birth_day = birth_day.replace(hour=0, minute=0, second=0)

            if pass1 != pass2: # Check the conform password and password
                messages.info(request, "Your password and confirm password do not match!")
                return redirect('register')

            try:
                # Create User instance
                my_user = User.objects.create_user(username=name, email=email, password=pass1)
                my_user.save()  # Ensure the user is saved before proceeding

                # Now create the student and link to the User instance
                student = Students(
                    user=my_user,  # Assign the user instance to the student
                    course=course,
                    year=year,
                    contact=contact,
                    birth=birth_day,
                    gender=gender
                )
                student.save()  # Save the student instance with the user link
                return redirect('home')

            except Exception as e:
                messages.error(request, f"Error occurred: {str(e)}")
                return redirect('register')

    return render(request,'Register..html')


################### Login view #####################
def sign_up(request):
    if request.method=='POST':
        name=request.POST.get('name')
        password=request.POST.get('password')
        user = authenticate(request, username=name, password=password) #check the uername and password in database

        if user is not None:
            login(request, user) # if user already register then login
            return redirect('home')
        else:
             messages.info(request,'username or Password is incorrect!!!')

    return render(request,'sign_up.html')


##################### Logout  view #################
@login_required(login_url='/sign_up/') #only when where is login. if user is not login the it redirect in sign page
def LogoutPage(request):
    logout(request) # call logout function
    return redirect('home')


################# Borrower Book view #################
@login_required(login_url='/sign_up/')
def Borrower(request):
    if request.method=='POST':
        bk_id=request.POST.get('book_id')
        time = timezone.now()
        release= time.replace(hour=0, minute=0, second=0)
        due_date=release + timedelta(days=25) #add the time 25 day to return the book

        if not bk_id:
            messages.info(request, "The book id is blank. Fill the book id.")
            return redirect('borrowers')
        else:
            try:
                # Get the book instance using the provided book ID

                books=Book.objects.get(id=bk_id)
                borr_list=books.borrowed_books.all() #get the data from revers name which is given to the Borrowers Model

                if not borr_list:
                        if books.copies==0:
                            messages.info(request,'The book is already taken by other. There is no other copies of this book.')
                            return redirect('borrowers')
                        else:
                            book_instance, created = Book.objects.get_or_create(id=bk_id)
                            if not book_instance:
                                messages.info(request, "There is no book of this id.")

                            # Check if the student exists for the current user
                            student, created = Students.objects.get_or_create(user=request.user)

                            # Create the new Borrower instance and save it
                            borrowers = Borrowers.objects.create(
                                book_id=book_instance,
                                student=student,
                                release_date=release,
                                due_date=due_date
                            )
                            books.copies=books.copies-1 # if student borrow the book the Book copies is subtract by one
                            books.save()

                else:
                    messages.info(request, f'book id {bk_id} is already taken by you')
                    return redirect('borrowers')

                # Redirect to home after successful borrowing
                messages.success(request, "Book borrowed successfully!")
                return redirect('home')

            except Book.DoesNotExist:
                messages.info(request, "The selected book does not exist.")
                return redirect('borrowers')  # Redirect to the borrower's page if book doesn't exist
            except Students.DoesNotExist:
                messages.info(request,"The student record does not exist. Please make sure a student record is linked to your user.")
                return redirect('home')

    return render(request,'Borrowers.html')


################# Book return view ##################
@login_required(login_url='/sign_up/')
def Return(request):
    if request.method=='POST':
        borrower_id=request.POST.get('borrowers_id')
        time = timezone.now()
        return_date = time.replace(hour=0, minute=0, second=0)

        if borrower_id=="":
            messages.info(request, "The borrowers id is blank. Fill the borrowers id.")
        else:
            try:
                borr = Borrowers.objects.get(id=borrower_id) #get the data from borrower id
                if borr.id=="":
                    messages.info(request, "There is no borrowers id.")
                    return redirect('return')
                else:
                    borrower,created = Borrowers.objects.get_or_create(id=borrower_id)
                    time_diff = return_date - borrower.release_date
                    if time_diff.days > 25:
                        fine_amount = 10
                    else:
                        fine_amount = 0

                    ret=Returns.objects.create(
                        borrowers_id=borrower,
                        fine_amount=fine_amount,
                        return_date=return_date

                    )


                    ret=borr.book_id
                    ret.copies+=1 # if student return the book the Book copies add by one
                    ret.save()
                    borr.delete() # if stduent return the book the Borrower id delete
                    return redirect('home')

            except ObjectDoesNotExist:
                messages.error(request, "The specified borrower does not exist.")
                return redirect('return')

        return redirect('return')

    return render(request,'Return_book.html')


@login_required(login_url='/sign_up/')
def Books(request):
    if request.method=='POST':
        book_name=request.POST.get('book')
        publisher_name =request.POST.get('publisher')
        author_name=request.POST.get('author')
        edition=request.POST.get('edition')
        cost=request.POST.get('cost')
        copies=request.POST.get('copies')
        category_name=request.POST.get('category')

        if not all([book_name,publisher_name,author_name,edition,cost,copies,category_name]):
            messages.info(request,"There is blank in the form. You have to fill all.")
            return redirect('book')
        else:
            # Fetch the Category and Publisher objects by name
            category,created = BookCategories.objects.get_or_create(category_name=category_name)
            publisher,created = Publishers.objects.get_or_create(publisher_name=publisher_name)

            # Create a new Book instance with the fields
            new_book = Book.objects.create(
                name=book_name,
                edition=edition,
                cost=cost,
                copies=copies,
                category_id=category,
                publisher_id=publisher
            )
            author, created = Author.objects.get_or_create(author_name=author_name)
            BoolAuthor.objects.create(book_id=new_book, auhtor_id=author)
            return redirect('book')
    return render(request,'book.html')


################### Borrower Book list ##################
@login_required(login_url='/sign_up/')
def BookList(request):
    id=request.user.id-1
    list=[]
    borrow_book_list=Borrowers.objects.filter(student=id)
    time = timezone.now()

    for b in borrow_book_list:
        today = time.replace(hour=0, minute=0, second=0)
        time_diff = today - b.release_date
        if time_diff.days > 25: # if the student delay the return the book. He should pay fine
            fine_amount = 10
        else:
            fine_amount = 0
        list.append({'id':b.id,'book_id':b.book_id.id,'name':b.book_id.name,'release':b.release_date,'due':b.due_date,'fine_amount':fine_amount})

    context={
        'borrow_book_list': list
    }
    return render(request,'Your_book_list.html',context)


################## Book category view ####################
@login_required(login_url='/sign_up/')
def category(request,name):
    books=[]
    cat=BookCategories.objects.filter(category_name=name)
    for c in cat:
        book=Book.objects.filter(category_id=c.id)
        for b in book:
            print(b.name)
            books.append({'id':b.id,'name':b.name,'category':b.category_id,'edition':b.edition,'copies':b.copies}) # add the data in books list which is filter by book

    context={
        'books':books
    }
    return render(request,'category.html',context)