from django.db import models
from django.utils.timezone import now


class App(models.Model):
    id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=254)
    app_logo = models.CharField(max_length=254)
    wallet = models.IntegerField()
    number = models.IntegerField()
    start = models.DecimalField()
    ms = models.CharField(max_length=254)
    contents = models.CharField(max_length=254)
    tj_ms = models.CharField(max_length=254)
    level = models.IntegerField()
    is_tj = models.BooleanField()
    is_ph = models.BooleanField()
    is_hot = models.BooleanField()
    times = models.BigIntegerField()
    andr_baoname = models.CharField(max_length=254)
    andr_apk = models.CharField(max_length=254)
    andr_banben = models.CharField(max_length=254)
    andr_size = models.CharField(max_length=254)
    andr_url = models.CharField(max_length=254)
    ios_url = models.CharField(max_length=254)
