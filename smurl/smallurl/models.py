from django.db import models
import random, string

def idgen():
    d = URL.objects.all()
    id = ''
    valid_id = False
    while not valid_id:
        id = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=5))
        
        if id not in d:
            valid_id = True
    
    return id

# Create your models here.
class URL(models.Model):
    id = models.CharField(max_length=50, primary_key=True, default=idgen)
    url = models.URLField(max_length=200)
    tls = models.BooleanField()
    expires = models.DateTimeField(null=True)
