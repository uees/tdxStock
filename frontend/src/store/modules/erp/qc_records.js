const state = {
  visible: false,
  recycled_thing: undefined,
  index: -1
}

const mutations = {
  SET_VISIBLE: (state, visible) => {
    state.visible = visible
  },
  SET_RECYCLED_THING: (state, recycled_thing) => {
    state.recycled_thing = recycled_thing
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
