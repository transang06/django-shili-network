import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from home.models import Database
from user.models import Follower, MyUser


class Profile(View):
    def get(self, request, user_username):
        if request.user.is_authenticated:
            if request.user.username == user_username:
                return redirect('user:profile_main')
            return render(request, 'user/profile.html', {'username': user_username, 'page': 'profile'})
        else:
            return redirect('home:home')


class ProfileMain(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'user/profile.html', {'username': request.user.username, 'page': 'profile'})
        else:
            return redirect('home:home')


class ApiGetProfile(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            database = Database(request.user.id)
            profile = database.get_profile(data['username'])
            profile_posts = database.get_profile_posts(data['username'], request.user.username)
            profile_watching = database.get_watching(data['username'])
            profile_followed = database.get_followed(data['username'])
            return JsonResponse(
                {'profile': profile, 'profile_posts': profile_posts, 'dangtheodoi': profile_watching,
                 'duoctheodoi': profile_followed})
        else:
            return redirect('home:home')


class ApiEditProfile(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            edit_user = MyUser.objects.get(id=request.user.id)
            if data['first_name'] != '' and data['last_name'] != '':
                edit_user.first_name = data['first_name']
                edit_user.last_name = data['last_name']
            if data['address'] != '':
                edit_user.address = data['address']
            if data['email'] != '':
                edit_user.email = data['email']
            if data['gender'] != edit_user.gender:
                edit_user.gender = data['gender']
            if data['birthday'] != edit_user.birthday:
                edit_user.birthday = data['birthday']
            edit_user.intro = data['intro']
            edit_user.save()
            return HttpResponse("Bạn đã thay đổi thông tin thành công.")
        else:
            return HttpResponse('Phiên đăng nhập của bạn đã hết hạn vui lòng đăng nhập lại')


class Edit_av_bg(View):
    def post(self, request):
        if request.user.is_authenticated:
            edit_user = MyUser.objects.get(id=request.user.id)
            try:
                edit_user.avatar = request.FILES['new_avatar']
                edit_user.save()
            except:
                pass
            try:
                edit_user.cover_image = request.FILES['new_cover_image']
                edit_user.save()
            except:
                pass
            return redirect('user:profile_main')
        else:
            return redirect('home:login')


class Add_follow(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            database = Database(request.user.id)
            id_follower = database.check_id_follow(request.user.id, data['id'])
            if not id_follower:
                fl = Follower()
                fl.main_user = request.user
                fl.followres = MyUser.objects.get(id=data['id'])
                fl.save()
                return HttpResponse('Follow thành công, hãy tiếp tục theo dõi những người khác')
            else:
                fl = Follower.objects.get(f_id=id_follower)
                fl.delete()
                return HttpResponse('Hủy follow thành công, hãy tiếp tục theo dõi những người khác')
        else:
            return HttpResponse('Phiên đăng nhập đã hết hạn.')


class AllUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'user/all_user.html', {'page': 'all_user'})
        else:
            return redirect('home:home')

    def post(self, request):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            all_user = database.get_all_user()
            return JsonResponse({'result': all_user})
        else:
            return redirect('home:home')


class ApiYourFriend(View):
    def post(self, request):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            profile_watching = database.get_watching(request.user.username)
            return JsonResponse({'result': profile_watching})
        else:
            return JsonResponse({'result': []})
