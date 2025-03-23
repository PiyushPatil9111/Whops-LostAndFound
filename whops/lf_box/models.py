from django.db import models
from django.contrib.auth.models  import User
import boto3
from django.conf import settings

class Item(models.Model):
    STATUS_CHOICES = [('L', 'Lost'),('F', 'Found'),]
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    date = models.DateField()
    image = models.ImageField(upload_to='item_images/')            #Django will save the image to the given path and save the image path to DB
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='L')  #status choice will be made from variable defined initially "STATUS_CHOICES".
    user = models.ForeignKey(User, on_delete=models.CASCADE)          #Links each Item to a USer that posted it.
    labels = models.CharField(max_length=100, blank=True, null=True)  #Allowing user field to be blank or null.

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.status == 'F':  # Only trigger for found items
            self.notify_matching_lost_items()

    def notify_matching_lost_items(self):
        sns_client = boto3.client(
            'sns',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )

        # Find matching lost items
        lost_items = Item.objects.filter(
            status='L',
            title__icontains=self.title,
            location__icontains=self.location
        )

        for lost_item in lost_items:
            message = f"A matching found item has been posted:\n\nTitle: {self.title}\nDescription: {self.description}\nLocation: {self.location}\nPosted by: {self.user.username}"
            sns_client.publish(
                TopicArn=settings.SNS_TOPIC_ARN,
                Message=message,
                Subject="Matching Found Item"
            )
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        # Update the email field in the User model
        if self.email:
            self.user.email = self.email
            self.user.save()
        super().save(*args, **kwargs)
