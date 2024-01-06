from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()


class DataFilterForm(forms.Form):
    startDate = forms.DateField(label="Start date")
    endDate = forms.DateField(label="End date")
    category = forms.CharField(label="Category")
