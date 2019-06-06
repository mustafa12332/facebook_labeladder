from django import forms


class PageForm(forms.Form):
    page_id = forms.CharField(required=True,label="Page Id")
    page_authtoken = forms.CharField(required=True,label="Page Authentication Token")
    label_id = forms.CharField(required=False,label="Label Id")
    csv_file = forms.FileField()
