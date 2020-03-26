import { Customer } from '@/defines/models'

const newDialog = () => {
  return {
    action: undefined,
    formData: Customer(),
    index: -1,
    visible: false
  }
}

const state = {
  formDialog: newDialog()
}

const mutations = {
  SET_FORM_DIALOG: (state, dialogData) => {
    state.formDialog = dialogData
  },
  UPDATE_FORM_DIALOG: (state, dialogData) => {
    state.formDialog = Object.assign({}, state.formDialog, dialogData)
  }
}

const actions = {
  async resetFormDialog({ commit }) {
    commit('SET_FORM_DIALOG', newDialog())
  },
  async setFormDialog({ commit }, dialogData) {
    commit('SET_FORM_DIALOG', dialogData)
  },
  async updateFormDialog({ commit }, dialogData) {
    commit('UPDATE_FORM_DIALOG', dialogData)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
