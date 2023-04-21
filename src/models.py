from django.db import models

# Create your models here.




class voice_history(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    voice_text = models.CharField(max_length=200)
    voice_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.voice_text