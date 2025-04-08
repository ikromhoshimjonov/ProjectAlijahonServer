from django.urls import path
from django.conf.urls.static import static

from apps.views import PaymentFormView
from root.settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
          path("payment/",PaymentFormView.as_view(),name="payment")
              ] + static(MEDIA_URL,document_root = MEDIA_ROOT)