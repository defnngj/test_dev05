import Vuex from 'vuex'
import Vue from 'vue'


Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        user: {},
        token: null,
        title: ''
    },
    mutations: {
        'login': (state, data) => {
            localStorage.token = data;
            state.token = data;
        },
        'logout': (state) => {
            localStorage.removeItem('token');
            state.token = null
        },
        'title': (state, data) => {
            state.title = data;
        }
    }
})