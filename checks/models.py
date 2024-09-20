from django.db import models

# Create your models here.
class UsbStor(models.Model):
    # regid INTEGER, regnum TEXT, serialnum TEXT, divname TEXT, owner TEXT, regdate DATE
    regid = models.IntegerField()
    regnum = models.CharField(max_length=20)
    regdate = models.DateField(null=True)
    serialnum = models.CharField(max_length=200)
    divname = models.CharField(max_length=50)
    owner = models.CharField(max_length=50)

class Host(models.Model):
    # id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, hostname TEXT NOT NULL, division TEXT, serialnumber TEXT, cs_manufacturer TEXT, cs_model TEXT, cs_systemfamily TEXT, restriction SHORT INTEGER, owner TEXT
    hostname = models.TextField()
    division = models.TextField(null=True)
    serialnumber = models.TextField(null=True)
    cs_manufacturer = models.TextField(null=True)
    cs_model = models.TextField(null=True)
    cs_systemfamily = models.TextField(null=True)
    restriction = models.SmallIntegerField(null=True)
    owner = models.TextField(null=True)