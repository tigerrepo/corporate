from django.core.cache import cache

from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import Http404, get_object_or_404, render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

import forms
import models
import settings
import logging
import collections
import random

# from django.utils.timezone import localtime, now
# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from django.core.urlresolvers import reverse
# import json

logger = logging.getLogger('main')


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        companies = models.Company.objects.\
            filter(status=models.Account.STATUS_ENABLE).order_by('-id')[0:9]

        company_tag_dict = collections.defaultdict(list)
        for item in models.CompanyTag.objects.all():
            company_tag_dict[item.company_id].append(item.tag.name)

        # company_video_dict = {}
        # for video in models.Video.objects.all():
        #     company_video_dict[video.company_id] = (video.host_url, video.video_url, video.name)
        company_list = []
        for company in companies:
            company_dict = model_to_dict(company)
            company_dict['tag'] = ','.join(company_tag_dict.get(company.id, ['Others']))
            company_list.append(company_dict)

        products = [obj for obj in
                    models.Product.objects.select_related("company").filter(status=1).order_by("-id")
                    if obj.company.status == models.Account.STATUS_ENABLE][0:3]
        product_list = []
        for product in products:
            product_dict = model_to_dict(product)
            try:
                gallery = models.Gallery.objects.get(product=product, is_cover=1)
                cover_image = "%s%s/%s" % (settings.IMAGE_URL_PREFIX, product.id, gallery.image_url)
            except models.Gallery.DoesNotExist:
                cover_image = '%sdefault.jpg' % settings.IMAGE_URL_PREFIX
            product_dict['cover_image'] = cover_image
            product_dict['company_id'] = product.company.id
            product_dict['company_url'] = product.company.url
            product_dict['create_date'] = product.create_date
            product_dict['company_name'] = product.company.name
            product_list.append(product_dict)

        context['domain'] = settings.IMAGE_URL_PREFIX
        context['companies'] = company_list
        context['latest'] = product_list
        context['url_path'] = 'index'
        return context


class CompanyDetailView(FormView):
    template_name = "company_detail.html"
    form_class = forms.ContactForm

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)

        company_id = self.kwargs['company_id']
        company = get_object_or_404(models.Company, id=company_id, status=1)
        if company.status != models.Account.STATUS_ENABLE:
            raise Http404
        context['company'] = company
        # try:
        #     video = models.Video.objects.get(company=company)
        #     context['youtube_url'] = "%s%s?rel=0" % (settings.YOUTUBE_URL_PREFIX, video.name)
        # except models.Video.DoesNotExist:
        #     context['youtube_url'] = ""

        # pdfs = models.PDF.objects.filter(company=company, status=1)
        # pdf_urls = []
        # for pdf in pdfs:
        #     pdf_url = "%s%s/%s" % (settings.PDF_URL, company.id, pdf.url)
        #     pdf_urls.append((pdf_url, pdf.name))
        # context['pdf_urls'] = pdf_urls
        if company.logo_url:
            context['logo_url'] = "%s%s/%s" % (settings.LOGO_URL, company.id, company.logo_url)
        else:
            context['logo_url'] = ''
        products = models.Product.objects.filter(company=company, status=1)
        product_list = []
        for product in products:
            product_dict = model_to_dict(product)
            try:
                gallery = models.Gallery.objects.get(product=product, is_cover=1)
                cover_image = "%s%s/%s" % (settings.IMAGE_URL_PREFIX, product.id, gallery.image_url)
            except models.Gallery.DoesNotExist:
                cover_image = '%sdefault.jpg' % settings.IMAGE_URL_PREFIX
            product_dict['cover_image'] = cover_image
            product_dict['company_name'] = product.company.name
            product_dict['create_date'] = product.create_date
            product_list.append(product_dict)

        context['products'] = product_list
        context['url_path'] = 'business'
        return context


class CompanyListView(TemplateView):
    template_name = "company.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyListView, self).get_context_data(**kwargs)

        company_tag_dict = collections.defaultdict(list)
        company_tagname_dict = collections.defaultdict(list)
        tag_company_dict = collections.defaultdict(list)
        for item in models.CompanyTag.objects.select_related("company").all():
            if item.tag.class_name:
                company_tag_dict[item.company_id].append(item.tag.class_name)
            company_tagname_dict[item.company_id].append(item.tag.name)
            if item.company.status == models.Account.STATUS_ENABLE:
                tag_company_dict[item.tag_id].append(item.company_id)

        # company_video_dict = {}
        # for video in models.Video.objects.all():
        #     company_video_dict[video.company_id] = (video.host_url, video.video_url, video.name)

        tags = models.Tag.objects.filter(status=1)
        companies = models.Company.objects.filter(status=1).order_by('-id')
        company_list = []

        for company in companies:
            t = random.randint(0,11)
            company_dict = model_to_dict(company)
            company_dict['tag_list'] = ' '.join(company_tag_dict.get(company.id, ['Others']))
            company_dict['tag_line'] = ', '.join(company_tagname_dict.get(company.id, ['Others']))
            
            if t <= 3:
                company_dict['bg'] = 1
            elif 4 <= t <= 7:
                company_dict['bg'] = 2
            else:
                company_dict['bg'] = 3
            company_list.append(company_dict)
        context['tags'] = [tag for tag in tags if tag_company_dict.get(tag.id, [])]
        context['companies'] = company_list
        context['url_path'] = 'business'
        logger.info("data:%s", context)

        print tags
        return context


