import random

from django.db import models


# Create your models here.
from post.models import Post
from user.models import MyUser, Conversation, Message


class ShiliEmail:
    def __init__(self, key, ban_ma,email):
        self.ban_ma = str(ban_ma)
        self.key = str(key)
        self.email = str(email)

    def xac_thuc(self):
        ketqua = """
           <!DOCTYPE html>
           <html lang="en">
           <head>
               <meta charset="UTF-8">
               <title>Title</title>
               <style>
                   html, body, ul {
                       margin: 0;
                       padding: 0;
                       scroll-behavior: smooth;
                   }        
                   body {
                       display: grid;
                       grid-template: 1fr/1fr;
                       background-color: #5B7D87;
                   }
                   #welcome {
                       background-color: #5B7D87;
                       background-image: -webkit-linear-gradient(45deg, #91B3BC 50%, #5B7D87 50%);
                       display: flex;
                       flex-flow: column wrap;
                       align-content: center;
                       justify-content: center;
                       width: 100%;
                       height: 100%;
                       padding: 20px;
                   }        
                   #welcome #chao {
                       font-family: "Segoe UI", serif;
                       font-style: italic;
                       font-size: 100px;
                       color: #FFFFFF;
                       font-weight: bold;
                   }        
                   #welcome p {
                       text-align: right;
                   }        
                   .chu {
                       font-family: "Consolas", serif;
                       font-size: 25px;
                       color: #FFFFFF
                   }
                   a{  font-style: unset;
                       text-decoration: underline;
                   }        
               </style>
           </head>
           <body>
           <div id="welcome">
               <div>
                   <div id="chao">WELCOME TO Shili</div>
                   <p class="chu">Bắt trọn khoảnh khắc - Dẫn dắt xu hướng </p>
                   <p class="chu"> Xin chào """ + self.email + """</p>
                   <a class="chu" style="color: #06628c" 
                   href="http://127.0.0.1:8000/xacthuc/""" + self.key + "/" + self.ban_ma + """">
                   Xác thực tài khoản của bạn
                   </a>
                </div>
            </div>
            </body>
             """
        return ketqua

    def reset_password(self):
        ketqua = """
           <!DOCTYPE html>
           <html lang="en">
           <head>
               <meta charset="UTF-8">
               <title>Title</title>
               <style>
                   html, body, ul {
                       margin: 0;
                       padding: 0;
                       scroll-behavior: smooth;
                   }        
                   body {
                       display: grid;
                       grid-template: 1fr/1fr;
                       background-color: #5B7D87;
                   }
                   #welcome {
                       background-color: #5B7D87;
                       background-image: -webkit-linear-gradient(45deg, #91B3BC 50%, #5B7D87 50%);
                       display: flex;
                       flex-flow: column wrap;
                       align-content: center;
                       justify-content: center;
                       width: 100%;
                       height: 100%;
                       padding: 20px;
                   }        
                   #welcome #chao {
                       font-family: "Segoe UI", serif;
                       font-style: italic;
                       font-size: 100px;
                       color: #FFFFFF;
                       font-weight: bold;
                   }        
                   #welcome p {
                       text-align: right;
                   }        
                   .chu {
                       font-family: "Consolas", serif;
                       font-size: 25px;
                       color: #FFFFFF
                   }
                   a{  font-style: unset;
                       text-decoration: underline;
                   }        
               </style>
           </head>
           <body>
           <div id="welcome">
               <div>
                   <div id="chao">WELCOME TO Shili</div>
                   <p class="chu">Bắt trọn khoảnh khắc - Dẫn dắt xu hướng </p>
                   <p class="chu"> Xin chào """ + self.email + """</p>
                   <a class="chu" style="color: #06628c" href="http://127.0.0.1:8000/resetpassword/""" + self.key + "/" + self.ban_ma + """">Đặt Lại mật khẩu</a>
                </div>
            </div>
            </body>
             """
        return ketqua


class MaHoaOneTimePad:
    def __init__(self):
        self.charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_.".lower()

    def ma_hoa(self, plaintext):
        otp = "".join(random.sample(self.charset, len(self.charset)))
        result = ""
        for c in plaintext.lower():
            if c not in otp:
                continue
            else:
                result += otp[self.charset.find(c)]
        return otp, result

    def giai_ma(self, otp, secret):
        result = ""
        for c in secret.lower():
            if c not in otp:
                continue
            else:
                result += self.charset[otp.find(c)]
        return result

