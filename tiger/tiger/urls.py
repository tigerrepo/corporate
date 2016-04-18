from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from solid_i18n.urls import solid_i18n_patterns
from views import *

urlpatterns = solid_i18n_patterns(
    '',
    url(r'^index$', IndexView.as_view(), name='home'),
    url(r'^business/(?P<company_name>\w+)$', CompanyDetailView.as_view(), name='company-detail'),
    url(r'^business$', CompanyListView.as_view(), name='company-list'),
    url(r'^products$', ProductListView.as_view(), name='product-list'),
    url(r'^product/(?P<pk>\d+)$', ProductDetailView.as_view(), name='product-detail'),
    url(r'^contact$', csrf_exempt(ContactView.as_view()), name='contact-add'),
    url(r'^features', PriceView.as_view(), name='price-detail'),
    url(r'^search$', SearchView.as_view(), name='search'),
    url(r'^join$', JoinUsView.as_view(), name='kick-start'),
    url(r'^support$', SupportView.as_view(), name='support'),
    url(r'^success$', SuccessView.as_view(), name='success'),
)
