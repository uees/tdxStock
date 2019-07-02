#tdxStock

最终目标：打造一个分析系统。

#### 采集股票列表

`scrapy crawl stock_list`
`scrapy crawl stock_detail`

#### 采集地域

`scrapy crawl territory`

#### 采集概念

`scrapy crawl concept`

#### 采集行业

`scrapy crawl industry_zjh`
`scrapy crawl industry_sw`

#### 采集财报数据

`scrapy crawl report -a quarter=S0 -a report=income -a crawl_mode=append`

+ quarter:
    + S0 所有单季报
    + all 所有报告期报表
+ report:
    + balance 资产负债表
    + income 利润表
    + cash_flow 现金流量表
    + indicator 主要指标
+ crawl_mode:
    + append 增量采集
    + all 全量采集

如果发现有数据丢失，可以修复数据：

`scrapy crawl stock_report -a quarter=S0 -a report=income`


### 一些命令

`update_last_report_date`

`clean_migrations`

`seed_options`

`seed_report_types`
