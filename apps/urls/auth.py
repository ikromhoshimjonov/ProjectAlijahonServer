from django.urls import path
from django.conf.urls.static import static

from apps.models import Wishlist
from apps.views import AuthFormView, HomeListView, ProductListView, UserLogoutView, ProfileListView, RegionFormView, \
    district_list_view, ChangePasswordFormView, WishlistView, ProductOrderDetailView, LikeProductListView, \
     ProductOrdersListView
from root.settings import MEDIA_URL, MEDIA_ROOT



urlpatterns = [
    path('auth',AuthFormView.as_view(),name="auth"),
    path('product/<str:slug>',ProductListView.as_view(),name="product"),
    path('logout', UserLogoutView.as_view(), name="logout"),
              ] + static(MEDIA_URL,document_root = MEDIA_ROOT)