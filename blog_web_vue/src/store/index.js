import { createStore } from 'vuex'
import createPersistedState from 'vuex-persistedstate'

export default createStore({
  state: {
    username:null,
    userid:null,
    isLoggedIn:false,

    articledetail:null
  },
  mutations: {
    setUsername(state,username){
      state.username = username
    },
    setUserid(state,userid){
      state.userid = userid
    },
    setIsLoggedIn(state,isLoggedIn){
      state.isLoggedIn = isLoggedIn
    },

    setarticledetail(state,articledetail){
      state.articledetail = articledetail
    }
  },
  actions: {
    xlogin({commit},{username,userid}){
      commit('setUsername',username)
      commit('setUserid',userid)
      commit('setIsLoggedIn',true)
    },
    xloginout({commit}){
      commit('setUsername',null)
      commit('setUserid',null)
      commit('setIsLoggedIn',false)
    },
    startLogoutTimer({ dispatch }, timeout) {
      setTimeout(() => {
        dispatch('xloginout')
      }, timeout)
    }
  },
  plugins: [
    createPersistedState({
      storage: window.localStorage
    })
  ],
  modules: {
  }
})
