from django.urls import path
from django.conf.urls.static import static

from apps.models import Order
from apps.views.operator import OperatorListView,OrderChangeDetailView,ChangeUserFormView,DeliverListView,DeliverOrderChangeDetailView,DeliverChangeUserFormView
from root.settings import MEDIA_URL, MEDIA_ROOT



urlpatterns = [
     path("operator/",OperatorListView.as_view(),name="operator"),
     path("order/change<int:pk>", OrderChangeDetailView.as_view() , name="order-change"),
     path("deliver/change<int:pk>",DeliverOrderChangeDetailView.as_view(),name="deliver-change"),
     path("change/data<int:pk>" , ChangeUserFormView.as_view(),name="user-change"),
     path("deliver/data<int:pk>", DeliverChangeUserFormView.as_view(), name="deliver_data-change"),
     path("deliver/",DeliverListView.as_view(),name="deliver")
              ] + static(MEDIA_URL,document_root = MEDIA_ROOT)
