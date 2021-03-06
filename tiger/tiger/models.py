from django.db import models
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Account(models.Model):
    username = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    salt = models.CharField(max_length=32)
    STATUS_ENABLE = 1
    STATUS_DISABLE = 0
    STATUS_CHOICES = (
        (STATUS_ENABLE, 'Activated'),
        (STATUS_DISABLE, 'Deactivated'),
    )
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    ACCOUNT_TYPE_ADMIN = 0
    ACCOUNT_TYPE_CUSTOMER = 1
    ACCOUNT_TYPE_CHOICES = (
        (ACCOUNT_TYPE_CUSTOMER, u'Customer Admin'),
        (ACCOUNT_TYPE_ADMIN, u'System Admin'),
    )
    account_type = models.SmallIntegerField(choices=ACCOUNT_TYPE_CHOICES, default=1)

    class Meta:
        db_table = "account_tab"
        in_db = "tiger"

    def __unicode__(self):
        return self.username


class Company(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slogan = models.CharField(max_length=128, default='')
    url = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=1024)
    create_time = models.DateTimeField(auto_now_add=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=Account.STATUS_DISABLE)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    is_index = models.BooleanField(default=False)
    address = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    tel = models.CharField(max_length=20)
    fax = models.CharField(max_length=20, default='')
    dis_order = models.IntegerField(default=0)
    logo_url = models.CharField(max_length=64)
    tel_opt = models.CharField(max_length=20, default='')
    open_from = models.CharField(max_length=20, default='')
    open_to = models.CharField(max_length=20, default='')
    
    class Meta:
        db_table = "company_tab"
        in_db = "tiger"

    def __unicode__(self):
        return self.name


class Video(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=1024)
    video_url = models.CharField(max_length=256)
    host_url = models.CharField(max_length=128)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    class Meta:
        db_table = "video_tab"
        in_db = "tiger"


class Contact(models.Model):
    sender = models.CharField(max_length=32)
    mobile = models.CharField(max_length=20)
    email = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=512)
    create_date = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)

    class Meta:
        db_table = 'contact_tab'
        in_db = "tiger"

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)
    class_name = models.CharField(max_length=64, unique=True)
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'tag_tab'
        in_db = "tiger"

    def __unicode__(self):
        return self.name


class CompanyTag(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    tag = models.ForeignKey(Tag, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('company', 'tag')
        db_table = 'company_tag_tab'
        in_db = "tiger"


class Product(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=1)

    class Meta:
        unique_together = ('company', 'name')
        db_table = 'product_tab'
        in_db = "tiger"

    def __unicode__(self):
        return self.name


class Gallery(models.Model):
    name = models.CharField(max_length=64)
    image_url = models.ImageField(upload_to='gallery/%Y%m%d', max_length=64)
    is_cover = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    class Meta:
        unique_together = ('name', 'product')
        db_table = 'gallery_tab'
        in_db = "tiger"

    def __unicode__(self):
        return self.name


class Enquiry(models.Model):
    name = models.CharField(max_length=64)
    company = models.CharField(max_length=128)
    email = models.CharField(max_length=64)
    mobile = models.CharField(max_length=20)
    REGION_TYPE_JU = 0
    REGION_TYPE_CO = 1
    REGION_TYPE_PAY = 2
    REGION_TYPE_OT = 3
    REGION_TYPE_CHOICES = (
        (REGION_TYPE_JU, u'Join Us'),
        (REGION_TYPE_CO, u'Collaboration Opportunities'),
        (REGION_TYPE_PAY, u'Payment'),
        (REGION_TYPE_OT, u'Others'),
    )
    region = models.SmallIntegerField(choices=REGION_TYPE_CHOICES, default=0)
    ip = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField()

    class Meta:
        db_table = 'enquiry_tab'
        in_db = "tiger"

    def __unicode__(self):
        return self.name


class HotCompany(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    dis_order = models.IntegerField(default=1)

    class Meta:
        db_table = 'hot_company_tab'
        in_db = "tiger"


class PDF(models.Model):
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    url = models.FileField(upload_to='pdf', max_length=128)
    status = models.SmallIntegerField(choices=Account.STATUS_CHOICES, default=1)

    class Meta:
        db_table = 'pdf_tab'
        in_db = "tiger"
