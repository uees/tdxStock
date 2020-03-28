/**
 * 行业
 */
export function Industry () {
  return {
    id: undefined,
    parent: undefined,
    name: undefined,
    level: undefined,
    type: undefined,
    memo: undefined,
    stocks: []
  }
}

/**
 * 概念
 */
export function Concept () {
  return {
    id: undefined,
    name: undefined,
    memo: undefined,
    stocks: []
  }
}

/**
 * 地域
 */
export function Territory () {
  return {
    id: undefined,
    name: undefined,
    stocks: []
  }
}

/**
 * 板块
 */
export function Section () {
  return {
    id: undefined,
    name: undefined,
    memo: undefined,
    stocks: []
  }
}

/**
 * 股票
 */
export function Stock () {
  return {
    id: undefined,
    name: undefined,
    code: undefined,
    exchange_code: undefined, // 交易市场, 例如，XSHG- 上海证券交易所；XSHE - 深圳证券交易所
    company_name: undefined,
    former_name: undefined, // 曾用名
    actual_controller: undefined, // 实际控制人
    ownership_nature: undefined, // 所有制性质名称
    primary_business: undefined, // 主营业务
    company_profile: undefined, // 公司简介
    operating_scope: undefined, // 经营范围
    chairman: undefined, // 董事长
    legal_person: undefined, // 法人代表
    general_manager: undefined, // 总经理
    secretary: undefined, // 董秘
    found_date: undefined, // 成立日期
    registered_capital: undefined, // 注册资本(元)
    employees_num: undefined, // 员工人数
    management_num: undefined, // 管理层人数
    listing_date: undefined, // 上市日期
    distribution_amount: undefined, // 发行量
    first_price: undefined, // 发行价格
    raise_money: undefined, // 募集资金
    first_pe: undefined, // 发行市盈率
    online_success_rate: undefined, // 网上中签率
    tel: undefined, // 联系电话
    zip_code: undefined, // 邮政编码
    fax: undefined, // 传真
    email: undefined, // 电子邮箱
    homepage: undefined, // 公司网址
    registered_address: undefined, // 注册地址
    office_address: undefined, // 办公地址
    updated_at: undefined, // 更新时间
    territory: undefined,
    metas: {
      primary_indicator_sheet: {
        last_report_date: undefined,
        last_all_report_date: undefined,
        quarter_list: [],
        all_list: []
      },
      consolidated_balance_sheet: {
        last_report_date: undefined,
        last_all_report_date: undefined,
        quarter_list: [],
        all_list: []
      },
      consolidated_income_sheet: {
        last_report_date: undefined,
        last_all_report_date: undefined,
        quarter_list: [],
        all_list: []
      },
      cash_flow_sheet: {
        last_report_date: undefined,
        last_all_report_date: undefined,
        quarter_list: [],
        all_list: []
      }
    }
  }
}

/**
 * 财报类型
 */
export function ReportType () {
  return {
    id: undefined,
    name: undefined,
    slug: undefined,
    memo: undefined
  }
}

/**
 * 会计科目
 */
export function AccountingSubject () {
  return {
    id: undefined,
    report_type: undefined,
    name: undefined,
    slug: undefined,
    parent: undefined,
    memo: undefined
  }
}

/**
 * 财报
 */
export function Report () {
  return {
    id: undefined,
    items: [],
    stock: undefined,
    report_type: undefined,
    name: undefined,
    year: undefined,
    quarter: undefined,
    report_date: undefined
  }
}

/**
 * 财报项目
 */
export function ReportItem () {
  return {
    id: undefined,
    value_number: undefined,
    value: undefined,
    value_type: undefined,
    value_unit: undefined,
    subject_id: undefined,
    stock: undefined,
    quarter: undefined
  }
}
