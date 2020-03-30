const state = {
  stocks: [],
  index: -1
}

const mutations = {
  SET_STOCKS: (state, stocks) => {
    state.stocks = stocks
  },
  ADD_STOCK: (state, stock) => {
    state.stocks.push(stock)
  },
  UPDATE_STOCK: (state, context) => {
    state.stocks.splice(context.index, 1, context.stock)
  },
  DELETE_STOCK: (state, index) => {
    state.stocks.splice(index, 1)
  },
  SET_INDEX: (state, index) => {
    state.index = index
  }
}

const actions = {

}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
