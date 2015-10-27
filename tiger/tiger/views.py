import collections

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import Http404, get_object_or_404, redirect, render
from django.utils.timezone import localtime, now
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView

from tiger import forms, models, settings


class IndexView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        companies = models.Company.objects.filter(status=1)

        company_tag_dict = collections.defaultdict(list)
        for item in models.CompanyTag.objects.filter():
            company_tag_dict[item.company_id].append(item.tag.name)

        company_video_dict = {}
        for video in models.Video.objects.all():
            company_video_dict[video.company_id] = (video.host_url, video.video_url, video.name)
        company_list = []
        for company in companies:
            company_dict = model_to_dict(company)
            company_dict['tag'] = ','.join(company_tag_dict.get(company.id, ['Others']))
            video_tuple = company_video_dict.get(company.id, ('','', ''))
            company_dict['video_host_url'] = "%s%s" % (settings.VIDEO_URL, video_tuple[0])
            company_dict['youtube_url'] = "%s%s" % (settings.YOUTUBE_URL_PREFIX, video_tuple[2])
            company_dict['video_url'] = video_tuple[1]
            company_dict['poster_url'] = "%s%s/%s.jpg" % (settings.VIDEO_URL, company.id, company.id)
            company_list.append(company_dict)

        products = models.Product.objects.filter(status=1).order_by("-id")[0:3]
        product_list = []
        for product in products:
            product_dict = model_to_dict(product)
            try:
                gallery = models.Gallery.objects.get(product=product, is_cover=1)
                cover_image = "%s%s" % (settings.IMAGE_URL_PREFIX, gallery.image_url)
            except models.Gallery.DoesNotExist:
                cover_image = '%sdefault.jpg' % settings.IMAGE_URL_PREFIX
            product_dict['cover_image'] = cover_image
            product_dict['company_name'] = product.company.name
            product_dict['company_url'] = product.company.url
            product_dict['create_date'] = product.create_date
            product_list.append(product_dict)

        context['domain'] = settings.IMAGE_URL_PREFIX
        context['companies'] = company_list
        context['latest'] = product_list
        context['url_path'] = 'index'
        return context

class CompanyDetailView(TemplateView):
    template_name = "company_detail.html"

    def get_context_data(self, **kwargs):
        context = super(CompanyDetailView, self).get_context_data(**kwargs)

        company_url = self.kwargs['company_name']
        company = get_object_or_404(models.Company, url=company_url, status=1)
        context['company'] = company
        context['video_url'] = "%s%s/%s.mp4" % (settings.VIDEO_URL, company.id, company.id)
        context['poster_url'] = "%s%s/%s.jpg" % (settings.VIDEO_URL, company.id, company.id)

        products = models.Product.objects.filter(company=company, status=1)
        product_list = []
        for product in products:
            product_dict = model_to_dict(product)
            try:
                gallery = models.Gallery.objects.get(product=product, is_cover=1)
                cover_image = "%s%s" % (settings.IMAGE_URL_PREFIX, gallery.image_url)
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
        for item in models.CompanyTag.objects.filter():
            company_tag_dict[item.company_id].append(item.tag.name)

        tags = models.Tag.objects.filter(status=1)
        companies = models.Company.objects.filter(status=1)
        company_list = []
        for company in companies:
            company_dict = model_to_dict(company)
            company_dict['tag_list'] = ' '.join(company_tag_dict.get(company.id, ['Others']))
            company_dict['video_url'] = "%s%s/%s.mp4" % (settings.VIDEO_URL, company.id, company.id)
            company_dict['poster_url'] = "%s%s/%s.jpg" % (settings.VIDEO_URL, company.id, company.id)
            company_list.append(company_dict)

        context['tags'] = tags
        context['companies'] = company_list
        context['url_path'] = 'business'
        return context

class ProductListView(TemplateView):
    template_name = "product.html"
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

        product_cover_image = {}
        for gallery in models.Gallery.objects.all():
            if gallery.is_cover:
                product_cover_image[gallery.product_id] = gallery.image_url
        products = models.Product.objects.filter(status=1)
        product_list = []
        for product in products:
            product_dict = model_to_dict(product)
            if product.id in product_cover_image:
                cover_image = "%s%s" % (settings.IMAGE_URL_PREFIX, product_cover_image[product.id])
            else:
                cover_image = '%sdefault.jpg' % settings.IMAGE_URL_PREFIX
            product_dict['cover_image'] = cover_image
            product_dict['company_name'] = product.company.name
            product_dict['create_date'] = product.create_date
            product_list.append(product_dict)

        paginator = Paginator(product_list, settings.PAGE_COUNT)
        page = self.request.GET.get('page')
        try:
            product_list = paginator.page(page)
        except PageNotAnInteger:
            product_list = paginator.page(1)
        except EmptyPage:
            product_list = paginator.page(paginator.num_pages)

        context['products'] = product_list
        context['url_path'] = 'product'
        return context

class ProductDetailView(DetailView):
    template_name = "product_detail.html"
    model = models.Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)

        context['url_path'] = 'product'
        return context

class ContactView(FormView):
    form_class = forms.ContactForm
    template_name = "contact.html"

    def form_valid(self, form):
        print form.cleaned_data
        form.instance.company_id = form.cleaned_data['company_id']
        form.save()
        return HttpResponse("OK")
