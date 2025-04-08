import re

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Form
from django.forms.fields import CharField, IntegerField
from django.template.defaultfilters import first

from apps.models import User, Order, Thread, Product, Payment


class AuthForm(Form):
    phone_number = CharField(max_length=20)
    password = CharField(max_length=20)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        password = make_password(password)
        return password

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        digits_only = "+"+re.sub(r"\D", "", phone_number)
        return digits_only


class ProfileForm(Form):
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    district_id = CharField(required=False)
    address = CharField(required=False)
    telegram_id = IntegerField(required=False)
    about = CharField(required=False)




class ChangePasswordForm(Form):
    old = CharField(required=True)
    new = CharField(required=True)
    confirm= CharField(required=True)

    def clean_confirm(self):
        new = self.data.get("new")
        confirm = self.cleaned_data.get("confirm")
        if new != confirm:
            raise ValidationError("Not Much !")


    def clean_new(self):
        password = self.cleaned_data.get("new")
        return make_password(password)



    def update(self, user):
        old = self.cleaned_data.get("new")
        User.objects.filter(pk=user.id).update(password = old)


class OrderProductForm(Form):
    phone_number = CharField(max_length=255)
    quantity = IntegerField()
    product_id = IntegerField()
    full_name = CharField(max_length=255)
    price = IntegerField()
    threed_id = IntegerField(required=False)
    total_amount = CharField(required=False)


    def clean_quantity(self):
        quantity = self.cleaned_data.get("quantity")
        product_id = self.data.get("product_id")
        quantity_all = Product.objects.filter(pk=product_id).first().quantity
        if int(quantity_all) >= int(quantity):
            quantity_all = int(quantity_all) - int(quantity)
            Product.objects.filter(pk=product_id).update(quantity=quantity_all)
            return quantity
        else:
            raise ValidationError("Maxsulot soni yetarli emas")





    def save(self):
        return Order.objects.create(**self.cleaned_data)



class ThreedForm(ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["user"].required = False

    class Meta:
        model = Thread
        fields = "name", "discount_sum","product","user"


    def clean_discount_sum(self):
        product_id = self.data.get("product")
        product = Product.objects.filter(pk = product_id).first()
        discount_sum = self.cleaned_data.get("discount_sum")
        if discount_sum:
           if product.discount_price < discount_sum:
               raise ValidationError("Chegirma narxidan oshib etdi ?")
        return discount_sum


class UserDataForm(Form):
    quantity = CharField(max_length=255, required=False)
    district = CharField(max_length=255, required=False)
    status = CharField(max_length=255, required=False)
    send_order = CharField(max_length=255, required=False)
    comment_operator = CharField(max_length=255, required=False)
    operator = CharField(max_length=255, required=False)
    deliver = CharField(max_length=255, required=False)
    id = CharField(max_length=255, required=False)

    def clean_quantity(self):
        order_id = self.data.get("id")
        form_quantity = self.cleaned_data.get("quantity")
        product_id = Order.objects.filter(pk=order_id).first().product_id
        all_quantity = Product.objects.filter(pk=product_id).first().quantity
        old_quantity = Order.objects.filter(pk=order_id).first().quantity
        if self.data.get("status") == "canceled":
            quantity = self.data.get("quantity")
            product_quantity = Product.objects.filter(pk=product_id).first().quantity
            product_all = int(product_quantity)+int(quantity)
            Product.objects.filter(pk=product_id).update(quantity=product_all)
            return 0

        if  int(form_quantity)>int(old_quantity):
           total_quantity = int(form_quantity)-int(old_quantity)
           if total_quantity < int(all_quantity):
               update_quantity = int(all_quantity)-total_quantity
               Product.objects.filter(pk=product_id).update(quantity=update_quantity)
               return form_quantity
           else:
               raise ValidationError("Maxsulot soni yetarli emas (Operator)")
        elif int(form_quantity)==int(old_quantity):
            return int(form_quantity)
        elif int(form_quantity) < int(old_quantity):
            total_quantity = int(old_quantity) - int(form_quantity)
            update_quantity =  int(all_quantity) + total_quantity
            Product.objects.filter(pk=product_id).update(quantity=update_quantity)
            return form_quantity














class DeliverDataForm(Form):
    quantity = CharField(max_length=255, required=False)
    district = CharField(max_length=255, required=False)
    status = CharField(max_length=255, required=False)
    send_order = CharField(max_length=255, required=False)
    comment_operator = CharField(max_length=255, required=False)
    operator = CharField(max_length=255, required=False)
    deliver = CharField(max_length=255, required=False)



class PaymentForm(Form):
    card_number = CharField(max_length=16)
    transferred_amount = CharField(max_length=255)
    user_id = CharField(max_length=233,required=False)


    def clean_transferred_amount(self):
        amount = self.cleaned_data.get("transferred_amount")
        user_id = self.data.get("user_id")
        balance = User.objects.filter(pk=user_id).first().balance
        summa = float(balance) - float(amount)
        if float(amount) >= 10000:
            if summa >= 0:
                return amount
            else:
                raise ValidationError("Hisobingizni yetarli mablag' mavjud emas")
        else:
            raise ValidationError("Minimal summa 10000 so'm etib belgilangan")

    def clean_card_number(self):
        card_number = self.cleaned_data.get("card_number")
        if len(card_number) == 16 and card_number.isdigit():
            return card_number
        else:
            raise ValidationError("Karta raqamingizda kamchilik bor")

    def save(self):
        return Payment.objects.create(**self.cleaned_data)



