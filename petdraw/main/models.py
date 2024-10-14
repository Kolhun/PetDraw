from django.db import models

class Drawing(models.Model):
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Drawing {self.id} at {self.created_at}"
