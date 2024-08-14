# forms.py
from django import forms
from .models import AnnouncedPUResults, PollingUnit
from django.utils import timezone

class ResultsForm(forms.ModelForm):
    class Meta:
        model = AnnouncedPUResults
        fields = ['polling_unit_uniqueid', 'party_abbreviation', 'party_score', 'entered_by_user', 'date_entered', 'user_ip_address']

    polling_unit_uniqueid = forms.ChoiceField(choices=[], label='Polling Unit')
    party_abbreviation = forms.CharField(max_length=4, label='Party Abbreviation')
    party_score = forms.IntegerField(label='Party Score')
    entered_by_user = forms.CharField(max_length=50, label='Entered By User')
    date_entered = forms.DateTimeField(label='Date Entered', initial=timezone.now)
    user_ip_address = forms.GenericIPAddressField(label='User IP Address')

    def __init__(self, *args, **kwargs):
        polling_units_choices = kwargs.pop('polling_units_choices', [])
        super().__init__(*args, **kwargs)
        self.fields['polling_unit_uniqueid'].choices = polling_units_choices