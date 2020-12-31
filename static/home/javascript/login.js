axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"
let index_login = new Vue({
    el: '#index_login',
    delimiters: ['[[', ']]'],
    data: {
        regEX: /^[a-z0-9_-]{3,16}$/,
        login_bg: false,
        themes: 'login',
        info: null,
        login: {
            username: null,
            password: null,
            resultMess: null,
        },
        forgotPass: {
            email: null,
            resultMess: null,
        },
        resetPassword: {
            checkResetPassword: null,
            password1: null,
            password2: null,
            resultMess: null,
        },
        registerUser: {
            firstname: null,
            lastname: null,
            username: null,
            email: null,
            password1: null,
            password2: null,
            birthday: null,
            gender: null,
            checkUserName: null,
            checkEmail: null,
            checkPassword: null,
            resultMess: null,
        },

    },
    mounted: function () {

    },
    methods: {
        check__: function () {
            axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/check/',
                data: {
                    username: this.registerUser.username,
                    email: this.registerUser.email,
                },
            }).then(response => {
                this.info = response.data;

            })
        },
        checkUserName_func: function () {
            this.check__();
            this.registerUser.checkUserName = this.regEX.test(this.registerUser.username);
        },
        checkEmail_func: function () {
            this.check__();
            this.registerUser.checkEmail = /\S+@\S+\.\S+/.test(this.registerUser.email);
        },
        checkPassword_func: function () {
            this.registerUser.checkPassword = this.registerUser.password1 === this.registerUser.password2;
        },
        checkResetPassword: function () {
            console.log(this.resetPassword.password1);
            this.resetPassword.checkResetPassword = this.resetPassword.password1 === this.resetPassword.password2 && this.resetPassword.password1 !== '';

        },
        login_func: function () {
            axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/login/',
                data: {
                    username: this.login.username.toLowerCase(),
                    password: this.login.password,
                },
            }).then(response => {
                this.login.resultMess = response.data;
                if (this.login.resultMess === 'success') {
                    window.location.href = 'http://127.0.0.1:8000';
                }
            })
        },
        forgotPass_func: function () {
            axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/sendpass/',
                data: {
                    email: this.forgotPass.email,
                },
            }).then(response => {
                this.forgotPass.resultMess = response.data;

            })
        },


        register_func: function () {
            axios({
                method: 'post',
                url: 'http://127.0.0.1:8000/register/',
                data: {
                    firstname: this.registerUser.firstname,
                    lastname: this.registerUser.lastname,
                    username: this.registerUser.username.toLowerCase(),
                    email: this.registerUser.email,
                    password1: this.registerUser.password1,
                    birthday: this.registerUser.birthday,
                    gender: this.registerUser.gender,
                },
            }).then(response => {
                this.registerUser.resultMess = response.data;
            })
        }
    }
});