from django.db import models


class Document(models.Model):
    title = models.CharField(max_length=255)
    file_data = models.BinaryField()  # Stores the file content in binary format
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Create your models here.
