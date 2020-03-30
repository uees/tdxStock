export const NUMBER_TYPE = 1
export const STRING_TYPE = 2

export const DATA_TYPES = [
  { value: NUMBER_TYPE, label: '数值' },
  { value: STRING_TYPE, label: '字符串' }
]

const YUAN = 1
const WAN_YUAN = 2
const YI = 3
const GE = 4
const REN = 5
const CI = 6
const RATE = 7

export const UNIT_TYPES = [
  { value: YUAN, label: '元' },
  { value: WAN_YUAN, label: '万元' },
  { value: YI, label: '亿' },
  { value: GE, label: '个' },
  { value: REN, label: '人' },
  { value: CI, label: '次' },
  { value: RATE, label: '%' }
]

export const REPORT_TYPES = [
  { value: 'primary_indicator_sheet', label: '主要指标' },
  { value: 'consolidated_income_sheet', label: '利润表' },
  { value: 'consolidated_balance_sheet', label: '资产负债表' },
  { value: 'cash_flow_sheet', label: '现金流量表' }
]
