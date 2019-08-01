"""
Definition of urls for DjangoWebProject3.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^inv', app.views.inv, name='inv'),
    url(r'^rep', app.views.Reports, name='rep'),
    url(r'^profile', app.views.profile, name='profile'),
    url(r'^allbooks', app.views.allbooks, name='allbooks'),
    url(r'^genSearch', app.views.genSearch, name='genSearch'),
    url(r'^forgot', app.views.forgot, name='forgot'),
    url(r'^addList', app.views.AddtoBorrowList, name='AddToList'),
     url(r'^DelinList', app.views.DelinInventory, name='DelinList'),
    url(r'^addInventory', app.views.Addtoinventory, name='AddToInv'),
    url(r'^OrderInventory', app.views.OrderforInventory, name='Orders'),
    url(r'^searchdel', app.views.SearchdelInv, name='SearchdelInv'),
    url(r'^Editdetails', app.views.EditbookDetails, name='EditDetails'),
    url(r'^returned', app.views.RemoveFromBorrowList, name='RemovefromDetails'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
     url(r'^register', app.views.register, name='register'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
]
