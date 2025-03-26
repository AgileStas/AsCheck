from django import forms
from django.contrib.admin import widgets

from .models import DataRestriction, Division, Host, Person, UsbStor

from bootstrap_modal_forms.forms import BSModalModelForm


class DivisionForm(forms.ModelForm):
    class Meta:
        model = Division
        fields = (
            "int_acro",
            "common_name",
            "active",
                )

    int_acro = forms.CharField(max_length=10)
    common_name = forms.CharField(max_length=500)
    active = forms.BooleanField()

class DivisionChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super(DivisionChoiceField, self).__init__(queryset=Division.objects.all(), *args, **kwargs)

    def label_from_instance(self, obj):
        return "%s :: %s" % (obj.int_acro, obj.common_name)

class PersonChoiceField(forms.ModelChoiceField):
    def __init__(self, *args, **kwargs):
        super(PersonChoiceField, self).__init__(queryset=Person.objects.all(), *args, **kwargs)

    def label_from_instance(self, obj):
        return "%s %s %s, %s" % (obj.family_name, obj.first_name, obj.middle_name, obj.military_rank)

class StorageChoiceField(forms.ModelMultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super(StorageChoiceField, self).__init__(
            # queryset=UsbStor.objects.all(),
            queryset=UsbStor.objects.filter(active=True),
            # widget=widgets.FilteredSelectMultiple("verbose name", is_stacked=False),
            widget=forms.SelectMultiple(attrs={'size':'10'}),
            *args,
            **kwargs
        )
        # widget=forms.CheckboxSelectMultiple(attrs={'size':'10'}),

    def label_from_instance(self, obj):
        return "%s (%s) :: %s" % (obj.regnum, obj.serialnum if len(obj.serialnum) < 15 else obj.serialnum[:12] + "...", obj.division.int_acro if obj.division else "???")

'''
class StorageListField(forms.CheckboxSelectMultiple):
    def __init__(self, *args, **kwargs):
        super(StorageListField, self).__init__(
            # queryset=UsbStor.objects.all(),
            # queryset=UsbStor.objects.filter(active=True),
            # widget=widgets.FilteredSelectMultiple("verbose name", is_stacked=False),
            # widget=forms.CheckboxSelectMultiple(),
            *args,
            **kwargs
        )
        # widget=forms.CheckboxSelectMultiple(attrs={'size':'10'}),

    def label_from_instance(self, obj):
        return "%s (%s) :: %s" % (obj.regnum, obj.serialnum if len(obj.serialnum) < 15 else obj.serialnum[:12] + "...", obj.division.int_acro if obj.division else "???")
'''

#from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
#class HostForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
class HostStorageForm(BSModalModelForm):
    class Meta:
        model = Host
        fields = (
            "allowed_storage",
                )

    allowed_storage = StorageChoiceField()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['usbstor_list'].initial = self.instance.usbstor_list

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = (
            "hostname",
            "division",
            "serialnumber",
            "cs_manufacturer",
            "cs_model",
            "cs_systemfamily",
            "restriction",
            "owner",
            "person",
            "note",
            # "usbstor_list",
            "allowed_storage",
                )

    hostname = forms.CharField(max_length=100)
    division = DivisionChoiceField()
    serialnumber = forms.CharField(max_length=100)
    cs_manufacturer = forms.CharField(max_length=100)
    cs_model = forms.CharField(max_length=100)
    cs_systemfamily = forms.CharField(max_length=100, required=False)
    restriction = forms.ChoiceField(required=False, choices=DataRestriction)
    owner = forms.CharField(required=False)
    person = PersonChoiceField()
    # check_date = forms.DateTimeField(required=False)
    note = forms.CharField(required=False,widget=forms.Textarea)

    usbstor_list = forms.CharField(required=False,disabled=True,widget=forms.Textarea)

    allowed_storage = forms.ModelMultipleChoiceField(
        queryset=UsbStor.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
    # allowed_storage = StorageListField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usbstor_list'].initial = self.instance.usbstor_list
        self.fields['allowed_storage'].label_from_instance = self.label_from_instance_01

    @staticmethod
    def label_from_instance_01(obj):
        return obj.regnum        

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = (
            "first_name",
            "middle_name",
            "family_name",
            "military_rank",
            "phone_number",
                )

    first_name = forms.CharField(max_length=100)
    middle_name = forms.CharField(max_length=100)
    family_name = forms.CharField(max_length=100)
    military_rank = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=30)

class StorageForm(forms.ModelForm):
    class Meta:
        model = UsbStor
        fields = (
            "regid",
            "regnum",
            "regdate",
            "restriction",
            "stype",
            "vendor",
            "product",
            "serialnum",
            "divname",
            "division",
            "owner",
            "person",
            "active",
            "note",
                )

    regid = forms.IntegerField()
    regnum = forms.CharField(max_length=20)
    regdate = forms.DateField()
    vendor = forms.IntegerField()
    product = forms.IntegerField()
    serialnum = forms.CharField(max_length=200)
    divname = forms.CharField(max_length=50)
    division = DivisionChoiceField(required=False)
    owner = forms.CharField(max_length=50)
    person = PersonChoiceField(required=False)
    restriction = forms.ChoiceField(required=False, choices=DataRestriction)
    # active = forms.BooleanField(required=False)
    active = forms.BooleanField(widget=forms.CheckboxInput)
    # HDD, SSD, PenDrive, ...
    stype = forms.CharField(max_length=50)
    note = forms.Textarea()