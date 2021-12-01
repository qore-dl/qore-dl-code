import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    Token: localStorage.getItem('Token') ? localStorage.getItem('Token') : ''
  },
  mutations: {
    // 修改token，并将token存入localStorage
    changeLogin (state, user) {
      state.Token = user.Token;
      localStorage.setItem('Token', user.Token);
    }
  },
  actions: {
  },
  modules: {
  }
})
