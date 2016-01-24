import collections
import json
from django.core.cache import cache

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import Http404, get_object_or_404, redirect, render
from django.utils.timezone import localtime, now
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView

from tiger import forms, models, settings
import  logging

logger = logging.getLogger('main')

class IndexView(TemplateView):
    template_name = "index.html"
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        companies = models.Company.objects.filter(status=models.Account.STATUS_ENABLE, is_index=True).order_by("dis_order")

        company_tag_dict = collections.defaultdict(list)
        for item in models.CompanyTag.objects.all():
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
            # company_dict['video_url'] = video_tuple[1]
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
            product_dict['company_name'] = product.company.name
            product_dict['company_url'] = product.company.url
            product_dict['create_date'] = product.create_date
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

        company_url = self.kwargs['company_name']
        company = get_object_or_404(models.Company, url=company_url, status=1)
        if company.status != models.Account.STATUS_ENABLE:
            raise Http404
        context['company'] = company
        try:
            video = models.Video.objects.get(company=company)
            context['youtube_url'] = "%s%s" % (settings.YOUTUBE_URL_PREFIX, video.name)
        except models.Video.DoesNotExist:
            context['youtube_url'] = ""
        context['pdf_url'] = "%s%s/%s" % (settings.PDF_URL, company.id, company.pdf_url)
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
        tag_company_dict = collections.defaultdict(list)
        for item in models.CompanyTag.objects.all():
            company_tag_dict[item.company_id].append(item.tag.name)
            tag_company_dict[item.tag_id].append(item.company_id)

        company_video_dict = {}
        for video in models.Video.objects.all():
            company_video_dict[video.company_id] = (video.host_url, video.video_url, video.name)

        tags = models.Tag.objects.filter(status=1)
        companies = models.Company.objects.filter(status=1).order_by('name')
        company_list = []
        for company in companies:
            company_dict = model_to_dict(company)
            company_dict['tag_list'] = ' '.join(company_tag_dict.get(company.id, ['Others']))
            video_tuple = company_video_dict.get(company.id, ('','', ''))
            # company_dict['video_host_url'] = "%s%s" % (settings.VIDEO_URL, video_tuple[0])
            company_dict['youtube_url'] = "%s%s" % (settings.YOUTUBE_URL_PREFIX, video_tuple[2])
            # company_dict['video_url'] = video_tuple[1]
            # company_dict['poster_url'] = "%s%s/%s.jpg" % (settings.VIDEO_URL, company.id, company.id)
            company_list.append(company_dict)

        context['tags'] = [tag for tag in tags if tag_company_dict.get(tag.id, [])]
        context['companies'] = company_list
        context['url_path'] = 'business'
        logger.info("data:%s", context)
        return context

class ProductListView(TemplateView):
    template_name = "product.html"
    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)

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
        if self.object.status != 1 or self.object.company.status != 1:
            raise Http404

        galleries =  models.Gallery.objects.filter(product=self.object)
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

    def get_initial(self):
        initials = {}
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
        context['results'] = models.Company.objects.filter(name__contains=keyword)
        context['keyword'] = keyword
        context['r_count'] = len(context['results'])
        context['searched'] = True
        return render(self.request, self.template_name, context)


class SuccessView(TemplateView):
    template_name = "success.html"
