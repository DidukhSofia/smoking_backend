from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    role = models.TextField()

class User(AbstractUser):
    userId = models.AutoField(primary_key=True)
    userName = models.TextField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    startAmountOfCigarettes = models.FloatField()
    priceOfPack = models.FloatField()
    amountCigarettesInPack = models.IntegerField()
    progressDays = models.IntegerField()
    role = models.ForeignKey(Role, default=1, on_delete=models.CASCADE)
    username = None
    first_name = None
    last_name = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def calculate_saved_cigarettes(self):
        return self.progressDays * self.startAmountOfCigarettes
    
    def calculate_saved_money(self):
        one_cigarette_price = self.priceOfPack / self.amountCigarettesInPack
        return one_cigarette_price * self.calculate_saved_cigarettes()



class Article(models.Model):
    articleId = models.AutoField(primary_key=True)
    author = models.TextField()
    title = models.TextField()
    text = models.TextField()

class Quote(models.Model):
    quoteId = models.AutoField(primary_key=True)
    text = models.TextField()
