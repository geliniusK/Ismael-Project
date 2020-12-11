from django import forms

class ItemForm(forms.Form):
    item = forms.CharField(max_length=50)
