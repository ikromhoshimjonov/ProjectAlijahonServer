
from django.urls import path
from django.conf.urls.static import static

from apps.models import Wishlist
from apps.views import AuthFormView, HomeListView, ProductListView, UserLogoutView, ProfileListView, RegionFormView, \
    district_list_view, ChangePasswordFormView, WishlistView, ProductOrderDetailView, LikeProductListView, \
    OrderProductFormView, ProductOrdersListView, MarketListView
from root.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path("wishlist/<int:product_id>/", WishlistView.as_view(), name="wishlist"),
    path("product-order/<str:slug>", ProductOrderDetailView.as_view(), name="product-order"),
    path("like", LikeProductListView.as_view(), name="like"),
    path("check",OrderProductFormView.as_view(),name="check"),
    path("orders", ProductOrdersListView.as_view(), name="orders")
] + static(MEDIA_URL,document_root = MEDIA_ROOT)