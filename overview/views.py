from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from er_system import settings
from django.core.mail.message import EmailMessage
from django.contrib.auth.decorators import login_required
from .models import *
#from .forms import *
import time
from django.views.generic.base import TemplateView
import json
from django.core import serializers
from django.http import JsonResponse
from django.db import connection
contacts = Contact_type.objects.all()

def Login(request):
    next = request.GET.get('next', '/home/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, "overview/log.html", {'redirect_to': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)

@login_required
def Tab_Home(request):

     #Populating the pie_chart
    counties = County.objects.all().exclude(description = 'none')
    disease_types = Disease_type.objects.all()
    disease_report_stat= {}
    for disease_type in disease_types:
       diseases_count = Disease.objects.all().filter(disease_type_id=disease_type.id).count()
       if diseases_count > 0:
        disease_report_stat[disease_type.description] = diseases_count


    #Populating the bargraph
    counties = County.objects.all().exclude(description = 'none')
    call_stats = {}#variable that collects county descriptions from their id's (to be used as an index)
    for county in counties:
        call_count = Call_log.objects.all().filter(county_id = county.id).count()
        if call_count > 0:
            call_stats[county.description] = call_count
        else:
            call_stats[county.description] = 0


    #
    # for county in counties:
    #     call_count = Call_log.objects.all().filter(county_id = county.id).count()
    #     if call_count > 0:
    #         call_stats[county.description] = call_count
    #
    #     for subcnty in sub_counties:
    #         call_subcny = Call_log.objects.all().filter(subcounty_id = subcnty.id).filter(county_id = county.id).count()
    #         if call_subcny > 0:
    #             sub_call_stat[subcnty.subcounty, county.description] = call_subcny

    #Populating the marquee
    _call_logs = Call_log.objects.all().filter(incident_status_id = 2).order_by("-date_reported")[:7]
    _events = Event.objects.all().filter(incident_status_id = 2).order_by("-date_created")[:7]
    _disease = Disease.objects.all().filter(incident_status_id = 2).order_by("-date_created")[:7]
    marquee_call_log = []#an array that collects all confirmed diseases and maps them to the marquee
    marquee_disease = []#an array that collects all confirmed diseases and maps them to the marquee
    marquee_events = []#an array that collects all confirmed diseases and maps them to the marquee
    for _logs in _call_logs:
       # marquee.append("CONFIRMED CALL LOGS : ")
        marquee_call_log.append(_logs)
        #marquee_call_log.append(_logs.mortality)
    for _eve in _events:
       # marquee.append("LATEST EVENTS : ")
        marquee_events.append(_eve)
        #marquee_events.append("......")
    for _dis in _disease:
       # marquee.append("LATEST DISEASE : ")
        marquee_disease.append(_dis)
       # marquee_disease.append(_dis.mortality)

    #Diseases reported
    d_count = Disease.objects.all().order_by("-date_created")[:7].count()
     #confirmed cases
    conf_disease_count = Disease.objects.all().filter(incident_status_id = 2).order_by("-date_created")[:7].count()
    conf_disease_call_log_count = Call_log.objects.all().filter(disease_type_id__gt=0).filter(incident_status_id=2).order_by("-date_reported")[:7].count()
    d_conf_count=conf_disease_count+conf_disease_call_log_count
    #Events reported
    e_count = Event.objects.all().order_by("-date_created")[:7].count()
     #confirmed cases
    conf_event_count = Event.objects.all().filter(incident_status_id = 2).order_by("-date_created")[:7].count()
    conf_event_call_log_count = Call_log.objects.all().filter(event_type_id__gt=0).filter(incident_status_id=2).order_by("-date_reported")[:100].count()
    e_conf_count=conf_event_count+conf_event_call_log_count

    values = {'vals': Call_log.objects.all().order_by("-date_reported")[:5]
        ,'disease_vals':Disease.objects.all().order_by("-date_created")[:5]
        ,'event_vals': Event.objects.all().order_by("-date_created")[:5]

        # , 'elements': call_stats
    }
    #cnts = {'contact_type_vals': contacts}
    # trl1 = {'elements':[{'label': 'Mombasa', 'y': '15'}, {'label': 'Kisumu', 'y': '50'}, {'label': 'Nairobi', 'y': '80'}]}
    trl1 = {'elements': call_stats,'disease_report_stat': disease_report_stat, 'marquee_disease': marquee_disease,'marquee_events': marquee_events,'marquee_call_log': marquee_call_log, 'd_count': d_count, 'd_conf_count': d_conf_count, 'e_count': e_count, 'e_conf_count': e_conf_count}
    v = {'valz': values, 'trl': trl1,'contact_type_vals': contacts}

    return render(request, 'overview/dashboard.html', v)

def call_logs_cordinates(request):

    if request.method=="POST":
        # allvals=Call_log.objects.filter(county__in=County.objects.all())
        # allvals=County.objects.filter(description__in=Call_log.objects.all())
        # # Article.objects.filter(reporter__in=Reporter.objects.filter(first_name='John')).distinct()

        # jsondata = serializers.serialize('json', allvals,use_natural_foreign_keys=True,use_natural_primary_keys=True)

        # return HttpResponse(jsondata,content_type="application/json")

        allvals = Call_log.objects.select_related('county').all()
        allvals2 = Disease.objects.select_related('subcounty').all()
        mydata=[]
        for x in allvals:
            result={}
            result['latitude']=x.county.latitude
            result['longitude']=x.county.longitude
            # result['longitude']=x.county.longitude
            result['position']=x.county.description
            mydata.append(result)

        # for y in allvals2:
        #     result2={}
        #     result2['dlatitude']=y.subcounty.latitude
        #     result2['dlongitude']=y.subcounty.longitude
        #     # result['longitude']=x.county.longitude
        #     result2['dposition']=y.subcounty.subcounty
        #     mydata.append(result2)

        jsondata = json.dumps(mydata)


        return HttpResponse(jsondata,content_type="application/json")




@login_required
def Call_Report(request):
    values = {'vals': Call_log.objects.all(),'contact_type_vals':contacts}
    #cnts = {'contact_type_vals': contacts}
    #v = {'valz': values}
    return render(request, 'overview/call_report.html', values)

@login_required
def Report_Agg(request):
    values = {'contact_type_vals':contacts}
    return render(request, 'overview/log_aggregate.html',values)

@login_required
def Report_Events(request):
    events = {'event_vals': Event.objects.all(),'contact_type_vals':contacts}
    return render(request, 'overview/events_report.html', events)

@login_required
def Report_Disease(request):
    disease = {'disease_vals': Disease.objects.all(),'contact_type_vals':contacts}
    return render(request, 'overview/disease_report.html', disease)

@login_required
def daily_reports(request):
    return render(request, 'overview/daily_report.html')

@login_required
def weekly_report_submit(request):

    disease_types = Disease_type.objects.all()
    disease_report_stat= {}
    for disease_type in disease_types:
       diseases_count = Disease.objects.all().filter(disease_type_id=disease_type.id).count()
       disease_report_stat[disease_type.description] = diseases_count

    #x = request.POST.get('date_from','')
    #print x
    date_from = request.POST.get('date_from','')
   # y =request.POST.get('date_to','')
    date_to = request.POST.get('date_to','')

    call_log_count_stat= {}
    disease_types = Disease_type.objects.all()
    for disease_type in disease_types:
       call_logs_count = Call_log.objects.all().filter(disease_type_id=disease_type.id).filter(date_reported__range=[date_from, date_to]).count()
       call_log_count_stat[disease_type.description] =  call_logs_count
       call_log_sum = sum(call_log_count_stat.values())

    regions = Region.objects.all()
    diseases_list = {}
    events_list = {}
    for region in regions:
       diseases = Disease.objects.all().filter(region_id=region.id).filter(date_created__range=[date_from, date_to])
       diseases_list[region.description] = diseases
       events = Event.objects.all().filter(region_id=region.id).filter(date_created__range=[date_from, date_to])
       events_list[region.description] = events


    significant_events = Significant_event.objects.all().filter(date_created__range=[date_from, date_to])
    if not significant_events :
     significant_events_none="None"

    media_reports = Significant_event.objects.all().filter(date_created__range=[date_from, date_to])
    if not media_reports :
     media_reports_none="None"

    events = {'event_vals': Event.objects.all(),"diseases": diseases_list,"date_from":date_from,"date_to":date_to,"media_reports":media_reports,"media_reports_none":media_reports_none,"significant_events_none": significant_events_none,"significant_events": significant_events, "events": events_list, "call_log_count_stat": call_log_count_stat, "call_log_sum": call_log_sum}
    return render(request, 'overview/weekly_report.html', events)



@login_required
def daily_report_submit(request):

    disease_types = Disease_type.objects.all()
    disease_report_stat= {}
    for disease_type in disease_types:
       diseases_count = Disease.objects.all().filter(disease_type_id=disease_type.id).count()
       disease_report_stat[disease_type.description] = diseases_count

    datefilter =request.POST.get('date_reported','')
    call_log_count_stat= {}
    disease_types = Disease_type.objects.all()
    for disease_type in disease_types:
       call_logs_count = Call_log.objects.all().filter(disease_type_id=disease_type.id).filter(date_reported=datefilter).count()
       call_log_count_stat[disease_type.description] =  call_logs_count
       call_log_sum = sum(call_log_count_stat.values())

    regions = Region.objects.all()
    diseases_list = {}
    events_list = {}
    for region in regions:
       diseases = Disease.objects.all().filter(region_id=region.id).filter(date_created=datefilter)
       diseases_list[region.description] = diseases
       events = Event.objects.all().filter(region_id=region.id).filter(date_created=datefilter)
       events_list[region.description] = events


    significant_events = Significant_event.objects.all().filter(date_created=datefilter)
    if not significant_events :
     significant_events_none="None"

    media_reports = Significant_event.objects.all().filter(date_created=datefilter)
    if not media_reports :
     media_reports_none="None"

    events = {'event_vals': Event.objects.all(),"media_reports":media_reports,"media_reports_none":media_reports_none,"date_filter":datefilter,"significant_events_none": significant_events_none,"significant_events": significant_events,"diseases": diseases_list, "events": events_list, "call_log_count_stat": call_log_count_stat, "call_log_sum": call_log_sum}
    return render(request, 'overview/daily_report.html', events)

@login_required
def Report_Weekly(request):
    return render(request, 'overview/weekly_report.html')

@login_required
def Report_DSRU(request):
    dsru = {'dsru_vals': DSRU_Weekly_Event.objects.all()}
    return render(request, 'overview/dsru-report.html', dsru)

def trial(request):
    return render(request, 'overview/dashboard.html')

def modal(request):
    return render(request, 'overview/modal.html')

# Contacts list
def eoc_contacts(request):
    eoc = { 'eocContacts': EOC_Contacts.objects.all()}
    return render(request, 'overview/surveillance_contacts.html', eoc)

@login_required
def Week_Shift(request):
    return render(request, 'overview/weekly_shift.html')

@login_required
def RRT_Shift(request):
    return render(request, 'overview/rrt_shift.html')

@login_required
def Allocation_Sheet(request):
    return render(request, 'overview/alocation_sheet.html')

@login_required
# def EOC_Contact(request):
#     # eoc_cnts = { 'eoc_conts': EOC_Contacts.objects.all() }
#     return render(request, 'overview/eoc_contacts.html')
#updates from forms
def significant_events_create(request):
    if request.method == "POST":
        form = PostSignificantEvent(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.user_id = 1
            instance.user_id = request.user.id

            instance.save()
            return redirect('/significant_events_create')
    else:
        form = PostSignificantEvent()
    return render(request, "overview/significant_events.html", {'form': form})

def media_report_create(request):
    if request.method == "POST":
        form = PostMediaReport(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.user_id = 1
            instance.user_id = request.user.id

            instance.save()
            return redirect('/media_report_create')
    else:
        form = PostMediaReport()
    return render(request, "overview/media_reports.html", {'form': form})

def field_deployments_create(request):
    if request.method == "POST":
        form = PostField_deployment(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.user_id = 1
            #instance.user_id = request.user.id

            instance.save()
            return redirect('/daily_report_field_deployment')
    else:
        form = PostField_deployment()
    return render(request, "overview/daily_report_field_deployment.html", {'form': form})

def media_summary_create(request):
    if request.method == "POST":
        form = PostMedia_summary(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.user_id = 1
            #instance.user_id = request.user.id

            instance.save()
            return redirect('/daily_report_media_reports_summary')
    else:
        form = PostMedia_summary()
    return render(request, "overview/daily_report_media_reports_summary.html", {'form': form})

#updates from forms


def event_update(request, id = None):
    instance = get_object_or_404(Event, id = id)
    form = PostEvent(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    context = {
        "instance":instance,
        "form": form,
    }
    return render(request, "overview/post_event.html",context)

class disease_create(TemplateView):
    template_name="overview/disease_form.html"

    def get_context_data(self):

        # eventT=Event_type.objects.all()
        diseaseT=Disease_type.objects.all().exclude(description = 'none')
        dataS=Data_source.objects.all().exclude(description = 'none')
        # countyt=County.objects.all()
        region = Region.objects.all().exclude(description = 'none')
        status=Incident_status.objects.all()
        day = time.strftime("%Y-%m-%d")
        success=""
        return {'success':success,'disease_type':diseaseT,'data_source':dataS,'region':region,'status':status,'day':day}

def disease_create_submit(request):
    if request.method=='POST':

        diseaseType=request.POST.get('disease_type','')
        dataSource=request.POST.get('data_source','')
        region=request.POST.get('region','')
        date_c=request.POST.get('date_created','')
        remarksd=request.POST.get('remarks','')
        county='none'
        status=request.POST.get('status','')
        mortality=request.POST.get('mortality','')
        cases=request.POST.get('cases','')
        deaths=request.POST.get('deaths','')
        subcounty='none'
        if(region=='kenya'):
            county=request.POST.get('county','')
            subcounty=request.POST.get('subcounty','')


        dataS=Data_source.objects.get(description=dataSource)
        # eventT=Event_type.objects.all()
        diseaseT=Disease_type.objects.get(description=diseaseType)
        countyt=County.objects.get(description=county)
        subcountyt=Sub_county.objects.get(subcounty=subcounty)
        statust=Incident_status.objects.get(description=status)

        # countyt=County.objects.all()
        regionD = Region.objects.get(description=region)
        cur_user=request.user.username
        usert=User.objects.get(username=cur_user)
        #usert=request.user.username


        diseaseForm=Disease_type.objects.all()
        dataForm=Data_source.objects.all()
        # countyt=County.objects.all()
        regionForm = Region.objects.all()
        status=Incident_status.objects.all()
        day = time.strftime("%Y-%m-%d")

        insertdata=Disease(disease_type=diseaseT,data_source=dataS,incident_status=statust,cases=cases,deaths=deaths,county=countyt,subcounty=subcountyt,region=regionD,user=usert,date_created=date_c,remarks=remarksd)
        insertdata.save()
        #find ways of retrieving the saved id and loop to send the success message after confirmation
        success="form inserted successfully"
        return render(request,"overview/disease_form.html",{"success":success,'disease_type':diseaseForm,'data_source':dataForm,'region':regionForm,'status':status,'day':day})

    else:
        success="form not inserted,try again"
        diseaseForm=Disease_type.objects.all()
        dataForm=Data_source.objects.all()
        status=Incident_status.objects.all()
        day = time.strftime("%Y-%m-%d")
        # countyt=County.objects.all()
        regionForm = Region.objects.all()
        return render(request,"overview/disease_form.html",{"success":success,'disease_type':diseaseForm,'data_source':dataForm,'region':regionForm,'status':status,'day':day})



@login_required
def disease_view(request, id = None):
    instance = get_object_or_404(Disease, id = id)

    context = {
        "disease_instance":instance,
    }
    return render(request, "overview/disease_view.html",context)

@login_required
def event_view(request, id = None):
    instance = get_object_or_404(Event, id = id)

    context = {
        "event_instance":instance,
    }
    return render(request, "overview/event_view.html",context)

@login_required
def call_log_view(request, id = None):
    instance = get_object_or_404(Call_log, id = id)

    context = {
        "call_log_instance":instance,
    }
    return render(request, "overview/call_log_view.html",context)


def disease_update(request, id = None):
    instance = get_object_or_404(Disease, id = id)
    form = PostDisease(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    context = {
        "instance":instance,
        "form": form,
    }
    return render(request, "overview/post_disease.html",context)


def call_log_create(request):

    # template_name="overview/post_call_log.html"
    template_name="overview/call_logs_form.html"
    diseaseT=Disease_type.objects.all().exclude(description = 'none')
    eventT=Event_type.objects.all().exclude(description = 'none')
    countyt = County.objects.all().exclude(description = 'none')
    day = time.strftime("%Y-%m-%d")

    return render(request,"overview/call_logs_form.html", {'disease_type':diseaseT,'event_type':eventT,'county':countyt,'day':day})
    # return render(request,"overview/heat_maps.html")

#Contacts Reports
def contact_json(request):
    all_ = Contact.objects.all()

    serialized = serializers.serialize('json', all_,use_natural_foreign_keys=True,use_natural_primary_keys=True)
    obj_list=json.loads(serialized)

    return HttpResponse(json.dumps(obj_list),content_type='application/json')

def get_timetables(request):
    if request.method=='POST':
        contactarray=request.POST.getlist('contactsarray[]')
        fdate=request.POST.get('fromdate','')
        tdate=request.POST.get('todate','')
        for x in contactarray:
            insertingcont=mytimetable(fname=x,from_date=fdate,to_date=tdate)
            insertingcont.save()

    myresponse="success adding contacts to timetable"
    data=json.dumps(myresponse)


    return HttpResponse(data,content_type="application/json")


def get_existing_timetable(request):
    all_ = mytimetable.objects.all()

    serialized = serializers.serialize('json', all_,use_natural_foreign_keys=True,use_natural_primary_keys=True)
    obj_list=json.loads(serialized)

    return HttpResponse(json.dumps(obj_list),content_type='application/json')

def Contact_type_report(request, id):
    contacts = Contact_type.objects.all()
    contacts = {'contacts_val': Contact.objects.all().filter(contact_type_id = id),
                'contact_type_description': Contact_type.objects.get(pk = id),
                'contact_type_vals': Contact_type.objects.all()}

    return render(request, 'overview/all_contacts_report.html', contacts)


def All_contacts_report(request):

    contacts = {'contacts_val': Contact.objects.all(),
                'contact_type_vals': Contact_type.objects.all()}

    return render(request, 'overview/all_contacts_report.html', contacts)


class event_create(TemplateView):
    template_name="overview/events_form.html"

    def get_context_data(self):

        # eventT=Event_type.objects.all()
        eventT=Event_type.objects.all().exclude(description = 'none')
        dataS=Data_source.objects.all()
        status=Incident_status.objects.all()
        day = time.strftime("%Y-%m-%d")
        # countyt=County.objects.all()
        region = Region.objects.all()
        success=""
        return {'success':success,'event_type':eventT,'data_source':dataS,'region':region,'status':status,'day':day}




def event_create_submit(request):
    if request.method=='POST':

        eventType=request.POST.get('event_type','')
        dataSource=request.POST.get('data_source','')
        region=request.POST.get('region','')
        date_c=request.POST.get('date_created','')
        remarksd=request.POST.get('remarks','')
        county='none'
        status=request.POST.get('status','')
        mortality=request.POST.get('mortality','')
        cases=request.POST.get('cases','')
        deaths=request.POST.get('deaths','')
        subcounty='none'
        if(region=='kenya'):
            county=request.POST.get('county','')
            subcounty=request.POST.get('subcounty','')


        dataS=Data_source.objects.get(description=dataSource)
        # eventT=Event_type.objects.all()
        eventT=Event_type.objects.get(description=eventType)
        countyt=County.objects.get(description=county)
        subcountyt=Sub_county.objects.get(subcounty=subcounty)
        statust=Incident_status.objects.get(description=status)

        # countyt=County.objects.all()
        regionD = Region.objects.get(description=region)
        cur_user=request.user.username
        usert=User.objects.get(username=cur_user)
        #usert=request.user.username


        eventForm=Event_type.objects.all()
        dataForm=Data_source.objects.all()
        # countyt=County.objects.all()
        regionForm = Region.objects.all()
        status=Incident_status.objects.all()
        day = time.strftime("%Y-%m-%d")

        # insertdata=Disease(disease_type=diseaseT,data_source=dataS,incident_status=statust,mortality=mortality,county=countyt,subcounty=subcountyt,region=regionD,user=usert,date_created=date_c,remarks=remarksd)
        insertdata=Event(event_type=eventT,data_source=dataS,incident_status=statust,cases=cases,deaths=deaths,county=countyt,subcounty=subcountyt,region=regionD,user=usert,date_created=date_c,remarks=remarksd)
        insertdata.save()
        #find ways of retrieving the saved id and loop to send the success message after confirmation
        success="form inserted successfully"
        return render(request,"overview/events_form.html",{"success":success,'event_type':eventForm,'data_source':dataForm,'region':regionForm,'status':status,'day':day})

    else:
        success="form not inserted,try again"
        eventForm=Event_type.objects.all()
        dataForm=Data_source.objects.all()
        status=Incident_status.objects.all()
        day = time.strftime("%Y-%m-%d")
        # countyt=County.objects.all()
        regionForm = Region.objects.all()
        return render(request,"overview/events_form.html",{"success":success,'event_type':eventForm,'data_source':dataForm,'region':regionForm,'status':status,'day':day})


def call_log_create_submit(request):
    if request.method=='POST':
        diseaseType=request.POST.get('disease_type','')
        eventType=request.POST.get('event_type','')
        county=request.POST.get('county','')
        subcounty=request.POST.get('subcounty','')
        location=request.POST.get('location','')
        callerName=request.POST.get('caller_name','')
        callerNumber=request.POST.get('caller_number','')
        dateReported=request.POST.get('date_reported','')
        description=request.POST.get('description','')
        actionTaken=request.POST.get('action_taken','')

        if diseaseType=='none':
            diseaseType='none'
        if eventType=='none':
            eventType='none'
            #send email when the disease type is Guinea worm
            if diseaseType == "Guinea worm":
              subject = "Guinea-worm suspected case-EOC"
              message = "Caller name:"+callerName+",Phone number:"+callerNumber+",County:"+county+",Sub county:"+subcounty+",Description:" +description+",action taken:"+ actionTaken
              from_email = "nyangat@yahoo.com"
              #send_mail(subject,message,from_email, ['tnyanga@mhealthkenya.org'])

              email = EmailMessage(subject,message,from_email, ['tnyanga@mhealthkenya.org'])
              email.send()

        diseaseT=Disease_type.objects.get(description=diseaseType)
        # eventT=Event_type.objects.all()
        eventT=Event_type.objects.get(description=eventType)
        # countyt=County.objects.all()
        countyt = County.objects.get(description=county)
        subcountyt = Sub_county.objects.get(subcounty=subcounty)
        cur_user=request.user.username
        usert=User.objects.get(username=cur_user)
        #usert=request.user.username

        diseaseForm=Disease_type.objects.all()
        # eventT=Event_type.objects.all()
        eventForm=Event_type.objects.all()
        # countyt=County.objects.all()
        countyForm = County.objects.all()


        Call_log.objects.create(disease_type=diseaseT,event_type=eventT,location=location,user=usert,county=countyt,subcounty=subcountyt,caller_name=callerName,caller_number=callerNumber,date_reported=dateReported,description=description,action_taken=actionTaken)

        return HttpResponse('')



def facilities_mappings(request):


    return render(request, 'overview/facilities_mappings.html')


def heat_maps(request):

    return render(request, 'overview/heat_maps.html')


def get_facilities(request):

    if request.method=="POST":
        allvals=list(coordinates.objects.values())

        data=json.dumps(allvals)

        return HttpResponse(data,content_type="application/json")

def get_subcounty(request):
    if request.method=="POST":
        mycounty=request.POST.get('county','')
        # lname=request.POST.get('mylname')
        mysubcounty=County.objects.get(description=mycounty)
        #mydic={}

        allvals=Sub_county.objects.filter(county=mysubcounty)
        # mytable.objects.create(fname=fname,lname=lname)
        # mylist=json.loads(allvals)
        #mydic['mydata']=allvals

        # mydic.update({'mydata':allvals})

        # data=json.dumps(mydic)
        serialized=serializers.serialize('json',allvals)
        obj_list=json.loads(serialized)


        return HttpResponse(json.dumps(obj_list),content_type="application/json")
        # return HttpResponse()

def get_county(request):
    if request.method=="POST":


        allvals=County.objects.all()
        # mytable.objects.create(fname=fname,lname=lname)
        # mylist=json.loads(allvals)
        #mydic['mydata']=allvals

        # mydic.update({'mydata':allvals})

        # data=json.dumps(mydic)
        serialized=serializers.serialize('json',allvals)
        obj_list=json.loads(serialized)


        return HttpResponse(json.dumps(obj_list),content_type="application/json")


def get_diseases(request):
    if request.method=="POST":

        allvals=Disease_type.objects.all().exclude(description = 'none')

        serialized=serializers.serialize('json',allvals)
        obj_list=json.loads(serialized)


        return HttpResponse(json.dumps(obj_list),content_type="application/json")


def get_disease_cordinates(request):

    if request.method=="POST":

        dtype=request.POST.get('dtype','')

        mydtype=Disease_type.objects.get(description=dtype)

        allvals=list(Disease.objects.filter(disease_type=mydtype).values('county__description','county__latitude','county__longitude'))

        data=json.dumps(allvals)

    return HttpResponse(data,content_type="application/json")





