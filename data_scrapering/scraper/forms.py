from django import forms
from .models import ObjectModel


class IdForm(forms.ModelForm):
    product_id = forms.CharField(label='Product Id')

    class Meta:
        model = ObjectModel
        fields = {'product_id',}
