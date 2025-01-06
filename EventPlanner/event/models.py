from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#class User(models.Model):
    #username = models.CharField(max_length=200)
    #password = models.CharField(max_length=200)

class User(AbstractUser):
    pass
    
class Events(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('unlisted', 'Unlisted'),
        ('concert', 'Concert'),
        ('book_club', 'Book club'),
        ('potluck', 'Potluck'),
        ('meeting', 'Meeting'),
    ], default='unlisted')
    id = models.IntegerField(primary_key=True, unique=True)
    title = models.CharField(max_length=255, default="Untitled")
    description = models.TextField(null=True, blank=True, default="No description")
    capacity = models.PositiveIntegerField(null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    event_status = models.CharField(max_length=50, choices=[
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ], default='upcoming')
    RSVP_deadline = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.id} - {self.category}"


class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)


#class Ticket(models.Model):