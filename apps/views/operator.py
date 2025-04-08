

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, FormView

from apps.forms import UserDataForm, DeliverDataForm
from apps.models import Order, Category, Region


class OperatorListView(TemplateView):
    template_name = "operator/operator-page.html"

    def post(self,request,*args,**kwargs):
        context = self.get_context_data()
        return render(request,"operator/operator-page.html",context=context)


    def get_context_data(self, **kwargs):
        status = self.request.GET.get("status")
        data = super().get_context_data(**kwargs)
        category_id = self.request.POST.get("category_id")
        district_id = self.request.POST.get("district_id")
        data["categories"] = Category.objects.all()
        data["regions"] = Region.objects.all()
        data["status"] = Order.StatusType
        op_id = self.request.user.id
        orders = Order.objects.filter(status=Order.StatusType.NEW)
        if status=="new":
            orders = Order.objects.filter(status=status)
        if status and status!="new":
            orders = Order.objects.filter(Q(status=status) & Q(operator=op_id))
        if category_id:
            orders = Order.objects.filter(product__category__id=category_id)
        if district_id:
            orders = Order.objects.filter(district__id = district_id)
        data["orders"] = orders
        return data





class OrderChangeDetailView(DetailView):
    queryset = Order.objects.all()
    template_name = "operator/order-change (1).html"
    context_object_name = "order"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data["regions"] = Region.objects.all()
        return data


class ChangeUserFormView(FormView):
    form_class = UserDataForm
    success_url = reverse_lazy("operator")
    template_name = "operator/order-change (1).html"



    def form_valid(self, form):
        order_pk = self.kwargs.get("pk")
        data = form.cleaned_data
        op_pk = Order.objects.filter(id=order_pk).first().operator
        if self.request.POST.get("status") != "new":
            form.cleaned_data["operator"] = self.request.user.id
        if self.request.POST.get("status") == "new" and op_pk:
            form.cleaned_data["operator"] = None
        Order.objects.filter(id=order_pk).update(**data)
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request,error)
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        order_pk = self.kwargs.get("pk")
        data =  super().get_context_data(**kwargs)
        data["order"] = Order.objects.filter(pk=order_pk).first()
        return data



    #------------------deliver ------------------------------------------

class DeliverListView(TemplateView):
    template_name = "operator/deliver-page.html"

    def post(self,request,*args,**kwargs):
        context = self.get_context_data()
        return render(request,"operator/deliver-page.html",context=context)


    def get_context_data(self, **kwargs):
        status = self.request.GET.get("status")
        data = super().get_context_data(**kwargs)
        category_id = self.request.POST.get("category_id")
        district_id = self.request.POST.get("district_id")
        data["categories"] = Category.objects.all()
        data["regions"] = Region.objects.all()
        data["status"] = Order.StatusType
        dl_id = self.request.user.id
        orders = Order.objects.filter(status=Order.StatusType.NEW)
        if status=="ready_to_order":
            orders = Order.objects.filter(status=status)
        if status and status!="ready_to_order":
            orders = Order.objects.filter(Q(status=status) & Q(deliver=dl_id))

        if category_id:
            orders = Order.objects.filter(product__category__id=category_id)
        if district_id:
            orders = Order.objects.filter(district__id = district_id)
        data["orders"] = orders
        return data

class DeliverOrderChangeDetailView(DetailView):
        queryset = Order.objects.all()
        template_name = "operator/deliver_order-change.html"
        context_object_name = "order"
        pk_url_kwarg = "pk"


class DeliverChangeUserFormView(FormView):
    form_class = DeliverDataForm
    success_url = reverse_lazy("deliver")
    template_name = "operator/deliver_order-change.html"

    def form_valid(self, form):
        deliv_pk = self.kwargs.get("pk")
        data = form.cleaned_data
        op_pk = Order.objects.filter(id=deliv_pk).first().deliver
        if self.request.POST.get("status") != "ready_to_order":
            form.cleaned_data["deliver"] = self.request.user.id
        if self.request.POST.get("status") == "ready_to_order" and op_pk:
            form.cleaned_data["deliver"] = None

        Order.objects.filter(id=deliv_pk).update(**data)
        return super().form_valid(form)






















