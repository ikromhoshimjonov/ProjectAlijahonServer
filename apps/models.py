from xmlrpc.client import DateTime

from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import CASCADE
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Model, CharField, TextField, DecimalField, ImageField, ForeignKey, IntegerField, \
    DateTimeField, SET_NULL, TextChoices
from django.db.models.fields import SlugField, DateField
from django.utils.text import slugify


class BaseSlugModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255,unique=True, blank=True, null=True)

    class Meta:
        abstract = True


    def save(self,**kwargs):
       slug = slugify(self.name)
       i = 1
       while Category.objects.filter(slug = slug).exists():
            slug += f"-{i}"
            i+=1
       self.slug = slug
       super().save()

class Category(BaseSlugModel):
    icon = CharField(max_length=300)

    def __str__(self):
        return self.name

class Product(BaseSlugModel):
    description = RichTextUploadingField()
    price = DecimalField(max_digits=10, decimal_places=2)
    image = ImageField(upload_to="images/")
    quantity =IntegerField(null=True,blank=True)
    category = ForeignKey("apps.Category",on_delete=CASCADE)
    telegram_url = CharField(max_length=255,null=True,blank=True)

    discount_price = DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    discount = CharField(max_length=255,blank=True,null=True)

class Wishlist(Model):
    user= ForeignKey("apps.User",on_delete=CASCADE)
    product = ForeignKey("apps.Product",on_delete=CASCADE)


class CustomUserManager(UserManager):
    def _create_user(self, phone_number, password, **extra_fields):

        if not phone_number:
            raise ValueError("The given phone number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number,  password, **extra_fields)

    def create_superuser(self,phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class StatusRole(TextChoices):
        ADMIN = "admin","Admin"
        USER = "user","User"
        OPERATOR = "operator"
    objects = CustomUserManager()
    USERNAME_FIELD = "phone_number"
    username = None

    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    district = ForeignKey("apps.District",on_delete=SET_NULL,null=True,blank=True)
    address = CharField(max_length=255)
    telegram_id = IntegerField(unique=True,blank=True,null=True)
    about = TextField()
    role = CharField(max_length=25,choices=StatusRole,default=StatusRole.USER)
    phone_number = CharField(max_length=20,unique=True)
    balance = CharField(max_length=255,default=0)


class Payment(Model):
    class StatusType(TextChoices):
        Review = "review","Review"
        COMPLETED = "completed","Completed"
        CANCEL = "cancel","Cancel"

    user = ForeignKey("apps.User",on_delete=CASCADE)
    photo = ImageField(upload_to="payments_photos/",blank=True)
    payment_at = DateTimeField(auto_now_add=True)
    status = CharField(max_length=20,choices=StatusType,default=StatusType.Review)
    description = TextField(blank=True,null=True)
    card_number = CharField(max_length=16,null=True,blank=True)
    transferred_amount = CharField(max_length=255,null=True,blank=True)


class District(Model):
    name  = CharField(max_length=255)
    region = ForeignKey("apps.Region",on_delete=CASCADE)


class Region(Model):
    name = CharField(max_length=255)


class Thread(Model):
    user = ForeignKey("apps.User",on_delete=CASCADE,blank=True)
    product  = ForeignKey("apps.Product",on_delete=CASCADE,related_name="threed")
    discount_sum = IntegerField(null=True,blank=True,default=0)
    name = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    visit_count = IntegerField(null=True, blank=True,default=0)
    payment = ForeignKey("apps.Payment",on_delete=CASCADE,null=True,blank=True,related_name="threed")




    @property
    def product_threed_price(self):
        return self.product.price - self.discount_sum






class Order(Model):
    class StatusType(TextChoices):
        NEW = "new", "New"
        PENDING = "pending","Pending"
        COMPLETED = "completed","Completed"
        CANCELED = "canceled","Canceled"
        READY_TO_ORDER = "ready_to_order","Ready To Order"
        DELIVERING = "delivering","Delivering"
        ARCHIVED = "archived","Archived"
        DELIVERED = "delivered","Delivered"
        NOT_PICK_UP = "not_pick_up","Not pick up"
        CANCEL_CALL = "cancel_call","Cancel_call"
        CONFIRMED = "confirmed","Confirmed"

    full_name = CharField(max_length=200)
    owner = ForeignKey("apps.User",on_delete=SET_NULL,null=True,blank=True,related_name="orders")
    phone_number = CharField(max_length=20)
    ordered_at = DateTimeField(auto_now_add=True)
    threed = ForeignKey("apps.Thread",on_delete=SET_NULL,null=True,blank=True,related_name="orders")
    product = ForeignKey("apps.Product",on_delete=CASCADE ,null=True ,blank=True,related_name="thread_order")
    district = ForeignKey("apps.District",on_delete=SET_NULL,related_name="district",null=True,blank=True)
    quantity = IntegerField(default=1)
    status = CharField(max_length=15,choices=StatusType,default=StatusType.NEW)
    update_at = DateTimeField(auto_now=True)
    comment_operator = CharField(max_length=255,null=True,blank=True)
    send_order = DateTimeField(null=True,blank=True)
    operator = CharField(max_length=255,null=True,blank=True)
    deliver = CharField(max_length=255,null=True,blank=True)
    total_amount = CharField(max_length=255,blank=True,null=True)
    price  = IntegerField()


    @property
    def amount_sum(self):
        return self.quantity*self.product.price

    @property
    def product_discount_threed(self):
        return self.quantity * float(self.threed.product_threed_price)

class DeliverPrice(Model):
    price_deliver = IntegerField()
    image = ImageField(upload_to="admin/images")
    start = DateField(blank=True,null=True)
    finish = DateField(blank=True,null=True)






