from django.conf.urls import patterns, include, url
from django.views.decorators.csrf import csrf_exempt

from views import *

urlpatterns = patterns('',
    url(r'^index$', IndexView.as_view(), name='home'),
    url(r'^business/(?P<company_name>\w+)$', CompanyDetailView.as_view(), name='company-detail'),
    url(r'^business$', CompanyListView.as_view(), name='company-list'),
    url(r'^products$', ProductListView.as_view(), name='product-list'),
    url(r'^product/(?P<pk>\d+)$', ProductDetailView.as_view(), name='product-detail'),
    url(r'^contact$', csrf_exempt(ContactView.as_view()), name='contact-add'),
)
