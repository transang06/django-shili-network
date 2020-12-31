axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"


let home = new Vue({
    el: '#app_Shili',
    delimiters: ['[[', ']]'],
    data() {
        return {
            email: email,
            domain: domain,
            api_one_post: {},
            get_profile: {},
            api_get_all_user: {},
            api_top_friend: {},
            api_top_hashtag: {},
            api_your_friend: {},
            api_post: {},
            join_mess: '',


            themes: 'thongtin',
            edit: {
                first_name: '',
                first_name1: '',
                last_name: '',
                intro: '',
                email: '',
                address: '',
                gender: '',
                birthday: '',
                results: '',
            },
            edit_av_bg: {
                avatar: '',
                cover_image: '',
                results: '',
            },


            show_page: 'home',


            form_edit_post: false,
            show_sl: false,

            chat_content: {},
            run_Interval_chat: null,
            run_Interval_cmt: null,

            user_id: user_id,
            api_edit_post: {},
            chat: {
                input: null,
                input1: null,
                boxchat: {},
                chat_content: {},
                boxchat_on: false,
            },
            comment: {
                content_input: {},
                content_input1: {},
                comment_show: {}
            },
            friends: {
                top: {},
                all: {},
                join_mess: null,
            },
            search: {
                input: null,
                results: {},
            },

        }
    },
    created: function () {
        this.get_api_top_friend;
        this.get_api_top_hashtag;
        this.get_api_post;
        if (username) {
            this.get_profile_func
        }
        if (post_id) {
            this.api_one_post_func;
        }
        if (top3post) {
            this.api_top3_hashtag_post;
        }
        if (all_user) {
            this.api_get_all_user_func;
        }
        if (hashtag_post) {
            this.api_hashtag_post_func;
        }
        this.get_api_your_friend;


    },
    computed: {
        get_profile_func: function () {
            axios({
                method: 'post',
                url: '/profile/api/getprofile/',
                data: {
                    username: username
                },
            }).then(response => {
                this.get_profile = response.data;
            })
        },
        get_api_post: function () {
            axios({
                method: 'post',
                url: '/api/get_content/',
            }).then(response => {
                return this.api_post = response.data;
            })
        },
        get_api_top_friend: function () {
            axios({
                method: 'post',
                url: '/profile/api/top_friend/',
            }).then(response => {
                return this.api_top_friend = response.data;
            })
        },
        get_api_top_hashtag: function () {
            axios({
                method: 'post',
                url: '/post/api/top_hashtag/',
            }).then(response => {
                this.api_top_hashtag = response.data;
            });
        },
        get_api_your_friend: function () {
            axios({
                method: 'post',
                url: '/profile/api/your_friend/',
            }).then(response => {
                this.api_your_friend = response.data;
            });
        },
        api_one_post_func: function () {
            axios({
                method: 'post',
                url: "/post/" + post_id + '/',
            }).then(response => {
                this.api_one_post = response.data;
            })
        },
        api_top3_hashtag_post: function () {
            axios({
                method: 'post',
                url: "/post/",
            }).then(response => {
                this.api_one_post = response.data;
            })
        },
        api_hashtag_post_func: function () {
            axios({
                method: 'post',
                url: "/post/hashtag/" + hashtag_post,
                data: {
                    hashtag: hashtag_post,
                },
            }).then(response => {
                this.api_one_post = response.data;
            })
        },

        api_get_all_user_func: function () {
            axios({
                method: 'post',
                url: '/profile/alluser/',
            }).then(response => {
                this.api_get_all_user = response.data;
            })
        },

    },

    watch: {
        join_mess: {
            handler: function () {

                console.log(1)

            },
        }
    },

    methods: {
         scrollToTop() {
                window.scrollTo(0,0);
           },
        edit_profile: function () {
            axios({
                method: 'post',
                url: '/profile/api/editprofile/',
                data: {
                    first_name: this.edit.first_name,
                    last_name: this.edit.last_name,
                    intro: this.edit.intro,
                    email: this.edit.email,
                    address: this.edit.address,
                    gender: this.edit.gender,
                    birthday: this.edit.birthday,
                },
            }).then(response => {
                this.get_profile_fun;
                this.edit.results = response.data;
            })
        },
        forgotPass_func: function (email) {
            if (email === this.email) {
                axios({
                    method: 'post',
                    url: '/sendpass/',
                    data: {
                        email: email,
                    },
                }).then(response => {
                    this.edit.results = response.data;

                })
            } else {
                return this.forgotPass.resultMess = 'bạn không phải chủ tài khoản này';
            }
        },
        delete_post: function (post_id) {
            axios({
                method: 'post',
                url: "/post/delete/",
                data: {
                    post_id: post_id,
                },
            }).then(response => {
                this.open_link('/post/')
            })
        },
        edit_av_bg_func: function () {
            axios({
                method: 'post',
                url: "/profile/api/editavbg/",
                data: {
                    avatar: this.edit_av_bg.avatar,
                    cover_image: this.edit_av_bg.cover_image,
                },
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            }).then(response => {
                profile.get_profile_fun;
            })
        },
        add_follow: function (friends_id) {
            axios({
                method: 'post',
                url: "/profile/addfollow/",
                data: {
                    id: friends_id,
                },
            }).then(response => {
                this.join_mess = response.data;

            })
        },
        comment_func: function (post_id) {
            axios({
                method: 'post',
                url: '/post/comments/',
                data: {
                    content_input: home.comment.content_input[`${post_id}`],
                    post_id: post_id,
                },
            }).then(response => {
                home.comment.content_input = {};
                return home.comment.comment_show[`${post_id}`] = response.data;
            })
        },
        comment_show_func: function (post_id) {
            this.run_Interval_cmt = setInterval(function () {
                axios({
                    method: 'post',
                    url: '/post/comments/',
                    data: {
                        post_id: `${post_id}`,
                    },
                }).then(response => {
                    home.comment.comment_show[`${post_id}`] = response.data;
                    home.comment.content_input1 = {}
                })
            }, 1000);
            if (this.comment.comment_show[`${post_id}`]) {
                delete this.comment.comment_show[`${post_id}`];
                clearInterval(this.run_Interval_cmt);
                return this.comment.content_input1 = {};
            }

        }
        ,
        comment_delete_func: function (post_id, comment_id) {
            axios({
                method: 'post',
                url: '/post/delete_comment/',
                data: {
                    post_id: post_id,
                    comment_id: comment_id,
                },
            }).then(response => {
                home.comment.content_input1 = {};
                return home.comment.comment_show[`${post_id}`] = response.data;
            })
        },
        get_mess_content: function (user_2_id) {
            this.run_Interval_chat = setInterval(function () {
                axios({
                    method: 'post',
                    url: "/chat/",
                    data: {
                        user_2_id: user_2_id,
                    },
                }).then(response => {
                    home.chat_content = response.data['mess_content'];
                })
            }, 500);
        },
        show_box_chat: function () {
            home.chat.boxchat_on = false;
            clearInterval(this.run_Interval_chat);
        },
        chat_box_func: function (user_2_id) {
            home.chat.boxchat_on = true;
            clearInterval(this.run_Interval_chat);
            this.get_mess_content(user_2_id);
            axios({
                method: 'post',
                url: "/chat/",
                data: {
                    user_2_id: user_2_id,
                },
            }).then(response => {
                home.chat.boxchat = response.data['result'];
                this.scrollBottom();
            })
        },
        send_mess_func: function (user_2_id) {
            axios({
                method: 'post',
                url: "/chat/save_mess/",
                data: {
                    user_2_id: user_2_id,
                    content: this.chat.input,
                },
            }).then(response => {
                home.chat.input = '';
                this.scrollBottom();
                clearInterval(this.run_Interval);
                this.get_mess_content(user_2_id);

            })
        },
        delete_mess_func: function (m_id, from_user_id) {
            home.chat.boxchat_on = true;
            axios({
                method: 'post',
                url: "/chat/delete_mess/",
                data: {
                    m_id: m_id,
                    from_user_id: from_user_id,
                },
            }).then(response => {
                home.chat.input = '';
                console.log(response.data);
            })
        },
        scrollBottom: function () {
            let container = home.$el.querySelector("#container");
            container.scrollTop = container.scrollHeight;
        },
        open_link: function (link) {
            window.open(`${link}`, "_self");
        },
    },
})

