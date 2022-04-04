from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django_pandas.managers import DataFrameManager

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Delete profile when user is deleted
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile' #show how we want it to be displayed

    def save(self):
        super().save()

        img = Image.open(self.image.path) # Open image
        
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(self.image.path) # Save it again and override the larger image

class Organization(models.Model):
	Organization_Name = models.CharField(max_length=50)
	Organization_Description = models.CharField(max_length=200, blank=True, null=True)

	objects = DataFrameManager()

	def __str__(self):
		return self.Organization_Name

	class Meta:
		ordering = ['Organization_Name']