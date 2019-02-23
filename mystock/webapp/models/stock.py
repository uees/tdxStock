# -*- coding:utf-8 -*-
'''
@author: Wan
'''
from datetime import datetime
from webapp.extensions import db


class StockFlow(db.Document):
    '''买卖流水'''

    date = db.DateTimeField(default=datetime.utcnow)
    stock_code = db.StringField(default="")  # stock code
    stock_name = db.StringField(default="")  # stock name
    stock_price = db.FloatField(default=0)   # 单价
    stock_amount = db.FloatField(default=0)  # 卖负，买正, 基金份额可能为小数
    commission = db.FloatField(default=0)    # 佣金
    stamp_duty = db.FloatField(default=0)    # 印花税
    meta = {
        "indexes": ['stock_code'],
        'collection': 'stock_flow'
    }


class StockHold(db.Document):
    '''持仓'''

    stock_code = db.StringField(default="")  # stock code
    stock_name = db.StringField(default="")  # stock name
    stock_amount = db.FloatField(default=0)  # 卖负，买正, 基金份额可能为小数
    # 摊薄成本 = (∑买入金额 - ∑卖出金额 - ∑现金股息) / 持股数
    cost_of_average = db.FloatField(default=0)
    # 持仓成本 = ∑买入金额  / (∑买入数量 + ∑红股数量 + ∑拆股所增数量)
    cost_of_carry = db.FloatField(default=0)
    meta = {
        "indexes": ['stock_code'],
        'collection': 'stock_hold'
    }


class CashFlow(db.Document):
    '''现金流水'''

    date = db.DateTimeField(default=datetime.utcnow)
    money = db.FloatField(default=0)
    note = db.StringField(max_length=250, default="")
    meta = {
        'collection': 'cash_flow'
    }


#
# 投资参考数据
#
class Distribution(db.Document):
    ''' 分配预案 '''
    __tsfunc__ = 'profit_data'

    code = db.StringField(default="")  # stock code
    name = db.StringField(default="")  # stock name
    year = db.IntField()
    report_date = db.DateTimeField()  # 公布日期
    divi = db.FloatField()  # 分红金额（每10股）
    shares = db.FloatField()  # 转增和送股数（每10股）
    meta = {
        'collection': 'ts_distribution_plan',
        'indexes': ['code'],
    }


class Forecast(db.Document):
    ''' 业绩预告'''
    __tsfunc__ = 'forecast_data'

    code = db.StringField(default="")  # stock code
    name = db.StringField(default="")  # stock name
    year = db.IntField()
    quarter = db.IntField()  # 季度 :1、2、3、4，只能输入这4个季度
    type = db.StringField(default="")  # 业绩变动类型【预增、预亏等】
    report_date = db.DateTimeField()  # 公布日期
    pre_eps = db.FloatField()  # 上年同期每股收益
    range = db.DynamicField()  # 业绩变动范围
    meta = {
        'collection': 'ts_forecast_data',
        'indexes': ['code'],
    }


class Xsg(db.Document):
    ''' 限售股解禁 2010年以后的数据 '''
    __tsfunc__ = 'xsg_data'

    year = db.IntField()  # 年度 e.g:2014
    month = db.IntField()  # 解禁月份
    code = db.StringField(default="")  # stock code
    name = db.StringField(default="")  # stock name
    date = db.DateTimeField()  # 解禁日期
    count = db.FloatField()  # 解禁数量（万股）
    ratio = db.FloatField()  # 占总盘比率
    meta = {
        'collection': 'ts_xsg_data',
        'indexes': ['code'],
    }


class FundHolding(db.Document):
    ''' 基金持股 '''
    __tsfunc__ = 'fund_holdings'

    year = db.IntField()  # 年度 e.g:2014
    quarter = db.IntField()  # 季度 :1、2、3、4
    code = db.StringField(default="")  # stock code
    name = db.StringField(default="")  # stock name
    date = db.DateTimeField()  # 报告日期
    nums = db.IntField()  # 基金家数
    nlast = db.IntField()  # 与上期相比（增加或减少了）
    count = db.FloatField()  # 基金持股数（万股）
    clast = db.FloatField()  # 基金持股数与上期相比
    amount = db.FloatField()  # 基金持股市值
    ratio = db.FloatField()  # 占流通盘比率
    meta = {
        'collection': 'ts_fund_holdings',
        'indexes': ['code'],
    }


