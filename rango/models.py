from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import datetime
#from datetime import date
from datetime import timezone

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.views < 0:
            self.views = 0
        super(Category, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name_plural = "Categories"
        
    def __str__(self):
        return self.name

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    first_visit = models.DateField(default=datetime.date.today)
    last_visit = models.DateField(blank=True, null=True)    

    def save(self, *args, **kwargs):
        if self.last_visit is not None:
            if self.first_visit > self.last_visit:
                self.last_visit = self.first_visit
            if self.last_visit > datetime.date.today():
                self.last_visit = datetime.date.today()
        if self.first_visit > datetime.date.today():
            self.first_visit = datetime.date.today()
          
        super(Page, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='/static/profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    def __str__(self):
    #def __unicode__(self):
        return self.user.username
