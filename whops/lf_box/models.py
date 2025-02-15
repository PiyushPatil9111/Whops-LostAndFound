from django.db import models
from django.contrib.auth.models  import User

class Item(models.Model):
    STATUS_CHOICES = [('lost', 'Lost'), ('found', 'Found')]
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='item_images/')               #Django will save the image to the given path and save the image path to DB
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)  #status choice will be made from variable defined initially "STATUS_CHOICES".
    user = models.ForeignKey(User, on_delete=models.CASCADE)          #Links each Item to a USer that posted it.
    labels = models.CharField(max_length=100, blank=True, null=True)  #Allowing user field to be blank or bull

    def __str__(self):
        return self.title

