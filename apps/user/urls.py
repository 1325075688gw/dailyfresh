from django.conf.urls import url
from apps.user import views
from apps.user.views import Register,ActiveEmail,Login,UserInfo,UserAddr,UserOrder,Logout
from django.contrib.auth.decorators import login_required

urlpatterns = [
    #url(r'^register$', views.register, name='register'), # 注册页面,注册业务逻辑处理
    #url(r'^register_handle$', views.register_handle, name='register_handle') # 注册业务逻辑处理
    url(r'^register$', Register.as_view(), name='register'), # 用户注册
    url(r'^active/(?P<token>.*)$', ActiveEmail.as_view(), name='active'), # 邮箱激活
    url(r'^login$', Login.as_view(), name='login'), # 用户登录
    url(r'^logout$', Logout.as_view(), name='logout'), # 注销用户,清除session
    url(r'^addr$', login_required(UserAddr.as_view()), name='addr'),
    url(r'^order$', UserOrder.as_view(), name='order'),
    url(r'^$', UserInfo.as_view(), name='info'),
]

