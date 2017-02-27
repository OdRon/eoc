from django.conf.urls import url, include
from overview.views import *
from . import views

urlpatterns = [
    url(r'^login/$', views.Login, name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^$', views.Login),
    url(r'^home/$', views.Tab_Home, name='home'),
    url(r'^call_reports/$', views.Call_Report, name='call_reports'),
    url(r'^agg_reports/$', views.Report_Agg, name='agg_reports'),
    url(r'^events_reports/$', views.Report_Events, name='events_reports'),
    url(r'^disease_reports/$', views.Report_Disease, name='disease_reports'),
    url(r'^daily_reports/$', views.daily_reports, name='daily_reports'),
    url(r'^daily_report_submit/$', views.daily_report_submit, name='daily_report_submit'),
    url(r'^weekly_report_submit/$', views.weekly_report_submit, name='weekly_report_submit'),
    url(r'^weekly_reports/$', views.Report_Weekly, name='weekly_reports'),
    url(r'^dsru_reports/$', views.Report_DSRU, name='dsru_reports'),
    url(r'^week_shift/$', views.Week_Shift, name='week_shift'),
    url(r'^rrt_shift/$', views.RRT_Shift, name='week_shift'),
    url(r'^allocation_sheet/$', views.Allocation_Sheet, name='week_shift'),
    url(r'^eoc_cont/$', views.eoc_contacts, name='eoc_cont'),
    url(r'^contact_json/$', views.contact_json, name='contact_json'),
    url(r'^get_existing_timetable/$', views.get_existing_timetable, name='get_existing_timetable'),
    url(r'^get_timetables/$', views.get_timetables, name='get_timetables'),
    url(r'^significant_events_create/', views.significant_events_create, name='significant_events_create'),
    url(r'^media_report_create/', views.media_report_create, name='media_report_create'),
    url(r'^field_deployments_create/', views.field_deployments_create, name='field_deployments_create'),
    url(r'^call_logs_cordinates/$', views.call_logs_cordinates, name='call_logs_cordinates'),
    #trial class
    url(r'^trial/', views.trial),
    url(r'^myModal/', views.modal),

    #contacts class
    url(r'^eoc/', views.eoc_contacts),


    #Forms
    # url(r'^event_create/', views.event_create),
    # url(r'^call_log_create/', views.call_log_create),
    # url(r'^disease_create/', views.disease_create),

    # edited forms
    url(r'^disease_create/', disease_create.as_view(), name='disease_create'),
    url(r'^disease_create_submit/', views.disease_create_submit,name='disease_create_submit'),
    url(r'^event_create/', event_create.as_view(), name='event_create'),
    url(r'^get_subcounty/', views.get_subcounty,name='get_subcounty'),
    url(r'^get_county/', views.get_county,name='get_county'),
    url(r'^get_diseases/', views.get_diseases,name='get_diseases'),
    url(r'^get_disease_cordinates/', views.get_disease_cordinates,name='get_disease_cordinates'),
    url(r'^event_create_submit/', views.event_create_submit, name='event_create_submit'),
    url(r'^call_log_create/', views.call_log_create,name='call_log_create'),
    url(r'^call_log_create_submit/', views.call_log_create_submit,name='call_log_create_submit'),

    # Form Edits
    url(r'^(?P<id>\d+)/event_edit/$', views.event_update),
    url(r'^(?P<id>\d+)/disease_edit/$', views.disease_update),
    #url(r'^(?P<id>\d+)/call_log_edit/$', views.call_log_update),

    #form Views
    url(r'^(?P<id>\d+)/disease_view/$', views.disease_view),
    url(r'^(?P<id>\d+)/event_view/$', views.event_view),
    url(r'^(?P<id>\d+)/call_log_view/$', views.call_log_view),
    #Contacts
    url(r'^all_contacts/', views.All_contacts_report, name='all_contacts'),
    url(r'^(?P<id>\d+)/contact_type/$', views.Contact_type_report),

    # mappings

    url(r'^facilities_mappings/$', views.facilities_mappings,name='facilities_mappings'),
    url(r'^get_facilities/$', views.get_facilities,name='get_facilities'),
    url(r'^heat_maps/$', views.heat_maps,name='heat_maps'),
]