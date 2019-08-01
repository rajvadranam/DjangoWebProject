from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.contrib.auth.forms import UserCreationForm

#App models here.
# deptment model
class Dept(models.Model):
    dpt_id = models.CharField(max_length=4,primary_key=True)
    name = models.CharField(max_length=50)
    college_name = models.CharField(max_length=50)
# student model
class Stud(models.Model):
    stu_id = models.CharField(max_length=9,primary_key=True)
    short_id = models.CharField(max_length=9)
    stu_name = models.CharField(max_length=26)
    dpt_id = models.ForeignKey(Dept,on_delete=models.CASCADE)
    d_typ = models.CharField(max_length=2)
    gender = models.CharField(max_length=2)
    email= models.CharField(max_length=26)
    address = models.CharField(max_length=250)
# library memebr model
class Libmem(models.Model):
    cwid = models.OneToOneField(Stud,on_delete=models.CASCADE)
    dpt_id = models.ForeignKey(Dept, on_delete=models.CASCADE)
# User profile model
class UserProfile(models.Model):
      user = models.OneToOneField(User,on_delete=models.CASCADE)
      City = models.CharField(max_length=50,default="NA")
      phone =models.IntegerField(default=0)

# Librarian model
class Librn(models.Model):
    lb_id = models.CharField(primary_key=True,max_length=9)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=26)
    dpt_id = models.ForeignKey(Dept,on_delete=models.CASCADE)
    d_typ = models.CharField(max_length=2)
    gender = models.CharField(max_length=2)
    address = models.CharField(max_length=250)
# Author model
class Atr(models.Model):
    a_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length = 26)
    title = models.CharField(max_length=5)
    email = models.CharField(max_length=26)
# books model
class Bks(models.Model):
    b_id = models.CharField(primary_key=True,max_length = 26)
    dpt_id = models.ForeignKey(Dept, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    email = models.CharField(max_length=26)
    desc= models.CharField(max_length=400)
    type = models.CharField(max_length=20)
    edition = models.CharField(max_length=8)
    p_year = models.IntegerField()
    pub = models.CharField(max_length=50)
    a_id = models.ForeignKey(Atr, on_delete=models.CASCADE)
# inventory model
class Invt(models.Model):
    i_id = models.OneToOneField(Bks,on_delete=models.CASCADE)
    shelf = models.CharField(max_length=10)
    rack = models.CharField(max_length=5)
    row = models.IntegerField()
    qty=models.IntegerField()
# Borrowed model
class Bowed(models.Model):
    b_id = models.ForeignKey(Bks,on_delete=models.CASCADE)
    cwid = models.ForeignKey(Libmem,on_delete=models.CASCADE)
    due = models.DateField()
    issue = models.DateField()
    i_id =models.ForeignKey(Invt, on_delete=models.CASCADE)
# book Order model
class Border(models.Model):
    lb_id = models.ForeignKey(Librn,on_delete=models.CASCADE)
    qty = models.IntegerField()
    i_id =models.ForeignKey(Invt, on_delete=models.CASCADE)
    status=models.CharField(max_length=26)

# User profile creation model
def create_profile(sender,**kwargs):
    if kwargs['created']:
        u_profile = UserProfile.objects.create(user=kwargs['instance'])


#adding a signal for creating a user profile on save
post_save.connect(create_profile,sender=User)

