from django.db import models
import uuid
# Create your models here.

class CSVconvert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    input = models.URLField(max_length=200, null=True, blank=True)
    output = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.input.name