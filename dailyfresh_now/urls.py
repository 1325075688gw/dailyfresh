from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^user/', include('apps.user.urls', namespace='user')),
    url(r'^cart/', include('apps.cart.urls', namespace='cart')),
    url(r'^order/', include('apps.order.urls', namespace='order')),
    url(r'^', include('apps.goods.urls', namespace='goods')),
]

