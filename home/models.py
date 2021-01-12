import random
from post.models import Post, Comment
from user.models import MyUser, Conversation, Message


class ShiliEmail:
    def form_mail(self, url, content, email):
        form_mail = """
       <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                #index_login {
                    background-color: #5B7D87;
                    background-image: -webkit-linear-gradient(45deg, #91B3BC 50%, #5B7D87 50%);
                    height: 100%;
                    z-index: 0;
                    padding: 50px;
                    padding-top:0;
                }
        
                .btn-grad {
                    background-image: linear-gradient(to right, #FF512F 0%, #F09819 51%, #FF512F 100%);
                }
        
                .btn-grad {
                    margin: 20px auto;
                    padding: 15px 45px;
                    text-align: center;
                    text-transform: uppercase;
                    transition: 0.5s;
                    background-size: 200% auto;
                    color: #070000;
                    box-shadow: 0 0 10px #eee;
                    border-radius: 10px;
                    display: block;
                    font-weight: bold;
                }
        
                .btn-grad:hover {
                    background-position: right center;
                    color: #efefef;
                   
                }
        
                .welcome h1 {
                    font-family: "Segoe UI", serif;
                    font-style: italic;
                    font-size: 100px;
                    color: #FFFFFF;
                    font-weight: bold;
                }
        
                .welcome h2, .welcome a {
                    font-family: "Segoe UI", serif;
                    font-style: italic;
                    font-size: 35px;
                    color: #FFFFFF;
                    font-weight: bold;
                    text-decoration: none;
                }
        
                .welcome p {
                    text-align: right;
                    font-family: "Consolas", serif;
                    font-size: 35px;
                    color: #FFFFFF
                }
        
                h1 span {
                    font-family: 'Berkshire Swash', cursive;
                    font-weight: bold;
                    color: #F18E16;
                    font-size: 150px;
                    text-transform: capitalize;
                    font-style: normal;
                }
            </style>
        </head>
        <body>
        <div id="index_login">
            <div class="welcome ">
                <h1 class="col-12">WELCOME TO <span>Shili</span></h1>
                <p class="col-12">Bắt trọn khoảnh khắc - Dẫn dắt xu hướng </p>
                <h2> Xin chào """ + email + """</h2>
                <a class="btn-grad" href=" """ + url + """ " >""" + content + """</a>
            </div>
        </div>
        </body>
             """
        return form_mail


