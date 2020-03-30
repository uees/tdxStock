import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'
import errorLog from './modules/errorLog'
import basedata from './modules/basedata'
import compare from './modules/compare'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    errorLog,
    basedata,
    compare
  },
  getters
})
