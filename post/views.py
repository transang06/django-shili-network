from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json
# Create your views here.
from django.views import View

from home.models import Database
from post.models import Comment, Post


class ShowPost(View):
    def get(self, request, post_id):
        if request.user.is_authenticated:
            return render(request, 'post/return_post.html', {'post_id': post_id})
        else:
            return redirect('home:home')

    def post(self, request, post_id):
        if request.user.is_authenticated:
            sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE post =" + str(
                post_id)
            Top = Post.objects.raw(sql)
            thislist = []
            for i in Top:
                thisdict = {}
                thisdict["post_id"] = i.post
                thisdict["username"] = i.username
                thisdict["full_name"] = i.first_name + i.last_name
                thisdict["feeling"] = i.feeling
                thisdict["created_at"] = i.created_at
                thisdict["public"] = i.public
                thisdict["content"] = i.content
                thisdict["hashtag"] = i.hashtag
                thisdict["user_id"] = i.user_id
                thisdict["avatar"] = str(i.avatar)
                thisdict["photo"] = str(i.photo)
                thislist.append(thisdict)
            return JsonResponse({'result': thislist})
        else:
            return redirect('home:login')


class TopHashtagPost(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'post/return_post.html', {'top3post': 1})
        else:
            return redirect('home:home')

    def post(self, request):
        if request.user.is_authenticated:
            sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id JOIN( SELECT hashtag,count(hashtag) AS SoLuot FROM post_post GROUP BY hashtag  ORDER BY SoLuot DESC LIMIT 3) c ON a.hashtag =c.hashtag"
            Top = Post.objects.raw(sql)
            thislist = []
            for i in Top:
                thisdict = {}
                thisdict["post_id"] = i.post
                thisdict["username"] = i.username
                thisdict["full_name"] = i.first_name + i.last_name
                thisdict["feeling"] = i.feeling
                thisdict["created_at"] = i.created_at
                thisdict["public"] = i.public
                thisdict["content"] = i.content
                thisdict["hashtag"] = i.hashtag
                thisdict["user_id"] = i.user_id
                thisdict["avatar"] = str(i.avatar)
                thisdict["photo"] = str(i.photo)
                thislist.append(thisdict)
            return JsonResponse({'result': thislist})
        else:
            return redirect('home:login')




class SetPost(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'post/set_post.html')
        else:
            return redirect('home:home')

    def post(self, request):
        if request.user.is_authenticated:
            content = request.POST.get('content')
            hashtag = request.POST.get('hashtag').upper().replace(" ", "")
            feeling = request.POST.get('feeling')
            tag_friends = request.POST.get('tag_friends')
            public = request.POST.get('public')
            photo = ''
            try:
                photo = request.FILES['photo']
            except:
                pass
            new_post = Post()
            new_post.content = content
            new_post.photo = photo
            new_post.hashtag = hashtag
            new_post.feeling = feeling
            new_post.tag_friends = tag_friends
            new_post.public = public
            new_post.user = request.user
            new_post.save()
            sql = 'SELECT post From user_myuser a JOIN post_post b on a.id =  b.user_id ORDER BY created_at DESC LIMIT 1'
            post_id = Post.objects.raw(sql)[0].post
            return redirect('post:ShowPost', post_id)


class EditPost(View):
    def get(self, request, post_id):
        if request.user.is_authenticated:
            return render(request, 'post/edit_post.html', {'post_id': post_id})
        else:
            return redirect('home:home')

    def post(self, request, post_id):
        if request.user.is_authenticated:
            get_post = Post.objects.get(post=post_id)
            if request.method == 'POST':
                try:
                    photo = request.FILES['photo']
                    get_post.photo = photo
                except:
                    pass
                get_post.content = request.POST.get('content')
                get_post.hashtag = request.POST.get('hashtag').upper()
                get_post.feeling = request.POST.get('feeling')
                get_post.public = request.POST.get('public')

                get_post.save()
            return redirect('post:ShowPost', post_id)
        else:
            return redirect('home:home')