class ShMargin(db.Document):
    '''沪市融资融券汇总数据
    本日融资融券余额＝本日融资余额＋本日融券余量金额
    本日融资余额＝前日融资余额＋本日融资买入额－本日融资偿还额；
    本日融资偿还额＝本日直接还款额＋本日卖券还款额＋本日融资强制平仓额＋本日融资正权益调整－本日融资负权益调整；
    本日融券余量=前日融券余量+本日融券卖出数量-本日融券偿还量；
    本日融券偿还量＝本日买券还券量＋本日直接还券量＋本日融券强制平仓量＋本日融券正权益调整－本日融券负权益调整－本日余券应划转量；
    融券单位：股（标的证券为股票）/份（标的证券为基金）/手（标的证券为债券）。
    明细信息中仅包含当前融资融券标的证券的相关数据，汇总信息中包含被调出标的证券范围的证券的余额余量相关数据。
    '''
    __tsfunc__ = 'sh_margins'

    opDate = db.DateTimeField()  # 信用交易日期
    rzye = db.FloatField()  # 本日融资余额(元)
    rzmre = db.FloatField()  # 本日融资买入额(元)
    rqyl = db.FloatField()  # 本日融券余量
    rqylje = db.FloatField()  # 本日融券余量金额(元)
    rqmcl = db.FloatField()  # 本日融券卖出量
    rzrqjyzl = db.FloatField()  # 本日融资融券余额(元)
    meta = {
        'collection': 'ts_sh_margins'
    }


class ShMarginDetail(db.Document):
    '''沪市融资融券明细数据'''
    __tsfunc__ = 'sh_margin_details'

    opDate = db.DateTimeField()  # 信用交易日期
    stockCode = db.StringField(default="")  # 标的证券代码
    securityAbbr = db.StringField(default="")  # 标的证券简称
    rzye = db.FloatField()  # 本日融资余额(元)
    rzmre = db.FloatField()  # 本日融资买入额(元)
    rzche = db.FloatField()  # 本日融资偿还额(元)
    rqyl = db.FloatField()  # 本日融券余量
    rqmcl = db.FloatField()  # 本日融券卖出量
    rqchl = db.FloatField()  # 本日融券偿还量
    meta = {
        'collection': 'ts_sh_margin_details',
        'indexes': ['stockCode'],
    }


class SzMargin(db.Document):
    '''深市融资融券汇总数据
    本日融资余额(元)=前日融资余额＋本日融资买入-本日融资偿还额
    本日融券余量(股)=前日融券余量＋本日融券卖出量-本日融券买入量-本日现券偿还量
    本日融券余额(元)=本日融券余量×本日收盘价
    本日融资融券余额(元)=本日融资余额＋本日融券余额；
    '''
    __tsfunc__ = 'sz_margins'

    opDate = db.DateTimeField()  # 信用交易日期
    rzmre = db.FloatField()  # 融资买入额(元)
    rzye = db.FloatField()  # 融资余额(元)
    rqmcl = db.FloatField()  # 融券卖出量
    rqyl = db.FloatField()  # 融券余量
    rqye = db.FloatField()  # 融券余额(元)
    rzrqye = db.FloatField()  # 融资融券余额(元)
    meta = {
        'collection': 'ts_sz_margins',
    }


class SzMarginDetail(db.Document):
    '''深市融资融券明细数据'''
    __tsfunc__ = 'sz_margin_details'

    stockCode = db.StringField(default="")
    securityAbbr = db.StringField(default="")
    rzmre = db.FloatField()  # 融资买入额(元)
    rzye = db.FloatField()  # 融资余额(元)
    rqmcl = db.FloatField()  # 融券卖出量
    rqyl = db.FloatField()  # 融券余量
    rqye = db.FloatField()  # 融券余额(元)
    rzrqye = db.FloatField()  # 融资融券余额(元)
    opDate = db.DateTimeField()  # 信用交易日期
    meta = {
        'collection': 'ts_sz_margin_details',
        'indexes': ['stockCode'],
    }


