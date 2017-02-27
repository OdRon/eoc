from django.db import models
from datetime import date
from django.contrib.auth.models import User

class County(models.Model):
    description= models.CharField(max_length=1000)
    longitude=models.CharField(max_length=1000, default=36.8167)
    latitude=models.CharField(max_length=1000, default=-1.2833)

    def natural_key(self):
        return (self.description)

    def __str__(self):
        return self.description

    class meta:
        unique_together=(('description'),)


class Sub_county(models.Model):
    county=models.ForeignKey(County,on_delete=models.CASCADE)
    subcounty=models.CharField(max_length=1000)
    longitude=models.CharField(max_length=1000, default=36.8167)
    latitude=models.CharField(max_length=1000, default=-1.2833)

    def natural_key(self):
        return (self.subcounty)

    def __str__(self):
        return self.subcounty

    class meta:
        unique_together=(('subcounty'),)


class Facilities(models.Model):

    mfl_code=models.CharField(max_length=1000)
    facility_name=models.CharField(max_length=1000)
    facility_level=models.CharField(max_length=1000)
    latitude=models.CharField(max_length=1000)
    longitude=models.CharField(max_length=1000)

    def __str__(self):
        return self.facility_name



class Police_posts(models.Model):

    post_code=models.CharField(max_length=1000)
    post_name=models.CharField(max_length=1000)
    latitude=models.CharField(max_length=1000)
    longitude=models.CharField(max_length=1000)

    def __str__(self):
        return self.post_name

class Referal_labs(models.Model):

    referal_code=models.CharField(max_length=1000)
    referal_name=models.CharField(max_length=1000)
    latitude=models.CharField(max_length=1000)
    longitude=models.CharField(max_length=1000)

    def __str__(self):
        return self.referal_name




class Incident_status(models.Model):
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.description


class Event_type(models.Model):
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.description


class Disease_type(models.Model):
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.description

class Region(models.Model):
    description = models.CharField(max_length=1000)

    def natural_key(self):
        return (self.description)

    def __str__(self):
        return self.description

    class meta:
        unique_together=(('description'),)


class Data_source(models.Model):
    description = models.CharField(max_length=500)

    def natural_key(self):
        return (self.description)

    def __str__(self):
        return self.description

    class meta:
        unique_together=(('description'),)

class Contact_type(models.Model):
    description = models.CharField(max_length=500)

    def natural_key(self):
        return (self.description)

    def __str__(self):
        return self.description

    class meta:
        unique_together=(('description'),)

class Contact(models.Model):
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    contact_type = models.ForeignKey(Contact_type, on_delete=models.CASCADE, default=0)
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500)
    designation = models.CharField(max_length=500)
    phone_number = models.IntegerField(default=0)
    email_address = models.EmailField(max_length=500)

    def __str__(self):
        return self.county.description + ' - ' + self.contact_type.description

class Event(models.Model):
    event_type = models.ForeignKey(Event_type, on_delete=models.CASCADE)
    data_source = models.ForeignKey(Data_source, on_delete=models.CASCADE)
    incident_status = models.ForeignKey(Incident_status, on_delete=models.CASCADE, default=1)
    county = models.ForeignKey(County, on_delete=models.CASCADE, default=1)
    subcounty = models.ForeignKey(Sub_county, on_delete=models.CASCADE, default=1)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date_created = models.DateField(default=date.today)
    mortality = models.IntegerField(default=0)
    cases = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    remarks = models.TextField(max_length=1000)

    class Meta:
       ordering = ['-date_created']

    def __str__(self):
       return str(self.date_created) + ' - ' +self.event_type.description + ' - ' + self.region.description + ' - ' + self.data_source.description


class Significant_event(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date_created = models.DateField(default=date.today)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.description)

