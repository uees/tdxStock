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
scrapy crawl report -a quarter=S0 -a crawl_mode=append -a report=balance
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
scrapy crawl stock_report -a quarter=S0 -a report=balance
```


### 一些命令

```
python manage.py update_last_report_date [--single]  // 更新最后报表日期
python manage.py clean_migrations
python manage.py seed_options
python manage.py seed_report_types
```

### API

#### `/api/stocks/` 获取股票列表和查看单个股票

**params**:

+ `name`
+ `code`

#### `/api/industries/` 行业信息接口

**params**:

+ `type`: value is `证监会分类` or `申万行业分类`


#### `/api/concepts/` 概念接口

**params**:

+ `omit`: 排除的字段， 例如 omit=stocks,id
+ `fileds`: 指定字段

#### `/api/sections/` 板块接口

**params**:

+ `omit`: 排除的字段， 例如 omit=stocks,id
+ `fileds`: 指定字段

#### `/api/territories/` 地域接口

**params**:

+ `omit`: 排除的字段， 例如 omit=stocks,id
+ `fileds`: 指定字段

#### `/api/report-types/` 报告类型接口

#### `/api/subjects/` 会计科目接口

#### `/api/reports/` 单季报接口

**params**:

+ `stock`: 股票ID
+ `report_type`: report_type ID
+ `quarter_str`: 季度，例如：2018-2

#### `/api/xreports/` 报告期季报接口

**params**:

+ `stock`: 股票ID
+ `report_type`: report_type ID
+ `quarter_str`: 季度，例如：2018-2

#### `/api/compare/` 比较信息接口

**params**:

+ `stocks`: 股票列表 ID 字符串， 逗号 `,` 号分隔，例如 stocks=25,36,456
+ `subject`: subject ID
+ `is_single`: 是否单季度报
+ `quarter`: 季度， such as 2018-2