class Database:
    def __init__(self, userid):
        self.userid = str(userid)

    def get_database_index(self):
        context = {
            'all_post': self.getPostOfFollow(),
            'top_hashtag': self.getTop3Hashtag(),
            'top_friends': self.getTop3Folower(),
            'followres': self.getFlower(),
        }
        return context

    # Lấy toàn bộ bài đăng của tài khoản đang theo dõi
    def getPostOfFollow(self):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.user_id IN(SELECT followres_id FROM user_follower WHERE main_user_id = " + self.userid + ") OR a.user_id = " + self.userid + "  ORDER BY a.created_at DESC"
        PostOfFollow = Post.objects.raw(sql)
        return PostOfFollow

    # Lấy top 3 hashtag nỗi bật trả về tên và số lượt
    def getTop3Hashtag(self):
        sql = "SELECT  hashtag,count(hashtag) AS SoLuot FROM post_post GROUP BY hashtag  ORDER BY SoLuot DESC"
        Top3Hashtag = Post.objects.raw(sql)[0:3]
        return Top3Hashtag

    # Lấy top 3 người chưa theo dõi
    def getTop3Folower(self):
        sql = "SELECT * FROM user_myuser WHERE id !=" + str(
            self.userid) + " AND id NOT IN (SELECT followres_id FROM user_follower c WHERE c.main_user_id = " \
              + str(self.userid) + " ) Order by date_joined DESC"
        Top3Folower = Post.objects.raw(sql)[0:3]
        return Top3Folower

    # Lấy ra toàn bộ người đang theo dõi của tài khoản đăng nhặp
    def getFlower(self):
        sql = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE main_user_id = " + str(
            self.userid) + ") b ON a.id = b.followres_id"
        getFlower = MyUser.objects.raw(sql)
        return getFlower

        # trả về các comments của bài đang bình luận

    def post_comment(self, post_id):
        sql_comments = "SELECT * FROM post_comment a JOIN user_myuser b ON  a.user_id = b.id WHERE a.post_id =" + str(
            post_id)
        post_comment = Post.objects.raw(sql_comments)
        return post_comment

    # lấy ra danh sách các tài khoản mình đang theo dõi
    def get_followers_with_username(self, username):
        id_ = self.get_id_with_username(username)
        sql_followres = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE main_user_id = " + str(
            id_) + ") b ON a.id = b.followres_id"
        followres = MyUser.objects.raw(sql_followres)
        return followres

    # lấy ra danh sách các tài khoản đang theo dõi mình
    def get_danhsach_nguoitheodoi(self, username):
        id = self.get_id_with_username(username)
        sql_followres = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE followres_id ='" + str(
            id) + "') b ON a.id = b.main_user_id"
        followres = MyUser.objects.raw(sql_followres)
        return followres

    # laasytaast cẩ người dung
    def all_user(self):
        sql = "SELECT * FROM user_myuser"
        all_user = MyUser.objects.raw(sql)
        return all_user

    def get_id_with_username(self, username):
        sql_get_user_id = "SELECT * FROM user_myuser a WHERE a.username ='" + str(username) + "'"
        get_user_id = Conversation.objects.raw(sql_get_user_id)

        a = get_user_id[:1][0].id
        return a

    def get_post_id(self, post_id):
        sql_post_hashtag = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.post = '" + str(
            post_id) + "' "
        posts = Post.objects.raw(sql_post_hashtag)
        return posts

    def get_top3_hashtag_post(self):
        sql_post_hashtag = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id JOIN( SELECT hashtag,count(hashtag) AS SoLuot FROM post_post GROUP BY hashtag  ORDER BY SoLuot DESC LIMIT 3) c ON a.hashtag =c.hashtag"
        posts = Post.objects.raw(sql_post_hashtag)
        return posts

    def get_search_post(self, key):
        sql_post_hashtag = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.hashtag like '%" + key + "%'"
        posts = Post.objects.raw(sql_post_hashtag)
        return posts

    def get_profile_post(self, username):
        user = str(username)
        sql_user_posts = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE b.username ='" + user + "' ORDER BY created_at DESC"
        user_posts = Post.objects.raw(sql_user_posts)
        return user_posts

    def get_profile(self, username):
        # in ra thông  tin người dùng (tham số có thể là  username hoặc id)
        user = str(username)
        sql_profile = "SELECT * FROM user_myuser a WHERE a.username ='" + user + "' OR a.id ='" + user + "'"
        profile = MyUser.objects.raw(sql_profile)
        return profile

    def followres(self):
        sql = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE main_user_id = " + self.userid + ") b ON a.id = b.followres_id"
        profile = MyUser.objects.raw(sql)
        return profile

    def id_room(self, user_1, user_2):
        sql = "SELECT c_id FROM user_conversation WHERE user_1_id = '" + str(user_1) + "' AND user_2_id = '" + str(
            user_2) + "' OR user_2_id =  '" + str(user_1) + "' AND user_1_id = '" + str(user_2) + "'"
        kt = Conversation.objects.raw(sql)[:1]

        if kt:
            a = kt[0].c_id
            return a
        else:
            return False

    def id_follow(self, user_1, user_2):
        sql = "SELECT f_id FROM user_follower WHERE main_user_id = " + str(
            user_1) + " AND followres_id =  " + str(user_2)
        kt = Conversation.objects.raw(sql)[:1]

        if kt:
            a = kt[0].f_id
            return a
        else:
            return False

    def context_room_chat(self, id_room):
        sql = "SELECT * FROM user_message WHERE conversation_id =" + str(id_room)
        ketqua = Conversation.objects.raw(sql)
        return ketqua

    def soLuongTinCuaBox(self, id_room):
        sql = "SELECT COUNT(m_id) AS SoTin FROM user_conversation a JOIN user_message b ON a.c_id = b.conversation_id WHERE a.c_id =" + str(
            id_room)
        soluongtin = Message.objects.raw(sql)[:1][0].SoTin
        return soluongtin
