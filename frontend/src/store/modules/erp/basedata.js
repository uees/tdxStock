import { rolesApi } from '@/api/user'
import { customersApi } from '@/api/erp'

// 用于提示建议的数据
const state = {
  roles: {
    data: [],
    loading: false
  },
  customers: {
    data: [],
    loading: false
  }
}

const mutations = {
  SET_ROLES_DATA: (state, roles) => {
    state.roles.data = roles
  },
  SET_ROLES_LOADING: (state, loading) => {
    state.roles.loading = loading
  },
  SET_CUSTOMERS_DATA: (state, customers) => {
    state.customers.data = customers
  },
  SET_CUSTOMERS_LOADING: (state, loading) => {
    state.roles.loading = loading
  }
}

const actions = {
  async loadRoles({ commit }) {
    commit('SET_ROLES_LOADING', true)
    const { data } = await rolesApi.list({
      params: {
        all: true
      }
    })
    commit('SET_ROLES_DATA', data)
    commit('SET_ROLES_LOADING', false)

    return data
  },
  async loadCustomers({ commit }, query) {
    if (query !== '') {
      commit('SET_CUSTOMERS_LOADING', true)
      const { data } = await customersApi.list({
        params: { q: query }
      })
      commit('SET_CUSTOMERS_DATA', data)
      commit('SET_CUSTOMERS_LOADING', false)

      return data
    } else {
      return []
    }
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