class DeletePost(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            get_post = Post.objects.get(post=data['post_id'])
            if get_post.user_id == request.user.id:
                get_post.delete()
            return HttpResponse('Xóa Thành công')

        else:
            return HttpResponse('Tài khoản chưa đăng nhập')



class ApiHashtag(View):
    def get(self, request, hashtag):
        if request.user.is_authenticated:
            return render(request, 'post/return_post.html', {'hashtag_post': hashtag})
        else:
            return redirect('home:home')

    def post(self, request, hashtag):
        if request.user.is_authenticated:
            sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.hashtag like '%" + str(
                hashtag).upper() + "%'"
            Top = Post.objects.raw(sql)
            thislist = []
            for i in Top:
                thisdict = {}
                thisdict["post_id"] = i.post
                thisdict["username"] = i.username
                thisdict["full_name"] = i.first_name + i.last_name
                thisdict["feeling"] = i.feeling
                thisdict["created_at"] = i.created_at
                thisdict["public"] = i.public
                thisdict["content"] = i.content
                thisdict["hashtag"] = i.hashtag
                thisdict["user_id"] = i.user_id
                thisdict["avatar"] = str(i.avatar)
                thisdict["photo"] = str(i.photo)
                thislist.append(thisdict)
            return JsonResponse({'result': thislist})
        else:
            return redirect('home:login')


class ApiTopHashtag(View):
    def post(self, request):
        if request.user.is_authenticated:
            sql = "SELECT  hashtag,count(hashtag) AS soluot FROM post_post GROUP BY hashtag  ORDER BY SoLuot DESC"
            Top = Post.objects.raw(sql)[0:3]
            thislist = []
            for i in Top:
                thisdict = {}
                thisdict["hashtag"] = i.hashtag
                thisdict["soluot"] = i.soluot
                thislist.append(thisdict)
            return JsonResponse({'result': thislist})
        else:
            return redirect('home:login')


class Comment_post(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        try:
            if data['content_input'] != '':
                new_cm = Comment()
                new_cm.content = data['content_input']
                new_cm.user_id = request.user.id
                new_cm.post_id = data['post_id']
                new_cm.save()

        except:
            pass

        sql = "SELECT * FROM post_comment a JOIN user_myuser b ON  a.user_id = b.id WHERE a.post_id =" + str(
            data['post_id'])
        Top = Post.objects.raw(sql)
        thislist = []
        for i in Top:
            thisdict = {}
            thisdict["content"] = i.content
            thisdict["user_id"] = i.user_id
            thisdict["username"] = i.username
            thisdict["comment_id"] = i.comment
            thisdict["fullname"] = i.first_name + i.last_name
            thisdict["created_at"] = i.created_at
            thislist.append(thisdict)
        return JsonResponse({'result': thislist})


class Delete_comment(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            get_comment = Comment.objects.get(comment=data['comment_id'])
            if get_comment.user == request.user:
                get_comment.delete()
            sql = "SELECT * FROM post_comment a JOIN user_myuser b ON  a.user_id = b.id WHERE a.post_id =" + str(
                data['post_id'])
            Top = Post.objects.raw(sql)
            thislist = []
            for i in Top:
                thisdict = {}
                thisdict["content"] = i.content
                thisdict["user_id"] = i.user_id
                thisdict["comment_id"] = i.comment
                thisdict["fullname"] = i.first_name + i.last_name
                thisdict["created_at"] = i.created_at
                thislist.append(thisdict)
            return JsonResponse({'result': thislist})
        else:
            return HttpResponse('Tài khoản chưa đăng nhập')


# class Search(View):
#     def post(self, request):
#         if request.user.is_authenticated:
#             data = json.loads(request.body.decode('utf-8'))
#             sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.hashtag like '%" + data[
#                 'key'].upper() + "%'"
#             Top = Post.objects.raw(sql)
#             thislist = []
#             for i in Top:
#                 thisdict = {}
#                 thisdict["post_id"] = i.post
#                 thisdict["username"] = i.username
#                 thisdict["full_name"] = i.first_name + i.last_name
#                 thisdict["feeling"] = i.feeling
#                 thisdict["created_at"] = i.created_at
#                 thisdict["public"] = i.public
#                 thisdict["content"] = i.content
#                 thisdict["hashtag"] = i.hashtag
#                 thisdict["user_id"] = i.user_id
#                 thisdict["avatar"] = str(i.avatar)
#                 thisdict["photo"] = str(i.photo)
#                 thislist.append(thisdict)
#             return JsonResponse({'result': thislist})
#         else:
#             return redirect('home:login')
