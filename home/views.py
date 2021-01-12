from django.contrib.auth import authenticate, login, logout

from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
# Create your views here.
from django.views import View

from home.models import ShiliEmail, MaHoaOneTimePad, Database

from user.models import MyUser


class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            kt = database.get_watching(request.user.username)
            if kt:
                return render(request, 'home/home.html', {'page': 'Trang chủ Shili'})
            else:
                return render(request, 'user/all_user.html', {'page': 'all_user'})

        else:
            return render(request, 'home/index.html')


class Login_user(View):
    def post(self, request):
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            username = data['username']
            password = data['password']
            try:
                user = authenticate(username=MyUser.objects.get(email=username), password=password)
            except:
                user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('success')
                else:
                    return HttpResponse(
                        "Tài khoản này chưa được kích hoạt. Hãy kích hoạt tài khoản trước khi đăng nhập")
            else:
                return HttpResponse('Thông tin đăng nhập không chính xác. Vui lòng kiểm tra lại')


def logout_user(request):
    try:
        logout(request)
    except:
        pass
    return redirect('home:home')


class Register_user(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        if not MyUser.objects.filter(email=email).exists():
            new_user = MyUser()
            new_user.first_name = data['firstname']
            new_user.last_name = data['lastname']
            new_user.username = data['username']
            new_user.email = data['email']
            new_user.set_password(data['password1'])
            new_user.birthday = data['birthday']
            new_user.gender = data['gender']
            new_user.is_active = 0
            new_user.save()
            new_user = MyUser.objects.filter(username=data['username'])
            if new_user:
                mail_content = "Hello"
                mail_title = "Welcome to Shili!"
                one_time_pad = MaHoaOneTimePad()
                result = one_time_pad.ma_hoa(email)
                domain = request.scheme + '://' + request.META['HTTP_HOST']
                url = domain + '/xacthuc/' + result[0] + '/' + result[1]
                content = "Nhấp vào đây để Xác thực tài khoản của bạn"
                theme = ShiliEmail()
                msg_html = theme.form_mail(url, content, email)
                send_mail(mail_title, mail_content, "PLC", [email], html_message=msg_html, fail_silently=False)
                return HttpResponse(
                    'Đăng kí thành công tài khoản. Kiểm tra email để nhận liên kết kích hoạt tài khoản')
            else:
                return HttpResponse('Có lỗi xảy ra! Vui lòng thử lại')


class Send_pass(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        if MyUser.objects.filter(email=email).exists():
            one_time_pad = MaHoaOneTimePad()
            result = one_time_pad.ma_hoa(email)
            mail_content = "Hello"
            mail_title = "Shili! Đặt lại mật khẩu"
            domain = request.scheme + '://' + request.META['HTTP_HOST']
            url = domain + '/resetpassword/' + result[0] + '/' + result[1]
            content = "Nhấp  vào đây để đặt lại mật khẩu  của bạn"
            theme = ShiliEmail()
            msg_html = theme.form_mail(url, content, email)
            send_mail(mail_title, mail_content, "PLC", [email], html_message=msg_html, fail_silently=False)
            return HttpResponse('Kiểm tra email để lấy liên kết đến trang thay đổi mật khẩu')
        return HttpResponse('Email này không tồn tại trong hệ thống,vui lòng kiểm tra lại')


class Xac_thuc(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        if MyUser.objects.filter(email=email).exists():
            one_time_pad = MaHoaOneTimePad()
            result = one_time_pad.ma_hoa(email)
            mail_content = "Hello"
            mail_title = "Shili! Xác thực tài khoản"
            domain = request.scheme + '://' + request.META['HTTP_HOST']
            url = domain + '/xacthuc/' + result[0] + '/' + result[1]
            content = "Nhấp  vào đây để xác thực tài khoản"
            theme = ShiliEmail()
            msg_html = theme.form_mail(url, content, email)
            send_mail(mail_title, mail_content, "PLC", [email], html_message=msg_html, fail_silently=False)
            return HttpResponse('Kiểm tra email để lấy liên kết đến trang xác thực tài khoản')
        return HttpResponse('Email này không tồn tại trong hệ thống, vui lòng kiểm tra lại')


class Xacthuc(View):
    def get(self, request, key, ban_ma):
        one_time_pad = MaHoaOneTimePad()
        email = one_time_pad.giai_ma(key, ban_ma)
        context = {
            'email': email,
            'key': key,
            'ban_ma': ban_ma,
        }
        user = MyUser.objects.get(email=email)
        user.is_active = 1
        user.save()
        return render(request, 'mail/xacthuc.html', context)


class ResetPassword(View):
    def get(self, request, key, ban_ma):
        one_time_pad = MaHoaOneTimePad()
        email = one_time_pad.giai_ma(key, ban_ma)
        context = {
            'email': email,
            'key': key,
            'ban_ma': ban_ma,
        }
        return render(request, 'mail/reset_password.html', context)

    def post(self, request, key, ban_ma):
        one_time_pad = MaHoaOneTimePad()
        email = one_time_pad.giai_ma(key, ban_ma)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password2 == password1:
            edit_user = MyUser.objects.get(email=email)
            edit_user.set_password(password1)
            edit_user.save()
        return redirect('home:home')


class Check(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        username = data['username']
        email = data['email']
        try:
            MyUser.objects.get(username=username)
            return HttpResponse('Username đã tồn tại trong hệ thống vui lòng thử username mới')
        except:
            pass
        try:
            MyUser.objects.get(email=email)
            return HttpResponse('Địa chỉ email đã tồn tại trong hệ thống, hãy thử email khác')
        except:
            pass
        return HttpResponse('')


class ApiGetContent(View):
    def post(self, request):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            get_post_index = database.json_post(database.get_post_index())
            return JsonResponse({'result': get_post_index})
        else:
            return redirect('home:home')
