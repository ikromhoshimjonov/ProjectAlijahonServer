from django.contrib import admin

from apps.models import Product, Category, User, DeliverPrice, Order, Payment, Thread


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
        exclude = "slug",

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
         pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(DeliverPrice)
class DeliverPriceAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
        def save_model(self, request, obj, form, change):
            status = form.cleaned_data.get("status")
            order_id = obj.id
            object = Order.objects.filter(pk=order_id).first()
            if status == "confirmed" and object.threed_id:
                product_id = object.product_id
                product_price = Product.objects.filter(pk=product_id).first().discount_price
                threed_price = Thread.objects.filter(pk=obj.threed_id).first().discount_sum
                total_summa = float(product_price) - float(threed_price)
                user_balance = User.objects.filter(pk=request.user.id).first().balance
                total_summa = total_summa + float(user_balance)
                User.objects.filter(pk=request.user.id).update(balance=total_summa)





@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id","card_number","status","payment_at","user"]

    def save_model(self, request, obj, form, change):
        if change:
            if obj.status == "cancel":
                user = obj.user
                balance = user.balance
                balance = float(balance) + float(obj.transferred_amount)
                user.balance = balance
                user.save()
        super().save_model( request, obj, form, change)

    def get_readonly_fields(self, request, obj =None):
        if obj.status == "completed":
            return "status",
        return []


