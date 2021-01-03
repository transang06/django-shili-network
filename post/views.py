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
            return render(request, 'home/home.html', {'post_id': post_id, 'page': 'Bài viết với ID là'})
        else:
            return redirect('home:home')

    def post(self, request, post_id):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            get_post_id = database.get_post_id(post_id)
            posts = database.json_post(get_post_id)
            return JsonResponse({'result': posts})
        else:
            return redirect('home:login')


class TopHashtagPost(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'home/home.html', {'page': 'Các bài viết nổi bật trong tuần'})
        else:
            return redirect('home:home')

    def post(self, request):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            get_post_in_top_x_hashtag = database.get_post_in_top_x_hashtag(str(3))
            posts = database.json_post(get_post_in_top_x_hashtag)
            return JsonResponse({'result': posts})
        else:
            return redirect('home:login')


class SetPost(View):
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
            database = Database(request.user.id)
            post_id = database.get_id_new_post()
            return redirect('post:ShowPost', post_id)


class EditPost(View):
    def get(self, request, post_id):
        if request.user.is_authenticated:
            return render(request, 'post/edit_post.html', {'post_id': post_id, 'page': 'Bài viết với ID là'})
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
            return render(request, 'home/home.html', {'hashtag_post': hashtag, 'page': 'Bài viết với Hashtag'})
        else:
            return redirect('home:home')

    def post(self, request, hashtag):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            get_post_hashtag = database.get_post_hashtag(hashtag.upper())
            posts = database.json_post(get_post_hashtag)
            return JsonResponse({'result': posts})
        else:
            return redirect('home:login')


class ApiTopHashtag(View):
    def post(self, request):
        if request.user.is_authenticated:
            database = Database(request.user.id)
            get_count_top_x_hashtag = database.get_count_top_x_hashtag(12)
            return JsonResponse({'result': get_count_top_x_hashtag})
        else:
            return redirect('home:login')


class Comment_post(View):
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        try:
            if data['content_input']:
                new_cm = Comment()
                new_cm.content = data['content_input']
                new_cm.user_id = request.user.id
                new_cm.post_id = data['post_id']
                new_cm.save()
                return HttpResponse('bình luận thành công, hãy tiếp tục tương tác nhé')
        except:
            pass
        database = Database(request.user.id)
        get_comment_post_id = database.get_comment_post_id(data['post_id'])
        return JsonResponse({'result': get_comment_post_id})



class Delete_comment(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            get_comment = Comment.objects.get(comment=data['comment_id'])
            if get_comment.user == request.user:
                get_comment.delete()
                return HttpResponse('Bạn vừa xóa thành công bình luận của mình')
            return HttpResponse('Bạn không thể xóa bình luận của người khác')
        else:
            return HttpResponse('Phiên đăng nhập  này đã hết hạn. vui lòng đăng nhập lại')
