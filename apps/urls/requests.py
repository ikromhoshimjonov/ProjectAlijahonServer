from django.urls import path
from django.conf.urls.static import static
from apps.views.requests import RequestTemplateView, DiagramTemplateView
from root.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
   path("request/",RequestTemplateView.as_view(),name="request_data"),
   path("diogram/",DiagramTemplateView.as_view(),name="diagram")
              ] + static(MEDIA_URL,document_root = MEDIA_ROOT)
