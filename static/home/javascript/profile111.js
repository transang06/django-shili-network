axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

let profile = new Vue({
    el: '#profile',
    delimiters: ['[[', ']]'],
    data: {
        themes: 'profile',
        username: username,
        email: email,
        user_id: user_id,
        get_profile: {},
        comment: {
            content_input: {},
            content_input1: {},
            comment_show: {}
        },
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


    },
    created: function () {
        axios({
            method: 'post',
            url: '/profile/api/getprofile/',
            data: {
                username: this.username
            },
        }).then(response => {
            profile.get_profile = response.data;
        })

    },

    methods: {
        get_profile_fun: function () {
            axios({
                method: 'post',
                url: '/profile/api/getprofile/',
                data: {
                    username: this.username
                },
            }).then(response => {
                profile.get_profile = response.data;
            })
        },
        comment_func: function (post_id) {
            axios({
                method: 'post',
                url: '/post/comments/',
                data: {
                    content_input: this.comment.content_input[`${post_id}`],
                    post_id: post_id,
                },
            }).then(response => {
                this.comment.content_input = {};
                return this.comment.comment_show[`${post_id}`] = response.data;
            })
        },
        comment_show_func: function (post_id) {
            setInterval(function () {
                axios({
                    method: 'post',
                    url: '/post/comments/',
                    data: {
                        post_id: `${post_id}`,
                    },
                }).then(response => {
                    profile.comment.comment_show[`${post_id}`] = response.data;
                    profile.comment.content_input1 = {}
                })
            }, 1000);
            if (this.comment.comment_show[`${post_id}`]) {
                delete this.comment.comment_show[`${post_id}`];
                return this.comment.content_input1 = {};
            }

        },
        comment_delete_func: function (post_id, comment_id) {
            axios({
                method: 'post',
                url: '/post/delete_comment/',
                data: {
                    post_id: post_id,
                    comment_id: comment_id,
                },
            }).then(response => {
                this.comment.content_input1 = {};
                return this.comment.comment_show[`${post_id}`] = response.data;
            })
        }
        ,

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
                    // avatar: this.edit.avatar,
                    // cover_image: this.edit.cover_image,
                },
            }).then(response => {
                profile.get_profile_fun();
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
        add_follow: function (friends_id) {
            axios({
                method: 'post',
                url: "/profile/addfollow/",
                data: {
                    id: friends_id,
                },
            }).then(response => {
                profile.get_profile_fun();
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
                profile.get_profile_fun();
                console.log(response.data)

            })
        },
        openlink: function (link) {
            window.open(`${link}`, "_self");
        }

    },


})
