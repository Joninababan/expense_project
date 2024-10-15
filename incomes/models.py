from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Source(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Sources' #untuk penamaan di list view admin

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    source = models.ForeignKey(to=Source, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.source} - Rp.{self.amount} on {self.date}"

    class Meta:
        ordering = ['-date'] #order by date desc
