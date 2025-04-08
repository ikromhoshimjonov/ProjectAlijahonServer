from django.urls import path
from django.conf.urls.static import static

from apps.views import AuthFormView, HomeListView, ProductListView, UserLogoutView, ProfileListView, RegionFormView, \
    district_list_view, ChangePasswordFormView, WishlistView, ProductOrderDetailView, LikeProductListView,  ProductOrdersListView, MarketListView
from apps.views.konkurs import CompetitionListView
from root.settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path("konkurs/list", CompetitionListView.as_view(), name="konkurs-list"),
] + static(MEDIA_URL,document_root = MEDIA_ROOT)