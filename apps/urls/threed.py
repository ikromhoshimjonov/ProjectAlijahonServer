
from django.urls import path
from django.conf.urls.static import static

from apps.views import ThreedListView
from apps.views.threed import ThreedFormView, ThreedProductDetailView,ThreadStaticTemplateView
from root.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path("thred/form", ThreedFormView.as_view(), name="threed-form"),
    path("thred/list", ThreedListView.as_view(), name="threed-list"),
    path("threed/<int:pk>", ThreedProductDetailView.as_view(), name="threed-product"),
    path("threed/static", ThreadStaticTemplateView.as_view(), name="threed-static")

              ] + static(MEDIA_URL,document_root = MEDIA_ROOT)