import RestApi from '../utils/restapi'
import request from '../utils/request'

/**
 * 获取股票列表和查看单个股票
 */
export const stocksApi = new RestApi({
  url: '/stocks/',
  methods: ['list', 'show']
})

/**
 * 行业信息接口
 */
export const industriesApi = new RestApi({
  url: '/industries/',
  methods: ['list', 'show']
})

/**
 * 概念接口
 */
export const conceptsApi = new RestApi({
  url: '/concepts/',
  methods: ['list', 'show']
})

/**
 * 板块接口
 */
export const sectionsApi = new RestApi({
  url: '/sections/',
  methods: ['list', 'show']
})

/**
 * 地域接口
 */
export const territoriesApi = new RestApi({
  url: '/territories/',
  methods: ['list', 'show']
})

/**
 * 报告类型接口
 */
export const reportTypesApi = new RestApi({
  url: '/report-types/',
  methods: ['list', 'show']
})

/**
 * 会计科目接口
 */
export const subjectsApi = new RestApi({
  url: '/subjects/',
  methods: ['list', 'show']
})

/**
 * 单季报接口
 * @param {object} params
 */
export function get_report (params) {
  return request.get('/reports/', { params })
}

/**
 * 报告期季报接口
 * @param {object} params
 */
export function get_xreport (params) {
  return request.get('/xreports/', { params })
}

/**
 * 比较信息接口
 * @param {object} params
 */
export function compare_stock (params) {
  return request.get('/compare/', { params })
}