class ProductListView(TemplateView):
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        company_tag_dict = collections.defaultdict(list)
        company_tagname_dict = collections.defaultdict(list)
        tag_company_dict = collections.defaultdict(list)
        for item in models.CompanyTag.objects.select_related("company").all():
            company_tag_dict[item.company_id].append(item.tag.class_name)
            company_tagname_dict[item.company_id].append(item.tag.name)
            if item.company.status == models.Account.STATUS_ENABLE:
                tag_company_dict[item.tag_id].append(item.company_id)

        product_cover_image = {}
        for gallery in models.Gallery.objects.all():
            if gallery.is_cover:
                product_cover_image[gallery.product_id] = gallery.image_url
        products = [obj for obj in
                    models.Product.objects.select_related("company").filter(status=1).order_by("name")
                    if obj.company.status == models.Account.STATUS_ENABLE]
        
        product_list = []
        for product in products:
            product_dict = model_to_dict(product)
            if product.id in product_cover_image:
                cover_image = "%s%s/%s" % (settings.IMAGE_URL_PREFIX, product.id, product_cover_image[product.id])
            else:
                cover_image = '%sdefault.jpg' % settings.IMAGE_URL_PREFIX
            company = product.company
            product_dict['tag_list'] = ' '.join(company_tag_dict.get(company.id, ['Others']))
            product_dict['tag_line'] = ', '.join(company_tagname_dict.get(company.id, ['Others']))
            product_dict['cover_image'] = cover_image
            product_dict['company_name'] = product.company.name
            product_dict['create_date'] = product.create_date
            product_list.append(product_dict)

        tags = models.Tag.objects.filter(status=1)
        context['tags'] = [tag for tag in tags if tag_company_dict.get(tag.id, [])]
        context['products'] = product_list
        context['url_path'] = 'product'
        return context


class ProductDetailView(DetailView):
    template_name = "product_detail.html"
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        if self.object.status != 1 or self.object.company.status != 1:
            raise Http404

        galleries = models.Gallery.objects.filter(product=self.object)
        gallery_list = []
        for gallery in galleries:
            d = model_to_dict(gallery)
            d['image_url'] = '%s%s/%s' % (settings.IMAGE_URL_PREFIX, self.object.id, gallery.image_url)
            gallery_list.append(d)
        context['url_path'] = 'product'
        context['galleries'] = gallery_list
        return context


class ContactView(FormView):
    form_class = forms.ContactForm
    template_name = "contact.html"

    def form_valid(self, form):
        ip = self.request.META['REMOTE_ADDR']
        logger.info("contact form data:%s, from client:%s", form.cleaned_data, ip)
        if cache.get(ip, None):
            logger.info("failed contact form data:%s, from client:%s, too frequent", form.cleaned_data, ip)
            cache.set(ip, 1, 300)
            return HttpResponseForbidden()

        form.instance.company_id = form.cleaned_data['company_id']
        form.save()
        cache.set(ip, 1, 300)
        return HttpResponse("0")


class JoinUsView(FormView):
    form_class = forms.JoinUsForm
    template_name = "enquiry.html"
    success_url = "/success"

    def get_context_data(self, **kwargs):
        context = super(JoinUsView, self).get_context_data(**kwargs)
        context['url_path'] = 'join'
        return context

    def get_initial(self):
        initials = dict()
        initials['region'] = self.request.GET.get('region', None)
        return initials

    def form_valid(self, form):
        ip = self.request.META['REMOTE_ADDR']
        logger.info("join us form data:%s, from client:%s", form.cleaned_data, ip)
        if cache.get(ip, None):
            cache.set(ip, 1, 300)
            logger.info("failed join us form data:%s, from client:%s, too frequent", form.cleaned_data, ip)
            form.on_frequent_submit()
            return self.form_invalid(form)

        form.instance.ip = self.request.META['REMOTE_ADDR']
        form.save()
        cache.set(ip, 1, 300)
        return super(JoinUsView, self).form_valid(form)


class PriceView(TemplateView):
    template_name = "pricing.html"

    def get_context_data(self, **kwargs):
        context = super(PriceView, self).get_context_data(**kwargs)
        context['url_path'] = 'price'
        return context


class SearchView(FormView):
    form_class = forms.SearchForm
    template_name = "search.html"

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['url_path'] = 'search'
        return context

    def form_valid(self, form):
        keyword = form.cleaned_data['keyword']
        context = self.get_context_data()
        context['companies'] = models.Company.objects.filter(name__icontains=keyword)
        context['products'] = models.Product.objects.filter(name__icontains=keyword)
        context['keyword'] = keyword
        context['r_count_company'] = len(context['companies'])
        context['r_count_product'] = len(context['products'])
        context['searched'] = True
        return render(self.request, self.template_name, context)


class SuccessView(TemplateView):
    template_name = "success.html"


class SupportView(TemplateView):
    template_name = "support.html"

    def get_context_data(self, **kwargs):
        context = super(SupportView, self).get_context_data(**kwargs)
        context['url_path'] = 'support'
        return context

class PrivacyView(TemplateView):
    template_name = "privacy.html"

    def get_context_data(self, **kwargs):
        context = super(PrivacyView, self).get_context_data(**kwargs)
        context['url_path'] = 'privacy'
        return context