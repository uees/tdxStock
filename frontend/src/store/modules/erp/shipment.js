import { Shipment } from '@/defines/models'

const newDialog = () => {
  return {
    action: undefined,
    formData: Shipment(),
    index: -1,
    visible: false
  }
}

const state = {
  formDialog: newDialog()
}

const mutations = {
  SET_FORM_DIALOG: (state, dialog_data) => {
    state.formDialog = dialog_data
  },
  UPDATE_FORM_DIALOG: (state, dialog_data) => {
    state.formDialog = Object.assign({}, state.formDialog, dialog_data)
  }
}

const actions = {
  async resetFormDialog({ commit }) {
    commit('SET_FORM_DIALOG', newDialog())
  },
  async setFormDialog({ commit }, dialog_data) {
    commit('SET_FORM_DIALOG', dialog_data)
  },
  async updateFormDialog({ commit }, dialog_data) {
    commit('UPDATE_FORM_DIALOG', dialog_data)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
