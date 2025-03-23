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
            aws_session_token=settings.AWS_SESSION_TOKEN,
            region_name=settings.AWS_REGION
        )
    
        # Find matching lost items
        lost_items = Item.objects.filter(
            status='L',
            title__icontains=self.title,
            location__icontains=self.location
        )
    
        # Get the founder's profile (user who posted the found item)
        founder_profile = Profile.objects.get(user=self.user)
    
        for lost_item in lost_items:
            message = (
                f"Dear {lost_item.user.username},\n\n"
                f"We are pleased to inform you that a matching found item has been posted on our platform! "
                f"It seems that someone has found an item that matches the description of your lost item. "
                f"Here are the details:\n\n"
                f"**Item Details:**\n"
                f"- Title: {self.title}\n"
                f"- Description: {self.description}\n"
                f"- Location Found: {self.location}\n\n"
                f"**Founder's Contact Information:**\n"
                f"- Posted by: {self.user.username}\n"
                f"- Mobile Number: {founder_profile.mobile_number}\n"
                f"- Address: {founder_profile.address}\n\n"
                f"Please reach out to the founder at your earliest convenience to claim your item. "
                f"We hope this brings you one step closer to recovering your lost belongings!\n\n"
                f"If you have any questions or need further assistance, feel free to contact us.\n\n"
                f"Best regards,\n"
                f"The Lost and Found Team"
            )
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