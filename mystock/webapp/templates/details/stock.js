{%- from "macros/javascript.js" import render_quarter_ratio, render_quarter_value %}
$(function () {
{%- if report_data is not none %}
  {%- set min_year = report_data['year'].drop_duplicates().iat[0] %}
  {{ render_quarter_value('net_profits', min_year, current_year, report_data, 'net_profits', '净利润(万元)', get_quarter_data) }}
  {{ render_quarter_ratio('profits_yoy', min_year, current_year, report_data, 'profits_yoy', '净利润同比(%)', get_quarter_data) }}
  {{ render_quarter_value('eps', min_year, current_year, report_data, 'eps', '每股收益', get_quarter_data) }}
  {{ render_quarter_ratio('eps_yoy', min_year, current_year, report_data, 'eps_yoy', '每股收益同比(%)', get_quarter_data) }}
  {{ render_quarter_value('bvps', min_year, current_year, report_data, 'bvps', '每股净资产', get_quarter_data) }}
  {{ render_quarter_value('epcf', min_year, current_year, report_data, 'epcf', '每股现金流量(元)', get_quarter_data) }}
  {%- if profit_data is not none %}
  {{ render_quarter_ratio('net_profit_ratio', min_year, current_year, profit_data, 'net_profit_ratio', '净利率(%)', get_quarter_data) }}
  {{ render_quarter_ratio('gross_profit_rate', min_year, current_year, profit_data, 'gross_profit_rate', '毛利率(%)', get_quarter_data) }}
  {{ render_quarter_value('business_income', min_year, current_year, profit_data, 'business_income', '营业收入(百万元)', get_quarter_data) }}
  {{ render_quarter_value('bips', min_year, current_year, profit_data, 'bips', '每股主营业务收入(元)', get_quarter_data) }}
  {%- endif %}
  {%- if operation_data is not none %}
  {{ render_quarter_value('arturnover', min_year, current_year, operation_data, 'arturnover', '应收账款周转率(次)', get_quarter_data) }}
  {{ render_quarter_value('arturndays', min_year, current_year, operation_data, 'arturndays', '应收账款周转天数(天)', get_quarter_data) }}
  {{ render_quarter_value('inventory_turnover', min_year, current_year, operation_data, 'inventory_turnover', '存货周转率(次)', get_quarter_data) }}
  {{ render_quarter_value('inventory_days', min_year, current_year, operation_data, 'inventory_days', '存货周转天数(天)', get_quarter_data) }}
  {{ render_quarter_value('currentasset_turnover', min_year, current_year, operation_data, 'currentasset_turnover', '流动资产周转率(次)', get_quarter_data) }}
  {{ render_quarter_value('currentasset_days', min_year, current_year, operation_data, 'currentasset_days', '流动资产周转天数(天)', get_quarter_data) }}
  {%- endif %}
  {%- if debtpaying_data is not none %}
  {{ render_quarter_ratio('currentratio', min_year, current_year, debtpaying_data, 'currentratio', '流动比率', get_quarter_data) }}
  {{ render_quarter_ratio('quickratio', min_year, current_year, debtpaying_data, 'quickratio', '速动比率', get_quarter_data) }}
  {{ render_quarter_ratio('cashratio', min_year, current_year, debtpaying_data, 'cashratio', '现金比率', get_quarter_data) }}
  {{ render_quarter_ratio('icratio', min_year, current_year, debtpaying_data, 'icratio', '利息支付倍数', get_quarter_data) }}
  {{ render_quarter_ratio('sheqratio', min_year, current_year, debtpaying_data, 'sheqratio', '股东权益比率', get_quarter_data) }}
  {{ render_quarter_ratio('adratio', min_year, current_year, debtpaying_data, 'adratio', '股东权益增长率', get_quarter_data) }}
  {%- endif %}
  {%- if cashflow_data is not none %}
  {{ render_quarter_ratio('cf_sales', min_year, current_year, cashflow_data, 'cf_sales', '经营现金净流量对销售收入比率', get_quarter_data) }}
  {{ render_quarter_ratio('rateofreturn', min_year, current_year, cashflow_data, 'rateofreturn', '资产的经营现金流量回报率', get_quarter_data) }}
  {{ render_quarter_ratio('cf_nm', min_year, current_year, cashflow_data, 'cf_nm', '经营现金净流量与净利润的比率', get_quarter_data) }}
  {{ render_quarter_ratio('cf_liabilities', min_year, current_year, cashflow_data, 'cf_liabilities', '经营现金净流量对负债比率', get_quarter_data) }}
  {{ render_quarter_ratio('cashflowratio', min_year, current_year, cashflow_data, 'cashflowratio', '现金流量比率', get_quarter_data) }}
  {%- endif %}
{%- endif %}
});