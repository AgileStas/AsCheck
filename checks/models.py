import sys

from django.db import models

class DataRestriction(models.IntegerChoices):
    UNR = 0, "Нетаємно"
    SEC = 3, "Таємно"
    RES = 4, "ДСК"

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
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    restriction = models.SmallIntegerField(null=False, default=DataRestriction.UNR, choices=DataRestriction)
    active = models.BooleanField(null=False, default=True)
    # HDD, SSD, PenDrive, ...
    stype = models.CharField(max_length=50,null=False, default='USB')

class Host(models.Model):
    # id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, hostname TEXT NOT NULL, division TEXT, serialnumber TEXT, cs_manufacturer TEXT, cs_model TEXT, cs_systemfamily TEXT, restriction SHORT INTEGER, owner TEXT
    hostname = models.TextField()
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True)
    serialnumber = models.TextField(null=True)
    cs_manufacturer = models.TextField(null=True)
    cs_model = models.TextField(null=True)
    cs_systemfamily = models.TextField(null=True)
    restriction = models.SmallIntegerField(null=False, default=DataRestriction.UNR, choices=DataRestriction)
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
    note = models.TextField(default='', null=False)
    # Host is currently in use
    active = models.BooleanField(null=False, default=True)

    @property
    def usbstor_list(self):
        usbstor_list_json = self.usb_json

        # import sys
        # print(usbstor_list_json, file=sys.stderr)

        usl = []
        # if isinstance(usbstor_list_json, list):
        if type(usbstor_list_json) is list:
            for el in usbstor_list_json:
                if type(el) is dict:
                    if 'Service' in el.keys() and 'PSChildName' in el.keys():
                        if el['Service'] == 'USBSTOR':
                            sn = el['PSChildName']
                            lm = el['Item-LastModified']
                            line_sn_t = '{lm}\t{pk}\t{res}\t{sn}'
                            line_sn = ''
                            print("Filtering UsbStor for '{}'".format(sn), file=sys.stderr)
                            try:
                                # rus = UsbStor.objects.get(serialnum__iexact=sn)
                                # rus = UsbStor.objects.filter(serialnum__icontains=sn)
                                rus = UsbStor.objects.filter(serialnum__iexact=sn)
                                print(rus, file=sys.stderr)
                                if not rus:
                                    line_sn = line_sn_t.format(lm=lm, pk='------', res='-', sn=sn)
                                else:
                                    print(rus[0], file=sys.stderr)
                                    line_sn = line_sn_t.format(lm=lm, pk=rus[0].regnum, res=rus[0].restriction, sn=sn)
                            except:
                                line_sn = line_sn_t.format(lm=lm, pk='!!!!!!', res='-', sn=sn)

                            usl.append(line_sn)

        # return usbstor_list_json
        return '\n'.join(usl)

# Windows Product Key
class WPK(models.Model):
    value = models.CharField(max_length=50)