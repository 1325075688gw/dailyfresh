from django.shortcuts import render, redirect,HttpResponse
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout

from utils.mixin import LoginRequiredMixin
from apps.user import models
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from celery_tasks.tasks import send_email
import re

# Create your views here.

# /user/register
def register(request):
    '''注册'''
    if request.method == 'GET':
        # 显示注册页面
        return render(request, 'register.html')
    else:
        # 进行用户注册处理
        # 接受数据
        username = request.POST.get('user_name', None)
        password = request.POST.get('pwd', None)
        email = request.POST.get('email', None)
        allow = request.POST.get('allow', None)

        # 进行数据校验
        if not all([username, password, email, allow]):
            return render(request, 'register.html', {'errmsg': '用户信息填写不完整'})
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        if not allow:
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 进行业务逻辑处理
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已被注册'})
        user = models.User.objects.create_user(username=username, email=email, password=password)
        user.is_active = 0
        user.save()

        # 返回应答消息
        return redirect(reverse('goods:index'))

# /user/register_handel
def register_handle(request):
    '''进行用户注册处理'''
    # 接受数据
    username = request.POST.get('user_name', None)
    password = request.POST.get('pwd', None)
    email = request.POST.get('email', None)
    allow = request.POST.get('allow', None)

    # 进行数据校验
    if not all([username, password, email, allow]):
        return render(request, 'register.html', {'errmsg' : '用户信息填写不完整'})
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg' : '邮箱格式不正确'})
    if not allow:
        return render(request, 'register.html', {'errmsg': '请同意协议'})

    # 进行业务逻辑处理
    try:
        user = models.User.objects.get(username=username)
    except models.User.DoesNotExist:
        user = None
    if user:
        return render(request, 'register.html', {'errmsg': '用户名已被注册'})
    user = models.User.objects.create_user(username=username, email=email, password=password)
    user.is_active = 0
    user.save()

    # 返回应答消息
    return redirect(reverse('goods:index'))

# /user/register
class Register(View):
    def get(self, request):
        # 显示注册页面
        return render(request, 'register.html')
    def post(self, request):
        # 进行用户注册处理
        # 接受数据
        username = request.POST.get('user_name', None)
        password = request.POST.get('pwd', None)
        email = request.POST.get('email', None)
        allow = request.POST.get('allow', None)

        # 进行数据校验
        if not all([username, password, email, allow]):
            return render(request, 'register.html', {'errmsg': '用户信息填写不完整'})
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})
        if not allow:
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 进行业务逻辑处理
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户名已被注册'})
        user = models.User.objects.create_user(username=username, email=email, password=password)
        user.is_active = 0
        user.save()
        # 发送邮件激活
        serializer = Serializer(settings.SECRET_KEY, 3600) # 一个小时过期时间
        info = {'id':user.id}
        token = serializer.dumps(info) # bytes
        token = token.decode()
        subject = '天天生鲜'
        message = ''
        html_message = '<h1>{0},欢迎您注册成为天天生鲜用户!<h1/><br/>请点击以下链接激活用户<a href="http:127.0.0.1:8000/user/active/{1}">http:127.0.0.1:8000/user/active/{1}<a/>'.format(username,token)
        receive_list = [settings.EMAIL_HOST_USER]
        sender = settings.EMAIL_FROM
        # send_mail(subject=subject, message=message, from_email=sender, recipient_list=receive_list,html_message=html_message )
        # 用celery发送异步右键
        # send_email.delay(receive_list, username, token)
        # send_email.apply_async((receive_list,username,token))
        # return redirect(reverse('user:active_email', kwargs={'token':token}))


        # 返回应答消息
        return redirect(reverse('user:login'))

class ActiveEmail(View):
    '''邮箱激活'''
    def get(self, request, token):
        # 接受数据,业务处理
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            id = info['id']
            # 修改用户邮箱状态
            user = models.User.objects.get(id=id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期!')


class Login(View):
    '''用户登录'''
    def get(self, request):
        '''显示用户登录页面'''
        if 'username' is request.COOKIES:
            username = request.COOKIES.get('username','你好')
            remember = 'checked'
        else:
            username =''
            remember = ''

        return render(request, 'login.html',{'username':username, 'remember':remember})

    def post(self, request):
        '''用户登录业务'''
        # 接受数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        remember = request.POST.get('remember')

        response = render(request, 'login.html', {'errmsg': '用户信息不完整!'})
        if remember == 'on':
            response.set_cookie('username', username, max_age=7 * 24 * 3600)
        else:
            response.delete_cookie('username')

        # 校验数据
        if not all([username, password]):
            return response

        # 业务处理
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user) # 记住用户名
                # 如果直接输入其他页面,会跳转到login页面,然后登陆成功后,跳转回去
                next_url = request.GET.get('next', reverse('goods:index')) # redirect是httpresponse子类
                response = redirect(next_url)

                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response
            else:
                return render(request, 'login.html', {'errmsg':'账户未激活!'})
        else:
            return render(request, 'login.html', {'errmsg': '用户名或者密码错误!'})



class UserInfo(View):
    def get(self, request):
        return render(request, 'user_center_info.html', {'page':'info'})

class UserOrder(View):
    def get(self, request):
        return render(request, 'user_center_order.html', {'page':'order'})

# class UserAddr(View):
# Mixin的作用,当多个视图都需要该功能时候,我们可以定义一个类,然后继承该类
class UserAddr(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user  # 用户登录后,各个视图都会存在user
        try:
            address = models.Address.objects.get(user=user, is_default=True)
        # 注意点:这儿抛异常的类
        except models.Address.DoesNotExist as e:
            address = None
        return render(request, 'user_center_addr.html', {'page': 'addr', 'address': address})

    def post(self, request):
        # 接受数据
        receiver = request.POST.get('receiver')
        phone = request.POST.get('phone')
        zip_code = request.POST.get('zip_code')
        addr = request.POST.get('addr')

        # 校验数据
        if not all([receiver,phone,addr]):
            return render(request, 'user_center_addr.html', {'errmsg':'用户数据不完整!'})

        if not re.match(r'^1[3|4|5|6][0-9]{9}$', phone):
            return render(request, 'user_center_addr.html', {'errmsg': '电话号码格式不正确!'})
        # 业务处理
        user = request.user # 用户登录后,各个视图都会存在user
        try:
            address = models.Address.objects.get(user=user, is_default=True)
        except models.Address.DoesNotExist as e:
            address = None
        if address:
            is_default = False
        else:
            is_default = True
        models.Address.objects.create(user=user,
                                      receiver=receiver,
                                      addr=addr,
                                      zip_code=zip_code,
                                      phone=phone,
                                      is_default=is_default)

        # 返回应答
        return redirect(reverse('user:addr')) # 重定向会以get形式请求

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('user:login'))