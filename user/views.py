import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from home.models import Database
from post.models import Post
from user.models import Follower, MyUser


class Profile(View):
    def get(self, request, user_username):
        if request.user.is_authenticated:
            if request.user.username == user_username:
                return redirect('user:profile_main')
            return render(request, 'user/profile.html', {'username': user_username})
        else:
            return redirect('home:home')


class ProfileMain(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'user/profile.html', {'username': request.user.username})
        else:
            return redirect('home:home')


class ApiGetProfile(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            sql_profile = "SELECT * FROM user_myuser a WHERE a.username ='" + data['username'] + "'"
            get_profile = MyUser.objects.raw(sql_profile)
            profile = []
            for i in get_profile:
                thisdict = {}
                thisdict["username"] = i.username
                thisdict["user_id"] = i.id
                thisdict["email"] = i.email
                thisdict["avatar"] = str(i.avatar)
                thisdict["cover_image"] = str(i.cover_image)
                thisdict["first_name"] = i.first_name
                thisdict["last_name"] = i.last_name
                thisdict["full_name"] = i.first_name + " " + i.last_name
                thisdict["birthday"] = i.birthday
                thisdict["gender"] = i.gender
                thisdict["address"] = i.address
                thisdict["intro"] = i.intro
                thisdict["date_joined"] = i.date_joined
                thisdict["is_superuser"] = i.is_superuser
                profile.append(thisdict)

            sql_profile_posts = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE b.username ='" + \
                                data['username'] + "' ORDER BY created_at DESC"
            get_profile_posts = Post.objects.raw(sql_profile_posts)
            profile_posts = []
            for i in get_profile_posts:
                thisdict = {}
                thisdict["post_id"] = i.post
                thisdict["username"] = i.username
                thisdict["full_name"] = i.first_name + " " + i.last_name
                thisdict["feeling"] = i.feeling
                thisdict["created_at"] = i.created_at
                thisdict["public"] = i.public
                thisdict["content"] = i.content
                thisdict["hashtag"] = i.hashtag
                thisdict["user_id"] = i.user_id
                thisdict["avatar"] = str(i.avatar)
                thisdict["photo"] = str(i.photo)
                profile_posts.append(thisdict)

            user_id_sql = "SELECT id FROM user_myuser WHERE username ='" + data['username'] + "'"
            user_id = MyUser.objects.raw(user_id_sql)[0].id
            sql_followres = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE main_user_id = " + str(
                user_id) + ") b ON a.id = b.followres_id WHERE  a.id !='" + str(user_id) + "'"
            dangtheodoi = MyUser.objects.raw(sql_followres)
            print(dangtheodoi)
            profile_dangtheodoi = []
            for i in dangtheodoi:
                thisdict = {}
                thisdict["avatar"] = str(i.avatar)
                thisdict["username"] = i.username
                thisdict["full_name"] = i.first_name + " " + i.last_name
                thisdict["id"] = i.id
                profile_dangtheodoi.append(thisdict)
                print(profile_dangtheodoi)

            sql_duoctheodoi = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE followres_id ='" + str(
                user_id) + "') b ON a.id = b.main_user_id WHERE  a.id !='" + str(user_id) + "'"
            duoctheodoi = MyUser.objects.raw(sql_duoctheodoi)
            print(duoctheodoi)

            profile_duoctheodoi = []
            for i in duoctheodoi:
                thisdict = {}
                thisdict["avatar"] = str(i.avatar)
                thisdict["username"] = i.username
                thisdict["full_name"] = i.first_name + " " + i.last_name
                thisdict["id"] = i.id
                profile_duoctheodoi.append(thisdict)
                print(profile_duoctheodoi)
            return JsonResponse(
                {'profile': profile, 'profile_posts': profile_posts, 'dangtheodoi': profile_dangtheodoi,
                 'duoctheodoi': profile_duoctheodoi})
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
            return HttpResponse("Thay Đổi Thành Công")
        else:
            return redirect('home:login')


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
            id_room = database.id_follow(request.user.id, data['id'])
            if not id_room:
                fl = Follower()
                fl.main_user = request.user
                fl.followres = MyUser.objects.get(id=data['id'])
                fl.save()
                return HttpResponse('Follow thành công, hãy tiếp tục theo dõi những người khác')
            else:
                return HttpResponse('ban da theo doi nguoi nay')

        else:
            return redirect('home:home')


class AllUser(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'user/all_user.html', {'all_user': '1'})
        else:
            return redirect('home:home')

    def post(self, request):
        if request.user.is_authenticated:
            sql = "SELECT * FROM user_myuser WHERE id !=" + str(
                request.user.id) + " AND id NOT IN (SELECT followres_id FROM user_follower c WHERE c.main_user_id = " \
                  + str(request.user.id) + " ) Order by date_joined DESC"
            Top = Post.objects.raw(sql)
            thislist = []
            for i in Top:
                thisdict = {}
                thisdict["id"] = i.id
                thisdict["username"] = i.username
                thisdict["avatar"] = str(i.avatar)
                thisdict["full_name"] = i.first_name + " " + i.last_name
                thislist.append(thisdict)
            return JsonResponse({'result': thislist})
        else:
            return redirect('home:home')


class TopFriend(View):
    def post(self, request):
        if request.user.is_authenticated:
            sql = "SELECT * FROM user_myuser WHERE id !=" + str(
                request.user.id) + " AND id NOT IN (SELECT followres_id FROM user_follower c WHERE c.main_user_id = " \
                  + str(request.user.id) + " ) Order by date_joined DESC"
            Top = Post.objects.raw(sql)
            thislist = []
            for i in Top:
                thisdict = {}
                thisdict["id"] = i.id
                thisdict["username"] = i.username
                thisdict["avatar"] = str(i.avatar)
                thisdict["full_name"] = i.first_name + " " + i.last_name
                thislist.append(thisdict)
            return JsonResponse({'result': thislist})
        else:
            return redirect('home:home')


class ApiYourFriend(View):
    def post(self, request):
        if request.user.is_authenticated:
            sql = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE main_user_id = " + str(
                request.user.id) + ") b ON a.id = b.followres_id"
            Top = Post.objects.raw(sql)
            thislist = []
            for i in Top:
                thisdict = {}
                thisdict["id"] = i.id
                thisdict["avatar"] = str(i.avatar)
                thisdict["full_name"] = i.first_name + " " + i.last_name
                thislist.append(thisdict)
            return JsonResponse({'result': thislist})
        else:
            return redirect('home:home')