class MaHoaOneTimePad:
    def __init__(self):
        self.charset = "v4b7zt9c8fwj5ok0.h6euqai1@lxrgd2yms_pn3".lower()
        # self.charset = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@_.".lower()

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

    # Lấy toàn bộ bài đăng của tài khoản đang theo dõi
    def get_post_index(self):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE (a.user_id IN(SELECT followres_id FROM user_follower WHERE main_user_id = " + self.userid + ") OR a.user_id = " + self.userid + ")  AND a.public != 'Chỉ Mình Tôi' ORDER BY a.created_at DESC"
        return Post.objects.raw(sql)

    # Lấy ra thông tin 1 bài viết với id cụ thể
    def get_post_id(self, post_id):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.post = '" + str(
            post_id) + "'"
        return Post.objects.raw(sql)

    #  Trả về json thông tin bài viết
    def json_post(self, get_post):
        posts = []
        for i in get_post:
            thisdict = {}
            thisdict["post_id"] = i.post
            thisdict["username"] = i.username
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["feeling"] = i.feeling
            thisdict["created_at"] = i.created_at.strftime("%H:%M:%S ngày %m/%d/%Y")
            thisdict["public"] = i.public
            thisdict["content"] = i.content
            thisdict["hashtag"] = i.hashtag
            thisdict["user_id"] = i.user_id
            thisdict["avatar"] = str(i.avatar)
            thisdict["photo"] = str(i.photo)
            posts.append(thisdict)
        return posts

    # Lấy ra thông tin bài viết nằm trong top x hashtag nổi bật
    def get_post_in_top_x_hashtag(self, limit):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id JOIN( SELECT hashtag,count(hashtag) AS SoLuot FROM post_post GROUP BY hashtag  ORDER BY SoLuot DESC LIMIT " + limit + ") c ON a.hashtag =c.hashtag"
        return Post.objects.raw(sql)

    # Lấy id bài viết mới đăng gần nhất của tài khoản đăng nhập
    def get_id_new_post(self):
        sql = 'SELECT post From user_myuser a JOIN post_post b on a.id =  b.user_id ORDER BY created_at DESC LIMIT 1'
        return Post.objects.raw(sql)[0].post

    # Lấy ra thông tin bài viết cho hashtag bất kì
    def get_post_hashtag(self, hashtag):
        sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE a.hashtag = '" + hashtag + "'"
        return Post.objects.raw(sql)

    # Lấy tên hashtag và  số lượt xuất hiện trong top x hashtag
    def get_count_top_x_hashtag(self, limit):
        sql = "SELECT  hashtag,count(hashtag) AS soluot FROM post_post GROUP BY hashtag  ORDER BY soluot DESC"
        count_top_x_hashtag = []
        for i in Post.objects.raw(sql)[0:limit]:
            thisdict = {}
            thisdict["hashtag"] = i.hashtag
            thisdict["soluot"] = i.soluot
            count_top_x_hashtag.append(thisdict)
        return count_top_x_hashtag

    # trả về tất cả comments của bài viết với post_id
    def get_comment_post_id(self, post_id):
        sql = "SELECT * FROM post_comment a JOIN user_myuser b ON  a.user_id = b.id WHERE a.post_id =" + str(
            post_id)
        comment_post_id = []
        for i in Comment.objects.raw(sql):
            thisdict = {}
            thisdict["content"] = i.content
            thisdict["user_id"] = i.user_id
            thisdict["username"] = i.username
            thisdict["comment_id"] = i.comment
            thisdict["fullname"] = i.first_name + i.last_name
            thisdict["created_at"] = i.created_at.strftime("%H:%M:%S ngày %m/%d/%Y")
            thisdict["post_id"] = i.post_id
            comment_post_id.append(thisdict)
        return comment_post_id

    # trả về toàn bộ thông tin người dùng với username
    def get_profile(self, username):
        sql = "SELECT * FROM user_myuser a WHERE a.username ='" + str(username) + "'"
        get_profile = MyUser.objects.raw(sql)
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
            thisdict["date_joined"] = i.date_joined.strftime("%H:%M:%S ngày %m/%d/%Y")
            thisdict["is_superuser"] = i.is_superuser
            profile.append(thisdict)
        return profile

    # Lấy ra tất cả bài viết của username nhập vào
    def get_profile_posts(self, username, session_user):
        if username != session_user:
            sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE b.username ='" + str(
                username) + "'  AND a.public != 'Chỉ Mình Tôi' ORDER BY created_at DESC"
        else:
            sql = "SELECT * FROM post_post a JOIN user_myuser b ON a.user_id =  b.id WHERE b.username ='" + str(
                username) + "' ORDER BY created_at DESC"
        get_profile_posts = Post.objects.raw(sql)
        profile_posts = []
        for i in get_profile_posts:
            thisdict = {}
            thisdict["post_id"] = i.post
            thisdict["username"] = i.username
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["feeling"] = i.feeling
            thisdict["created_at"] = i.created_at.strftime("%H:%M:%S ngày %m/%d/%Y")
            thisdict["public"] = i.public
            thisdict["content"] = i.content
            thisdict["hashtag"] = i.hashtag
            thisdict["user_id"] = i.user_id
            thisdict["avatar"] = str(i.avatar)
            thisdict["photo"] = str(i.photo)
            profile_posts.append(thisdict)
        return profile_posts

    # Chuyển đổi username thành id
    def username_convert_id(self, username):
        user_id_sql = "SELECT id FROM user_myuser WHERE username ='" + str(username) + "'"
        return MyUser.objects.raw(user_id_sql)[0].id

    # Chuyển đổi id thành username
    def id_convert_username(self, id):
        user_id_sql = "SELECT username FROM user_myuser WHERE id =" + str(id)
        return MyUser.objects.raw(user_id_sql)[0].username

    # lấy ra các tài khoản mà username đang theo dõi
    def get_watching(self, username):
        user_id = self.username_convert_id(username)
        sql = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE main_user_id = " + str(
            user_id) + ") b ON a.id = b.followres_id WHERE  a.id !='" + str(user_id) + "'"
        get_watching = MyUser.objects.raw(sql)
        profile_watching = []
        for i in get_watching:
            thisdict = {}
            thisdict["avatar"] = str(i.avatar)
            thisdict["username"] = i.username
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["id"] = i.id
            profile_watching.append(thisdict)
        return profile_watching

    # lấy ra các tài khoản đang theo dõi username (được theo dõi)
    def get_followed(self, username):
        user_id = self.username_convert_id(username)
        sql = "SELECT * FROM user_myuser a JOIN (SELECT * FROM user_follower WHERE followres_id ='" + str(
            user_id) + "') b ON a.id = b.main_user_id WHERE  a.id !='" + str(user_id) + "'"
        get_followed = MyUser.objects.raw(sql)
        profile_followed = []
        for i in get_followed:
            thisdict = {}
            thisdict["avatar"] = str(i.avatar)
            thisdict["username"] = i.username
            thisdict["full_name"] = i.first_name + " " + i.last_name
            thisdict["id"] = i.id
            profile_followed.append(thisdict)
        return profile_followed

    # Lấy tất cả người dùng mà tài khoản đăng nhập chưa theo dõi
    def get_all_user(self):
        sql = "SELECT * FROM user_myuser WHERE id !=" + self.userid + " AND id NOT IN (SELECT followres_id FROM user_follower c WHERE c.main_user_id = " + self.userid + " ) Order by date_joined DESC"
        get_all_user = MyUser.objects.raw(sql)
        all_user = []
        for i in get_all_user:
            thisdict = {}
            thisdict["id"] = i.id
            thisdict["username"] = i.username
            thisdict["avatar"] = str(i.avatar)
            thisdict["full_name"] = i.first_name + " " + i.last_name
            all_user.append(thisdict)
        return all_user

    # kiểm tra xem đã theo dõi chưa
    def check_id_follow(self, user_1, user_2):
        sql = "SELECT f_id FROM user_follower WHERE main_user_id = " + str(
            user_1) + " AND followres_id =  " + str(user_2)
        if Conversation.objects.raw(sql)[:1]:
            return Conversation.objects.raw(sql)[:1][0].f_id
        else:
            return False

    # kiểm tra xem đã có phòng chat chưa
    def check_box_chat(self, user_1, user_2):
        sql = "SELECT c_id FROM user_conversation WHERE user_1_id = '" + str(user_1) + "' AND user_2_id = '" + str(
            user_2) + "' OR user_2_id =  '" + str(user_1) + "' AND user_1_id = '" + str(user_2) + "'"
        if Conversation.objects.raw(sql)[:1]:
            return Conversation.objects.raw(sql)[0:1][0].c_id
        else:
            return False

    # đếm số  tin nhắn của phòng chat
    def count_mess(self, id_room):
        sql = "SELECT COUNT(m_id) AS SoTin FROM user_conversation a JOIN user_message b ON a.c_id = b.conversation_id WHERE a.c_id =" + str(
            id_room)
        return Message.objects.raw(sql)[0:1][0].SoTin

    # lấy nội dung chat của phòng chat
    def get_context_box_chat(self, id_room):
        sql = "SELECT * FROM user_message WHERE conversation_id =" + str(id_room)
        mess = Conversation.objects.raw(sql)
        context_box_chat = []
        for i in mess:
            thisdict = {}
            thisdict["from_user_id"] = i.from_user_id
            thisdict["created_at"] = i.created_at.strftime("%H:%M:%S ngày %m/%d/%Y")
            thisdict["content"] = i.content
            thisdict["m_id"] = i.m_id
            context_box_chat.append(thisdict)
        return context_box_chat