#
# 股票分类数据
#
class IndustryClassified(db.Document):
    '''行业分类'''
    __tsfunc__ = 'get_industry_classified'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    c_name = db.StringField(default="")  # 行业名称
    meta = {
        'collection': 'ts_industry_classified'
    }


class ConceptClassified(db.Document):
    '''概念分类'''
    __tsfunc__ = "get_concept_classified"

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    c_name = db.StringField(default="")  # 概念名称
    meta = {
        'collection': 'ts_concept_classified',
        'indexes': ['code', 'c_name'],
    }


class AreaClassified(db.Document):
    '''地域分类'''
    __tsfunc__ = "get_area_classified"

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    area = db.StringField(default="")  # 地域名称
    meta = {
        'collection': 'ts_area_classified'
    }


class SmeClassified(db.Document):
    '''中小板分类'''
    __tsfunc__ = 'get_sme_classified'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    meta = {
        'collection': 'ts_sme_classified'
    }


class GemClassified(db.Document):
    '''创业板分类'''
    __tsfunc__ = 'get_gem_classified'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    meta = {
        'collection': 'ts_gem_classified'
    }


class StClassified(db.Document):
    '''风险警示板分类'''
    __tsfunc__ = 'get_st_classified'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    meta = {
        'collection': 'ts_st_classified'
    }


class Hs300(db.Document):
    '''沪深300分类'''
    __tsfunc__ = 'get_hs300s'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    date = db.StringField(default="")  # 日期
    weight = db.FloatField()  # 权重
    meta = {
        'collection': 'ts_hs300s'
    }


class Sz50(db.Document):
    '''上证50成份股'''
    __tsfunc__ = 'get_sz50s'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    meta = {
        'collection': 'ts_sz50s'
    }


class Zz500(db.Document):
    '''中证500成份股'''
    __tsfunc__ = 'get_zz500s'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    date = db.StringField(default="")  # 日期
    weight = db.FloatField()  # 权重
    meta = {
        'collection': 'ts_zz500s'
    }


class Terminated(db.Document):
    '''终止上市股票列表 '''
    __tsfunc__ = 'get_terminated'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    oDate = db.StringField(default="")  # 上市日期
    tDate = db.StringField(default="")  # 终止上市日期
    meta = {
        'collection': 'ts_terminated'
    }


class Suspended(db.Document):
    '''暂停上市股票列表'''
    __tsfunc__ = 'get_suspended'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    oDate = db.StringField(default="")  # 上市日期
    tDate = db.StringField(default="")  # 暂停上市日期
    meta = {
        'collection': 'ts_suspended'
    }


#
# 基本面数据
#
class StockBasic(db.Document):
    """ 股票列表
    沪深上市公司基本情况"""
    __tsfunc__ = 'get_stock_basics'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    industry = db.StringField(default="")  # 所属行业
    area = db.StringField(default="")  # 所属地区
    pe = db.FloatField()  # 市盈率
    outstanding = db.FloatField()  # 流通股本
    totals = db.FloatField()  # 总股本(万)
    totalAssets = db.FloatField()  # 总资产(万)
    liquidAssets = db.FloatField()  # 流动资产
    fixedAssets = db.FloatField()  # 固定资产
    reserved = db.FloatField()  # 公积金
    reservedPerShare = db.FloatField()  # 每股公积金
    esp = db.FloatField()  # 每股收益
    bvps = db.FloatField()  # 每股净资
    pb = db.FloatField()  # 市净率
    timeToMarket = db.IntField()  # 上市日期
    undp = db.FloatField()  # 未分利润
    perundp = db.FloatField()  # 每股未分配
    rev = db.FloatField()  # 收入同比(%)
    profit = db.FloatField()  # 利润同比(%)
    gpr = db.FloatField()  # 毛利率(%)
    npr = db.FloatField()  # 净利润率(%)
    holders = db.FloatField()  # 股东人数
    meta = {
        'collection': 'ts_stock_basics',
        'indexes': ['code', 'name', 'industry', 'area']
    }


class ReportData(db.Document):
    """业绩报告(主表)
    按年度、季度的业绩报表数据"""
    __tsfunc__ = 'get_report_data'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    eps = db.FloatField()  # 每股收益
    eps_yoy = db.FloatField()  # 每股收益同比(%)
    bvps = db.FloatField()  # 每股净资产
    roe = db.FloatField()  # 净资产收益率(%)
    epcf = db.FloatField()  # 每股现金流量(元)
    net_profits = db.FloatField()  # 净利润(万元)
    profits_yoy = db.FloatField()  # 净利润同比(%)
    distrib = db.DynamicField()  # 分配方案 FloatField
    report_date = db.StringField()  # 发布日期 02-29
    year = db.IntField()  # 年度
    quarter = db.IntField()  # 季度
    meta = {
        'collection': 'ts_report_data',
        'indexes': ['code'],
        'ordering': ['year', 'quarter']
    }


class ProfitData(db.Document):
    """盈利能力
    按年度、季度的盈利能力数据"""
    __tsfunc__ = 'get_profit_data'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    roe = db.FloatField()  # 净资产收益率(%)
    net_profit_ratio = db.FloatField()  # 净利率(%)
    gross_profit_rate = db.FloatField()  # 毛利率(%)
    net_profits = db.FloatField()  # 净利润(万元)
    eps = db.FloatField()  # 每股收益
    business_income = db.FloatField()  # 营业收入(百万元)
    bips = db.FloatField()  # 每股主营业务收入(元)
    year = db.IntField()  # 年度
    quarter = db.IntField()  # 季度
    meta = {
        'collection': 'ts_profit_data',
        'indexes': ['code'],
        'ordering': ['year', 'quarter']
    }


class OperationData(db.Document):
    """营运能力
    按年度、季度的营运能力数据"""
    __tsfunc__ = 'get_operation_data'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    arturnover = db.FloatField()  # 应收账款周转率(次)
    arturndays = db.FloatField()  # 应收账款周转天数(天)
    inventory_turnover = db.FloatField()  # 存货周转率(次)
    inventory_days = db.FloatField()  # 存货周转天数(天)
    currentasset_turnover = db.FloatField()  # 流动资产周转率(次)
    currentasset_days = db.FloatField()  # 流动资产周转天数(天)
    year = db.IntField()  # 年度
    quarter = db.IntField()  # 季度
    meta = {
        'collection': 'ts_operation_data',
        'indexes': ['code'],
        'ordering': ['year', 'quarter']
    }


class GrowthData(db.Document):
    '''成长能力
    按年度、季度获取成长能力数据'''
    __tsfunc__ = 'get_growth_data'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    mbrg = db.FloatField()  # 主营业务收入增长率(%)
    nprg = db.FloatField()  # 净利润增长率(%)
    nav = db.FloatField()  # 净资产增长率
    targ = db.FloatField()  # 总资产增长率
    epsg = db.FloatField()  # 每股收益增长率
    seg = db.FloatField()  # 股东权益增长率
    year = db.IntField()  # 年度
    quarter = db.IntField()  # 季度
    meta = {
        'collection': 'ts_growth_data',
        'indexes': ['code'],
        'ordering': ['year', 'quarter']
    }


class DebtpayingData(db.Document):
    '''偿债能力
    按年度、季度获取偿债能力数据'''
    __tsfunc__ = 'get_debtpaying_data'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    currentratio = db.DynamicField()  # 流动比率  String
    quickratio = db.DynamicField()  # 速动比率  String
    cashratio = db.DynamicField()  # 现金比率  String
    icratio = db.DynamicField()  # 利息支付倍数  String
    sheqratio = db.DynamicField()  # 股东权益比率  String
    adratio = db.DynamicField()  # 股东权益增长率  String
    year = db.IntField()  # 年度
    quarter = db.IntField()  # 季度
    meta = {
        'collection': 'ts_debtpaying_data',
        'indexes': ['code'],
        'ordering': ['year', 'quarter']
    }


class CashflowData(db.Document):
    '''现金流量
    按年度、季度获取现金流量数据'''
    __tsfunc__ = 'get_cashflow_data'

    code = db.StringField(default="")  # 代码
    name = db.StringField(default="")  # 名称
    cf_sales = db.FloatField()  # 经营现金净流量对销售收入比率
    rateofreturn = db.FloatField()  # 资产的经营现金流量回报率
    cf_nm = db.FloatField()  # 经营现金净流量与净利润的比率
    cf_liabilities = db.FloatField()  # 经营现金净流量对负债比率
    cashflowratio = db.FloatField()  # 现金流量比率
    year = db.IntField()  # 年度
    quarter = db.IntField()  # 季度
    meta = {
        'collection': 'ts_cashflow_data',
        'indexes': ['code'],
        'ordering': ['year', 'quarter']
    }


#
# 宏观经济数据
#
class DepositRate(db.Document):
    '''存款利率'''
    __tsfunc__ = 'get_deposit_rate'

    date = db.DateTimeField()  # 变动日期
    deposit_type = db.StringField(default="")  # 存款种类
    rate = db.StringField()  # 利率（%）
    meta = {
        'collection': 'ts_deposit_rate'
    }


class LoanRate(db.Document):
    '''贷款利率'''
    __tsfunc__ = 'get_loan_rate'

    date = db.DateTimeField()  # 执行日期
    loan_type = db.StringField(default="")  # 贷款种类
    rate = db.StringField()  # 利率（%）
    meta = {
        'collection': 'ts_loan_rate'
    }


class Rrr(db.Document):
    '''存款准备金率'''
    __tsfunc__ = 'get_rrr'

    date = db.DateTimeField()  # 变动日期
    before = db.StringField()  # 调整前存款准备金率(%)
    now = db.StringField()  # 调整后存款准备金率(%)
    changed = db.StringField()  # 调整幅度(%)
    meta = {
        'collection': 'ts_rrr'
    }


class MoneySupply(db.Document):
    '''货币供应量'''
    __tsfunc__ = 'get_money_supply'

    month = db.StringField()  # 统计时间 '2014.12'
    m2 = db.StringField()  # 货币和准货币（广义货币M2）(亿元)
    m2_yoy = db.StringField()  # 货币和准货币（广义货币M2）同比增长(%)
    m1 = db.StringField()  # 货币(狭义货币M1)(亿元)
    m1_yoy = db.StringField()  # 货币(狭义货币M1)同比增长(%)
    m0 = db.StringField()  # 流通中现金(M0)(亿元)
    m0_yoy = db.StringField()  # 流通中现金(M0)同比增长(%)
    cd = db.StringField()  # 活期存款(亿元)
    cd_yoy = db.StringField()  # 活期存款同比增长(%)
    qm = db.StringField()  # 准货币(亿元)
    qm_yoy = db.StringField()  # 准货币同比增长(%)
    ftd = db.StringField()  # 定期存款(亿元)
    ftd_yoy = db.StringField()  # 定期存款同比增长(%)
    sd = db.StringField()  # 储蓄存款(亿元)
    sd_yoy = db.StringField()  # 储蓄存款同比增长(%)
    rests = db.StringField()  # 其他存款(亿元)
    rests_yoy = db.StringField()  # 其他存款同比增长(%)
    meta = {
        'collection': 'ts_money_supply'
    }


class MoneySupplyBal(db.Document):
    '''货币供应量(年底余额)'''
    __tsfunc__ = 'get_money_supply_bal'

    year = db.StringField()  # 统计年度
    m2 = db.StringField()  # 货币和准货币（广义货币M2）(亿元)
    m1 = db.StringField()  # 货币(狭义货币M1)(亿元)
    m0 = db.StringField()  # 流通中现金(M0)(亿元)
    cd = db.StringField()  # 活期存款(亿元)
    qm = db.StringField()  # 准货币(亿元)
    ftd = db.StringField()  # 定期存款(亿元)
    sd = db.StringField()  # 储蓄存款(亿元)
    rests = db.StringField()  # 其他存款(亿元)
    meta = {
        'collection': 'ts_money_supply_bal'
    }


class GdpYear(db.Document):
    ''' 国内生产总值(年度) '''
    __tsfunc__ = 'get_gdp_year'

    year = db.IntField()  # 统计年度
    gdp = db.FloatField()  # 国内生产总值(亿元)
    pc_gdp = db.FloatField()  # 人均国内生产总值(元)
    gnp = db.FloatField()  # 国民生产总值(亿元)
    pi = db.FloatField()  # 第一产业(亿元)
    si = db.FloatField()  # 第二产业(亿元)
    industry = db.FloatField()  # 工业(亿元)
    cons_industry = db.FloatField()  # 建筑业(亿元)
    ti = db.FloatField()  # 第三产业(亿元)
    trans_industry = db.FloatField()  # 交通运输仓储邮电通信业(亿元)
    lbdy = db.FloatField()  # 批发零售贸易及餐饮业(亿元)
    meta = {
        'collection': 'ts_gdp_year'
    }


class GdpQuarter(db.Document):
    '''国内生产总值(季度)'''
    __tsfunc__ = 'get_gdp_quarter'

    year = db.IntField()  # 统计年度
    quarter = db.IntField()  # 季度
    gdp = db.FloatField()  # 国内生产总值(亿元)
    gdp_yoy = db.FloatField()  # 国内生产总值同比增长(%)
    pi = db.FloatField()  # 第一产业增加值(亿元)
    pi_yoy = db.FloatField()  # 第一产业增加值同比增长(%)
    si = db.FloatField()  # 第二产业增加值(亿元)
    si_yoy = db.FloatField()  # 第二产业增加值同比增长(%)
    ti = db.FloatField()  # 第三产业增加值(亿元)
    ti_yoy = db.FloatField()  # 第三产业增加值同比增长(%)
    meta = {
        'collection': 'ts_gdp_quarter'
    }


class GdpFor(db.Document):
    '''三大需求对GDP贡献'''
    __tsfunc__ = 'get_gdp_for'

    year = db.IntField()  # 统计年度
    end_for = db.FloatField()  # 最终消费支出贡献率(%)
    for_rate = db.FloatField()  # 最终消费支出拉动(百分点)
    asset_for = db.FloatField()  # 资本形成总额贡献率(%)
    asset_rate = db.FloatField()  # 资本形成总额拉动(百分点)
    goods_for = db.FloatField()  # 货物和服务净出口贡献率(%)
    goods_rate = db.FloatField()  # 货物和服务净出口拉动(百分点)
    meta = {
        'collection': 'ts_gdp_for'
    }


class GdpPull(db.Document):
    '''三大产业对GDP拉动'''
    __tsfunc__ = 'get_gdp_pull'

    year = db.IntField()  # 统计年度
    gdp_yoy = db.FloatField()  # 国内生产总值同比增长(%)
    pi = db.FloatField()  # 第一产业拉动率(%)
    si = db.FloatField()  # 第二产业拉动率(%)
    industry = db.FloatField()  # 其中工业拉动(%)
    ti = db.FloatField()  # 第三产业拉动率(%)
    meta = {
        'collection': 'ts_gdp_pull'
    }


class GdpContrib(db.Document):
    '''三大产业贡献率'''
    __tsfunc__ = 'get_gdp_contrib'

    year = db.IntField()  # 统计年度
    gdp_yoy = db.FloatField()  # 国内生产总值
    pi = db.FloatField()  # 第一产业献率(%)
    si = db.FloatField()  # 第二产业献率(%)
    industry = db.FloatField()  # 其中工业献率(%)
    ti = db.FloatField()  # 第三产业献率(%)
    meta = {
        'collection': 'ts_gdp_contrib'
    }


class Cpi(db.Document):
    '''居民消费价格指数'''
    __tsfunc__ = 'get_cpi'

    month = db.StringField()  # 统计月份
    cpi = db.FloatField()  # 价格指数
    meta = {
        'collection': 'ts_cpi'
    }


class Ppi(db.Document):
    '''工业品出厂价格指数'''
    __tsfunc__ = 'get_ppi'

    month = db.StringField()  # 统计月份
    ppiip = db.FloatField()  # 工业品出厂价格指数
    ppi = db.FloatField()  # 生产资料价格指数
    qm = db.FloatField()  # 采掘工业价格指数
    rmi = db.FloatField()  # 原材料工业价格指数
    pi = db.FloatField()  # 加工工业价格指数
    cg = db.FloatField()  # 生活资料价格指数
    food = db.FloatField()  # 食品类价格指数
    clothing = db.FloatField()  # 衣着类价格指数
    roeu = db.FloatField()  # 一般日用品价格指数
    dcg = db.FloatField()  # 耐用消费品价格指数
    meta = {
        'collection': 'ts_ppi'
    }
