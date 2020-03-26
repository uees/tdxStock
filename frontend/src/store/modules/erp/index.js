import entering_warehouse from './entering_warehouse'
import shipment from './shipment'
import customers from './customers'
import basedata from './basedata'
import qc_records from './qc_records'

export default {
  namespaced: true,
  modules: {
    entering_warehouse,
    shipment,
    customers,
    basedata,
    qc_records
  }
}
