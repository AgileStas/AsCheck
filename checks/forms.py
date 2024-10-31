from django import forms

from .models import Division, Host, Person

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
                )

    hostname = forms.CharField(max_length=100)
    division = DivisionChoiceField()
    serialnumber = forms.CharField(max_length=100)
    cs_manufacturer = forms.CharField(max_length=100)
    cs_model = forms.CharField(max_length=100)
    cs_systemfamily = forms.CharField(max_length=100, required=False)
    restriction = forms.ChoiceField(required=False, choices=Host.Restriction)
    owner = forms.CharField(required=False)
    person = PersonChoiceField()
    # check_date = forms.DateTimeField(required=False)
    note = forms.CharField(required=False)