class Media_report(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date_created = models.DateField(default=date.today)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return str(self.description)


class Disease(models.Model):
    disease_type = models.ForeignKey(Disease_type, on_delete=models.CASCADE)
    data_source = models.ForeignKey(Data_source, on_delete=models.CASCADE)
    incident_status = models.ForeignKey(Incident_status, on_delete=models.CASCADE, default=1)
    county = models.ForeignKey(County, on_delete=models.CASCADE, default=1)
    subcounty = models.ForeignKey(Sub_county, on_delete=models.CASCADE, default=1)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    date_created = models.DateField(default=date.today)
    mortality = models.IntegerField(default=0)
    cases = models.IntegerField(default=0)
    deaths = models.IntegerField(default=0)
    remarks = models.TextField(max_length=1000)

    class Meta:
       ordering = ['-date_created']
    def __str__(self):
        return str(self.date_created) + ' - ' + self.disease_type.description + ' - ' + self.region.description + ' - ' + self.data_source.description


class Call_log(models.Model):
    disease_type = models.ForeignKey(Disease_type, on_delete=models.CASCADE, default=0)
    event_type = models.ForeignKey(Event_type, on_delete=models.CASCADE, default=0)
    county = models.ForeignKey(County, on_delete=models.CASCADE, default=1)
    incident_status = models.ForeignKey(Incident_status, on_delete=models.CASCADE,default=1)
    subcounty = models.ForeignKey(Sub_county, on_delete=models.CASCADE, default=1)
    location = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    caller_name = models.CharField(max_length=500)
    caller_number = models.IntegerField(default=0)
    date_reported = models.DateField(default=date.today)
    description = models.TextField(max_length=1000)
    action_taken = models.TextField(max_length=1000)


    class Meta:
       ordering = ['-date_reported']
    def __str__(self):
        return self.disease_type.description + ' - ' + self.county.description



    #def __str__(self):
      #  return str(self.date_reported) + ' - ' + self.disease_type.description + ' - ' + self.county.description + ' - ' +self.location + ' - ' + self.description

class Designation(models.Model):
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.description


class EOC_Contacts(models.Model):
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, default=0)
    mobile = models.CharField(max_length=30)
    email = models.EmailField(max_length=500)

    def __str__(self):
        return self.first_name + ' - ' + self.mobile


class EOC_Shifts(models.Model):
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    week_no = models.CharField(max_length=50)
    officer_name = models.ForeignKey(EOC_Contacts, on_delete=models.CASCADE, default=0)
    # _designation = models.ForeignKey(EOC_Contacts, on_delete=models.CASCADE, default=0)
    # _mobile = models.ForeignKey(EOC_Contacts, on_delete=models.CASCADE, default=0)
    # _email = models.ForeignKey(EOC_Contacts, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.officer_name.officer_name


class RRT_Shifts(models.Model):
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    week_no = models.CharField(max_length=50)
    officer_name = models.ForeignKey(EOC_Contacts, on_delete=models.CASCADE, default=0)
    # _designation = models.ForeignKey(EOC_Contacts, on_delete=models.CASCADE, default=0)
    # _mobile = models.ForeignKey(EOC_Contacts, on_delete=models.CASCADE, default=0)
    # _email = models.ForeignKey(EOC_Contacts, on_delete=models.CASCADE, default=0)

    def __str__(self):
        return self.officer_name.officer_name


class DSRU_Weekly_Event(models.Model):
    disease = models.ForeignKey(Disease_type, on_delete=models.CASCADE)
    district = models.CharField(max_length=500)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    province = models.CharField(max_length=500)
    wk_no = models.IntegerField(default=0)
    wn_end = models.DateField(default=date.today)
    cases_under_5 = models.IntegerField(default=0)
    cases_over_5 = models.IntegerField(default=0)
    total_cases = models.IntegerField(default=0)
    death_under_5 = models.IntegerField(default=0)
    death_over_5 = models.IntegerField(default=0)
    total_death = models.IntegerField(default=0)
    year = models.IntegerField(default=2000)
    reported = models.DateField(default=date.today)
    designation = models.CharField(max_length=500)
    date_reported = models.DateField(default=date.today)

    def __str__(self):
        return self.disease.description + ' - ' + self.district + ' - ' + self.county.description


class coordinates(models.Model):

    longitude=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    position=models.CharField(max_length=50)

    def __str__(self):

        return self.position

class mytimetable(models.Model):

    fname=models.CharField(max_length=1000)
    from_date=models.CharField(max_length=500,default="")
    to_date=models.CharField(max_length=500,default="")
    deleted=models.CharField(max_length=20,default="N")

    def __str__(self):
        return self.fname
