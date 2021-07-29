from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from crispy_forms.helper import FormHelper
from .models import Event, Location, Asset
from django_better_admin_arrayfield.models.fields import ArrayField
from django_better_admin_arrayfield.forms.widgets import DynamicArrayWidget
from django.utils.datastructures import MultiValueDict


class ArrayFieldSelectMultiple(forms.SelectMultiple):
    """This is a Form Widget for use with a Postgres ArrayField. It implements
    a multi-select interface that can be given a set of `choices`.
    You can provide a `delimiter` keyword argument to specify the delimeter used.
    """
    def __init__(self, *args, **kwargs):
        # Accept a `delimiter` argument, and grab it (defaulting to a comma)
        self.delimiter = kwargs.pop('delimiter', ',')
        super().__init__(*args, **kwargs)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            # Normally, we'd want a list here, which is what we get from the
            # SelectMultiple superclass, but the SimpleArrayField expects to
            # get a delimited string, so we're doing a little extra work.
            return self.delimiter.join(data.getlist(name))

        return data.get(name)

    def get_context(self, name, value, attrs):
        return super().get_context(name, value.split(self.delimiter), attrs)


class EventCreationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """ Grants access to the request object so that only members of the current user
        are given as options"""

        self.request = kwargs.pop('request')
        super(EventCreationForm, self).__init__(*args, **kwargs)

        self.fields['Locations'].queryset = Location.objects.filter(
            user=self.request.user)

        self.fields['Assets'].queryset = Asset.objects.filter(
            user=self.request.user)

    class Meta:
        model = Event
        fields = ['Name', 'Photo', 'Locations', 'Assets', 'starting_date', 'ending_date']
        widgets = {
            'starting_date': forms.DateInput(format=('%Y-%m-%d'),
                                             attrs={'class': 'datepicker1', 'placeholder': 'Select Date', 'type': 'date'}),
            'ending_date': forms.DateInput(format=('%Y-%m-%d'),
                                             attrs={'class': 'datepicker2', 'placeholder': 'Select Date',
                                                    'type': 'date'})
        }

    Photo = forms.ImageField()

    Locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    # Locations = forms.ModelMultipleChoiceField(
    #     queryset=Location.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    Assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )


class AssetCreationForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = ['Expiry_date', 'Expiry_time',]
        widgets = {
            'Expiry_date': forms.DateInput(format=('%Y-%m-%d'),
                                             attrs={'class': 'datepicker1', 'placeholder': 'Select Date', 'type': 'date'}),
            'Expiry_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            # 'Asset_File':forms.FileField( attrs={'onchange': 'handleContentUpload(this)'})
        }
        # longitude1 = ArrayField(
        #     forms.CharField(max_length=100), size=2,
        # )
        # longitude1 = ArrayFieldSelectMultiple()
    # Asset_File = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))




class LocationCreationForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     """ Grants access to the request object so that only members of the current user
    #     are given as options"""
    #
    #     self.request = kwargs.pop('request')
    #     super(LocationCreationForm, self).__init__(*args, **kwargs)
    #
    #     self.fields['Assets'].queryset = Asset.objects.filter(
    #         user=self.request.user)


    class Meta:
        model = Location
        # fields = ['Name', 'Longitude', 'Latitude', 'Google_maps_link', 'Plus_code', 'Radius', 'Assets']
        fields = ['Longitude1', 'Latitude1', 'Assets']
        # widgets = {
        #     'Expiry_date': forms.DateInput(format=('%Y-%m-%d'),
        #                                      attrs={'class': 'datepicker1', 'placeholder': 'Select Date', 'type': 'date'}),
        #     'Expiry_time': forms.TimeInput(format='%H:%M',attrs={'type': 'time'}),
        # }

    Longitude = forms.NumberInput()
    Latitude = forms.NumberInput()
    # Radius = forms.NumberInput()
    # Google_maps_link = forms.CharField()
    # Plus_code = forms.CharField()



    Assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )



