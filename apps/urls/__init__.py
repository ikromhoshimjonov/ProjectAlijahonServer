from apps.urls.home import urlpatterns as home_url
from apps.urls.auth import urlpatterns as auth_url
from apps.urls.order import urlpatterns as order_url
from apps.urls.market import urlpatterns as  market_url
from apps.urls.threed import urlpatterns as threed_url
from apps.urls.konkurs import urlpatterns as konkurs_url
from apps.urls.operator import urlpatterns as operator_url
from apps.urls.payment import urlpatterns  as payment_url
from apps.urls.requests import urlpatterns as request_url
urlpatterns = [
    *home_url , *auth_url , *order_url, *market_url , *threed_url , *konkurs_url, *operator_url , *payment_url,*request_url
]