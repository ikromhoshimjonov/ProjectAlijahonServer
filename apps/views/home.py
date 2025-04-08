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






class ProfileListView(LoginRequiredMixin,ListView):
    queryset = User.objects.all()
    template_name = "profile/profile.html"
    context_object_name = "profile"
    login_url = "auth"

class RegionFormView(FormView):
    template_name = "settings/settings.html"
    form_class = ProfileForm
    success_url = reverse_lazy("region")



    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data



    def post(self ,request ,**kwargs):
        user = request.user.id
        data = request.POST
        tg= data.get("telegram_id")
        if not data.get("district_id")=="Viloyatni tanlang":
            datas = {
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "district_id": data.get("district_id"),
                "address": data.get("address"),
                "telegram_id": tg if data.get("telegram_id") else None,
                "about": data.get("about")

            }
        else:
            datas = {
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name"),
                "district_id": None,
                "address": data.get("address"),
                "telegram_id": tg if data.get("telegram_id") else None,
                "about": data.get("about")

            }



        User.objects.filter(pk=user).update(**datas)
        return redirect("region")

def district_list_view(request):
    region_id = request.GET.get('region_id')
    district = District.objects.filter(region_id=region_id).values('id', 'name')
    return JsonResponse(list(district), safe=False)


class ChangePasswordFormView(FormView):
    form_class = ChangePasswordForm
    template_name ="settings/settings.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        session_password = self.request.user.password
        data = form.cleaned_data.get('old')

        if not check_password(data,session_password):
            messages.error(self.request , "Old password error")

        else:
            form.update(self.request.user)


        return super().form_valid(form)

    def form_invalid(self, form):
        for i in form.errors:
            messages.error(self.request, i)
        return super().form_invalid(form)