import RestApi from '../utils/restapi'
import request from '../utils/request'

export const enteringWarehousesApi = new RestApi({
  url: '/entering-warehouses'
})

export const shipmentsApi = new RestApi({
  url: '/shipments'
})

export const qcRecordsApi = new RestApi({
  url: '/qc-records'
})

export const customersApi = new RestApi({
  url: '/customers'
})

export const recyclesApi = new RestApi({
  url: '/recycles',
  methods: ['list', 'destroy', 'show']
})

export function recycle(data, config) {
  return request.post('/recycles/recycle', data, config)
}

export function updateRecycled(id, data, config) {
  return request.patch(`/recycles/recycle/${id}`, data, config)
}

export function confirm(id, data, config) {
  return request.patch(`/recycles/confirm/${id}`, data, config)
}

export function getRecycledStatistics(params) {
  return request.get('/recycled-statistics', { params })
}

export function getRecycledStatisticsRange(params) {
  return request.get('/recycled-statistics/range', { params })
}

export function makeRecycledStatistics(data, config) {
  return request.post('/recycled-statistics', data, config)
}

export function makeAllCustomersRecycledStatistics(data, config) {
  return request.post('/recycled-statistics/customers', data, config)
}
