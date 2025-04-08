from django.urls import path
from django.conf.urls.static import static

from apps.models import Wishlist
from apps.views import AuthFormView, HomeListView, ProductListView, UserLogoutView, ProfileListView, RegionFormView, \
    district_list_view, ChangePasswordFormView, WishlistView, ProductOrderDetailView, LikeProductListView, \
    ProductOrdersListView
from root.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('', HomeListView.as_view(), name="home"),
    path('profile', ProfileListView.as_view(), name="profile"),
    path('district', district_list_view, name="district"),
    path("region",RegionFormView.as_view(),name="region"),
    path("change-password", ChangePasswordFormView.as_view(), name="change-password")] + static(MEDIA_URL,document_root = MEDIA_ROOT)