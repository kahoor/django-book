from django.db import models
import uuid
# Create your models here.


class Ganre(models.Model):
    """
    Model representing a book ganre (just a name like drama, comedy, ...)
    """
    name = models.CharField(max_length=50, help_text="Enter a book ganre")

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a book in general, not every copy available just a book,
    by title sumery, author, this kind of staff!
    """
    title = models.CharField(max_length=250, help_text='Enter book title')
    summary = models.TextField(max_length=2000, help_text='Enter a description of book')
    isbn = models.CharField(max_length=13, help_text='barcode khodmoone yejooraye')
    
    ganre = models.ManyToManyField(Ganre, help_text='Enter a ganre or more for the book')
    
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    """
    Model representing an author, 
    """
    first_name = models.CharField(max_length=90)
    last_name = models.CharField(max_length=90)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return "{} {}".format(self.last_name, self.first_name)


class BookInstance(models.Model):
    """
    Model representing situation of every single copy of a book!
    """

    id = models.UUIDField(primary_key=True, 
                            default=uuid.uuid4)
    book = models.ForeignKey("Book",  on_delete=models.SET_NULL, null=True)
    imprint = models.CharField( max_length=250)
    due_back = models.DateField(null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    status = models.CharField(max_length=50,
                                choices=LOAN_STATUS,
                                blank=True,
                                default='m',
                                help_text='Book Availablity')

    class Meta:
        ordering = ["due_back"]

    def __str__(self):
        return "{} ({})".format(self.id, self.book.title)