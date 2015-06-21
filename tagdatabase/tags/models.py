from django.db import models

# Create your models here.

class Tag(models.Model):
    user_id = models.IntegerField(default=0)
    box_number = models.IntegerField(default=0)
    name = models.CharField(max_length=20)  
    print_date = models.DateField('print date')
    comment = models.CharField(max_length=50)
    def get_absolute_url(self):
    	from django.core.urlresolvers import reverse
    	return reverse('tags:details_long', args=[str(self.id)])

