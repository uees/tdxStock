#tdxStock

最终目标：打造一个分析系统。

#### 采集股票列表和股票信息

```
scrapy crawl stock_list

scrapy crawl stock_detail
```

#### 采集地域信息

```
scrapy crawl territory // 网易数据不更新
```

#### 采集概念信息

```
scrapy crawl concept  // 网易数据不更新
```

#### 采集行业信息

```
scrapy crawl industry_zjh  // 网易数据不更新

scrapy crawl industry_sw
```

#### 采集财报数据

```
scrapy crawl report -a quarter=S0 -a crawl_mode=append -a report=income
```

+ quarter:
    + S0 所有单季报
    + all 所有报告期报表
+ crawl_mode:
    + append 增量采集
    + all 全量采集
+ report:
    + balance 资产负债表
    + income 利润表
    + cash_flow 现金流量表
    + indicator 主要指标
+ start_year: 报表开始年
+ end_year: 报表截止年

如果发现有数据丢失，可以修复数据：

```
scrapy crawl stock_report -a quarter=S0 -a report=income
```


### 一些命令

```
update_last_report_date --singe  // 更新最后报表日期
clean_migrations
seed_options
seed_report_types
```
