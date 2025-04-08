from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.db.models.aggregates import Count
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView, TemplateView, ListView, View, DetailView

from apps.forms import AuthForm, ProfileForm, ChangePasswordForm, OrderProductForm
from apps.models import User, Product, Category, Region, District, Wishlist, Order, DeliverPrice, Thread


class WishlistView(LoginRequiredMixin, View):
    liked = True
    login_url = reverse_lazy("home")
    def get(self,request, product_id):
        liked = True
        like = Wishlist.objects.filter(product_id = product_id, user_id = self.request.user.id)
        if like.exists():
            like.delete()
            liked = False
        else:
            Wishlist.objects.create(product_id=product_id,user_id = self.request.user.id)

        return JsonResponse({"liked":liked})


class ProductOrderDetailView(DetailView):
    queryset = Product.objects.all()
    template_name ="order/product-order.html"
    slug_url_kwarg = "slug"
    context_object_name = "product"
    form_class = OrderProductForm
    success_url = reverse_lazy("check")







class LikeProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "like_product/like_product.html"
    context_object_name = "products"


    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if Wishlist.objects.filter(user_id=self.request.user.id):
            data["liked_products_id"] = Wishlist.objects.values_list("product_id",flat=True)
            data['like'] = Wishlist.objects.values_list("product_id",flat=True)
        return data

class OrderProductFormView(FormView):
    form_class =  OrderProductForm
    success_url = reverse_lazy("check")
    template_name = "order/product-order.html"


    def form_valid(self, form):
        deliver_price = DeliverPrice.objects.all().first().price_deliver
        form.cleaned_data["owner_id"] = self.request.user.id
        threed_id = form.cleaned_data.get("threed_id")
        if threed_id:
            discount_sum = Thread.objects.filter(pk=threed_id).first().discount_sum
            form.cleaned_data["price"] = (float(self.request.POST.get("price")) - discount_sum) * int((self.request.POST.get("quantity")))
            form.cleaned_data["total_amount"] = form.cleaned_data.get("price") + deliver_price

        else:
            form.cleaned_data["price"] = float(self.request.POST.get("price"))*int((self.request.POST.get("quantity")))
            form.cleaned_data["total_amount"] = form.cleaned_data.get("price") + deliver_price
        order = form.save()
        return render(self.request,"order/check.html",context={"order":order,"a":deliver_price})



    def form_invalid(self, form):

        error_list = []
        for error in form.errors.values():
            messages.error(self.request, error)
            error_list.append(error)

            product_id = self.request.POST.get("product_id")
            slug = Product.objects.filter(pk=product_id).first().slug
        return redirect(reverse("product-order", kwargs={"slug": slug }))


















class  ProductOrdersListView(ListView):
    template_name = "orders_product/order_product.html"
    context_object_name ="orders"


    def get_queryset(self):
        orders = Order.objects.filter(owner_id=self.request.user.id)
        status = self.request.GET.get("status")
        if status:
            orders = orders.filter(status=status)
        return orders










class MarketListView(LoginRequiredMixin, ListView):
    template_name = "Market/market.html"
    queryset = Product.objects.all()
    context_object_name = "markets"
    login_url = reverse_lazy("home")



    def get_context_data(self , **kwargs):
            slug = self.kwargs.get("slug")
            data = super().get_context_data(**kwargs)
            query = self.request.GET.get("search")
            data["categories"] = Category.objects.all()
            markets = Product.objects.all()
            if query:
                markets = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
            data["markets"] = markets
            if slug != "all":
                data['markets'] = Product.objects.filter(category__slug=slug)
            if slug == "top":
                data["markets"] = Product.objects.annotate(order_count = Count(F("thread_order"))).order_by("-order_count")[:10]
            return data
