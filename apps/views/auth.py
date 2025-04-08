from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, ListView, View, DetailView

from apps.forms import AuthForm, ProfileForm, ChangePasswordForm, OrderProductForm
from apps.models import User, Product, Category, Region, District, Wishlist, Order, DeliverPrice



class AuthFormView(FormView):
    template_name = "base/include.html"
    form_class = AuthForm
    success_url = reverse_lazy("home")


    def form_valid(self, form):
        data = form.cleaned_data
        phone_number = data.get("phone_number")
        password = form.data["password"]

        users = User.objects.filter(phone_number=phone_number)
        if users.exists():
            user = users.first()
            if check_password(password ,user.password):
                login(self.request,user)
            else:
                messages.error(self.request,"Passwordda xatolik mavjud")
                return redirect("auth")
        else:
            obj , _ = User.objects.get_or_create(phone_number=phone_number, password=data.get("password"))
            login(self.request,obj)
        return  super().form_valid(form)



    def form_invalid(self, form):
        for i in form.errors:
            messages.error(self.request,i)
        return super().form_invalid(form)

class HomeListView(ListView):
    queryset = Category.objects.all()
    template_name = "home-page.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["products"] = Product.objects.all()
        if self.request.user.is_authenticated:
            data["liked_products_id"] = Wishlist.objects.filter(user_id=self.request.user).values_list("product_id",flat=True)
        return data

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/product.html"
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        slug = self.kwargs.get("slug")
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        data["session_category"] = Category.objects.filter(slug=slug)
        products = Product.objects.all()
        if self.request.user.is_authenticated:
            data["liked_products_id"] = Wishlist.objects.filter(user_id=self.request.user).values_list("product_id",flat=True)
        # -----search --------
        query = self.request.GET.get("query")
        if query:
            products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        data['products'] = products
        # -----search --------

        if slug != "all":
           data['products'] = Product.objects.filter(category__slug=slug)
        return data

class UserLogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('home')