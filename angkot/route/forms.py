from django import forms

from angkot.route.models import PROVINCES

class NewTransportationForm(forms.Form):
    province = forms.ChoiceField(choices=PROVINCES)
    city = forms.CharField(max_length=256)
    number = forms.CharField(max_length=64)
    company = forms.CharField(max_length=256, required=False)
    agreeToContributorTerms = forms.CharField()

    def clean_agreeToContributorTerms(self):
        data = self.cleaned_data['agreeToContributorTerms']
        data = data.lower().strip()
        if data != 'true':
            raise forms.ValidationError('Need to accept contributor terms')
        return data == 'true'

