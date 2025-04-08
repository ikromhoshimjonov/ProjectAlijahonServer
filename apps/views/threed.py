import datetime

from django.contrib import messages
from django.db.models import Count, F, Q, Sum
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, TemplateView

from apps.forms import ThreedForm
from apps.models import Thread, Product, Category, Order



class ThreedFormView(FormView):
      template_name = "Market/market.html"
      form_class = ThreedForm
      success_url = reverse_lazy("threed-list")

      def get_context_data(self, **kwargs):
          data = super().get_context_data(**kwargs)
          data["markets"] = Product.objects.all()
          data["categories"] = Category.objects.all()
          return data

      def form_valid(self, form):
         thread = form.save(commit=False)
         thread.user = self.request.user
         thread.save()
         return super().form_valid(form)

      def form_invalid(self, form):
          for error in form.errors.values():
              messages.error(self.request,error)
          return super().form_invalid(form)
              


class ThreedListView(ListView):
    queryset = Thread.objects.all()
    template_name = "Market/market-list.html"
    context_object_name = "threeds"

    def get_context_data(self,  **kwargs):
        data =  super().get_context_data(**kwargs)
        data["threeds"] = data.get("threeds").filter(user_id=self.request.user.id).order_by("-created_at")
        return data



class ThreedProductDetailView(DetailView):
    queryset = Thread.objects.all()
    template_name = "order/product-order.html"
    context_object_name = "threed"

    def get_context_data(self, **kwargs):
        data =  super().get_context_data(**kwargs)
        data["product"] = data.get("threed").product
        data.get("threed").visit_count += 1
        data.get("threed").save()
        return data



class ThreadStaticTemplateView(TemplateView):
    template_name ="Market/threed-static.html"

    def get_context_data(self, **kwargs):
        map_range_date = {
            "today": (
                datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                datetime.datetime.now(),
            ),
            "last-day": (
                (datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0,
                                                                               microsecond=0),
                (datetime.datetime.now() - datetime.timedelta(days=1)).replace(hour=23, minute=59, second=59,
                                                                               microsecond=999999),
            ),
            "wekly": (
                datetime.datetime.now() - datetime.timedelta(weeks=1),
                datetime.datetime.now(),
            ),
            "monthly": (
                datetime.datetime.now() - datetime.timedelta(days=30),
                datetime.datetime.now(),
            ),
        }
        period = self.request.GET.get("period")
        date = map_range_date.get(period)
        data =  super().get_context_data(**kwargs)
        statistic = Thread.objects.filter(user_id=self.request.user.id)
        if date:
            statistic =   statistic.filter(user_id=self.request.user.id, created_at__range=date)
        statistic = statistic.annotate(
        new_count=Count("orders", filter=Q(orders__status  = Order.StatusType.NEW)),
        ready_to_order_count=Count("orders", filter=Q(orders__status = Order.StatusType.READY_TO_ORDER)),
        delivering_count=Count("orders", filter=Q(orders__status  = Order.StatusType.DELIVERING)),
        delivered_count=Count("orders", filter=Q(orders__status = Order.StatusType.DELIVERED)),
        not_pick_up_count=Count("orders", filter=Q(orders__status = Order.StatusType.NOT_PICK_UP)),
        archived_count=Count("orders", filter=Q(orders__status = Order.StatusType.ARCHIVED)),


        ).only("name","product__name","visit_count")
        tmp = statistic.aggregate(
            all_visit_count = Sum("visit_count"),
            all_new_count=Sum("new_count"),
            all_ready_to_order_count=Sum("ready_to_order_count"),
            all_delivering_count=Sum("delivering_count"),
            all_delivered_count=Sum("delivered_count"),
            all_not_pick_up_count=Sum("not_pick_up_count"),
            all_archived_count=Sum("archived_count"),

        )
        data["statistic"] = statistic
        data["product_count"] = statistic.count()

        data.update(tmp)
        return data


