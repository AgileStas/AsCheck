from django.db import models

class Division(models.Model):
    int_acro = models.TextField()
    common_name = models.TextField()
    active = models.BooleanField()

class Person(models.Model):
    first_name = models.TextField()
    middle_name = models.TextField()
    family_name = models.TextField()
    military_rank = models.TextField(null=True)
    phone_number = models.TextField(null=True)

    def full_name(self):
        return "%s %s %s, %s" % (self.family_name, self.first_name, self.middle_name, self.military_rank)

# Create your models here.
class UsbStor(models.Model):
    # regid INTEGER, regnum TEXT, serialnum TEXT, divname TEXT, owner TEXT, regdate DATE
    regid = models.IntegerField()
    regnum = models.CharField(max_length=20)
    regdate = models.DateField(null=True)
    serialnum = models.CharField(max_length=200)
    divname = models.CharField(max_length=50)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True)
    owner = models.CharField(max_length=50)

class Host(models.Model):
    class Restriction(models.IntegerChoices):
        UNR = 0, "Нетаємно"
        SEC = 3, "Таємно"
        RES = 4, "ДСК"

    # id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, hostname TEXT NOT NULL, division TEXT, serialnumber TEXT, cs_manufacturer TEXT, cs_model TEXT, cs_systemfamily TEXT, restriction SHORT INTEGER, owner TEXT
    hostname = models.TextField()
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True)
    serialnumber = models.TextField(null=True)
    cs_manufacturer = models.TextField(null=True)
    cs_model = models.TextField(null=True)
    cs_systemfamily = models.TextField(null=True)
    restriction = models.SmallIntegerField(null=False, default=Restriction.UNR, choices=Restriction)
    owner = models.TextField(null=True)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    # Computer System
    cs_json = models.JSONField(null=True)
    # Antivirus Product
    av_json = models.JSONField(null=True)
    # Windows Activation
    wa_json = models.JSONField(null=True)
    # ESET
    eset_json = models.JSONField(null=True)
    # Enum USB
    usb_json = models.JSONField(null=True)
    # Date and time of the latest check
    check_date = models.DateTimeField(null=True)
    # Notes about this host
    note = models.TextField(default='',null=False)

