import {
  stocksApi,
  industriesApi,
  conceptsApi,
  sectionsApi,
  territoriesApi,
  reportTypesApi,
  subjectsApi
} from '@/api'

// 缓存数据
const state = {
  stocks: {
    data: {},
    loading: false,
  },
  industries: {
    data: [],
    loading: false,
  },
  concepts: {
    data: [],
    loading: false,
  },
  sections: {
    data: [],
    loading: false,
  },
  territories: {
    data: [],
    loading: false,
  },
  reportTypes: {
    data: [],
    loading: false,
  },
  accountingSubjects: {},
}

function get_report_type_slug(reportTypes, id) {
  for (reportType of reportTypes) {
    if (reportType.id == id) {
      return reportType.slug
    }
  }
}

const mutations = {
  SET_STOCKS: (state, stocks) => {
    for (stock of stocks) {
      state.stocks.data[stock.id] = stock
    }
  },
  ADD_STOCK: (state, stock) => {
    state.stocks.data[stock.id] = stock
  },
  INIT_SUBJECTS: (state, subjects) => {
    for (subject of subjects) {
      const slug = get_report_type_slug(state.reportTypes, subject.report_type)
      if (!state.accountingSubjects[slug]) {
        state.accountingSubjects[slug] = []
      }
      state.accountingSubjects[slug].push(subject)
    }
  }
}

const actions = {
  async getStock({ commit, state }, stock_id) {
    state.stocks.loading = true
    if (Object.keys(state.stocks.data).indexOf(stock_id) > -1) {
      return state.stocks.data[stock_id]
    }
    const stock = await stocksApi.show(stock_id)
    commit('ADD_STOCK', stock)
    state.stocks.loading = false
    return stock
  },
  async loadStocks({ commit }, query) {
    if (query !== '') {
      state.stocks.loading = true
      const { results } = await stocksApi.list({
        params: { q: query }
      })
      commit('SET_STOCKS', results)
      state.stocks.loading = false
      return results
    } else {
      return []
    }
  },
  async loadIndustries({ state }, params) {
    state.industries.loading = true
    const { results } = await industriesApi.list({ params })
    state.industries.data = results
    state.industries.loading = false
    return results
  },
  async loadConcepts({ state }, params) {
    state.concepts.loading = true
    const { results } = await conceptsApi.list({ params })
    state.concepts.data = results
    state.concepts.loading = false
    return results
  },
  async loadSections({ state }, params) {
    state.sections.loading = true
    const { results } = await sectionsApi.list({ params })
    state.sections.data = results
    state.sections.loading = false
    return results
  },
  async loadTerritories({ state }, params) {
    state.territories.loading = true
    const { results } = await territoriesApi.list({ params })
    state.territories.data = results
    state.territories.loading = false
    return results
  },
  async loadReportTypes({ state }, params) {
    state.reportTypes.loading = true
    const types = await reportTypesApi.list({ params })
    state.reportTypes.data = types
    state.reportTypes.loading = false
    return types
  },
  async loadAccountingSubjects({ commit, state }, params) {
    const subjects = await subjectsApi.list({ params })
    commit('INIT_SUBJECTS', subjects)
    return state.accountingSubjects
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
