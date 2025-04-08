from itertools import product

from django.db.models import F, Q
from django.db.models.aggregates import Count, Sum
from django.views.generic import ListView

from apps.models import DeliverPrice, User, Order


class CompetitionListView(ListView):
    template_name = "Konkurs/competition.html"
    queryset = User.objects.filter(role=User.StatusRole.USER)
    context_object_name = "users"

    def get_queryset(self):
        query = super().get_queryset()
        query = query.annotate(order_sum = Sum("thread__orders__quantity",filter=Q(thread__orders__status=Order.StatusType.CONFIRMED))).only("first_name").order_by("-order_sum")
        return query


    def get_context_data(self,  **kwargs):
        data =  super().get_context_data(**kwargs)
        data["complemented"] = DeliverPrice.objects.all()
        return data







