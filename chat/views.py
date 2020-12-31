import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from home.models import Database
from user.models import Conversation, MyUser, Message


class BoxChat(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            user_2_id = str(data['user_2_id'])
            database = Database(request.user.id)
            id_room = database.id_room(request.user.id, user_2_id)
            if not id_room:
                try:
                    Conv = Conversation()
                    Conv.user_1 = MyUser.objects.get(id=request.user.id)
                    Conv.user_2 = MyUser.objects.get(id=user_2_id)
                    Conv.save()
                except:
                    return redirect('home:home')
            soluongtin = database.soLuongTinCuaBox(id_room),
            sql = "SELECT * FROM user_myuser a WHERE a.username ='" + user_2_id + "' OR a.id ='" + user_2_id + "'"
            thong_tin_user_2 = MyUser.objects.raw(sql)
            thislist = []
            for i in thong_tin_user_2:
                thisdict = {}
                thisdict["user_id"] = i.id
                thisdict["avatar"] = str(i.avatar)
                thisdict["username"] = i.username
                thisdict["full_name"] = i.first_name + i.last_name
                thisdict["soluongtin"] = soluongtin
                thislist.append(thisdict)
            sql = "SELECT * FROM user_message WHERE conversation_id =" + str(id_room)
            mess = Conversation.objects.raw(sql)
            mess_content = []
            for i in mess:
                thisdict = {}
                thisdict["from_user_id"] = i.from_user_id
                thisdict["created_at"] = i.created_at
                thisdict["content"] = i.content
                thisdict["m_id"] = i.m_id
                mess_content.append(thisdict)
        return JsonResponse({'result': thislist, 'mess_content': mess_content})


class SaveMess(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            user_2_id = str(data['user_2_id'])
            database = Database(request.user.id)
            id_room = database.id_room(request.user.id, user_2_id)
            # lưu tin nhắn
            if data['content'] != '':
                Mess = Message()
                Mess.from_user = MyUser.objects.get(id=request.user.id)
                Mess.conversation = Conversation.objects.get(c_id=id_room)
                Mess.content = data['content']
                Mess.save()
            return HttpResponse('Gửi thành công')
        else:
            return redirect('home:home')


class DeleteMess(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = json.loads(request.body.decode('utf-8'))
            m_id = str(data['m_id'])
            get_message = Message.objects.get(m_id=m_id)
            if str(data['from_user_id']) == str(request.user.id) and get_message:
                get_message.delete()
                return HttpResponse('Xóa thành công')
            return HttpResponse('Xóa thất bại')
        else:
            return HttpResponse('Chưa Đăng Nhập')
