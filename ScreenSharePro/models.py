from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    video_blob = models.FileField(upload_to='videos/')  # Adjust the upload path as needed
    transcript_id = models.CharField(max_length=100, blank=True, null=True)  # Add a transcript ID field

    def __str__(self):
        return self.title
