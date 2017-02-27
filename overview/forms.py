from django import forms
from .models import *
#from django.contrib.admin.widgets import widgets
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
from django.forms.fields import DateField, TimeField

class PostEvent(forms.ModelForm):

    class Meta:
        model = Event
        fields = [
            "event_type",
            "data_source",
            "region",
            "remarks"
        ]

class PostSignificantEvent(forms.ModelForm):

    class Meta:
        model = Significant_event
        fields = [
            "date_created",
            "description"

        ]

class PostMediaReport(forms.ModelForm):

    class Meta:
        model = Media_report
        fields = [
            "date_created",
            "description"

        ]


class PostDisease(forms.ModelForm):

    class Meta:
        model = Disease
        fields = [
            "disease_type",
            "data_source",
            "region",
            "remarks"
        ]

class PostCallLog(forms.ModelForm):
    date_reported = DateField(widget = AdminDateWidget)
    # time_reported = TimeField(widget = AdminTimeWidget)
    #time_reported = forms.TimeField(widget=widgets.AdminTimeWidget)
    #date_reported = forms.DateField(widget=widgets.AdminDateWidget)
    class Meta:
        model = Call_log
        fields = [
            "disease_type",
            "event_type",
            "county",
            "location",
            "caller_name",
            "caller_number",
            # "time_reported",
            "date_reported",
            "description",
            "action_taken"
        ]



