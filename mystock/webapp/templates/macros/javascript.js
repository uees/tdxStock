{% macro render_quarter_value(id, min_year, current_year, df, field, title, get_quarter_data) %}
var {{ id }} = echarts.init(document.getElementById('{{ id }}'));
{{ id }}.setOption({
  title: { text: '{{ title }}' },
  tooltip: {  // 提示框组件
    trigger: 'axis'
  },
  legend: {  // 图例组件
    data: ['1季度', '2季度', '3季度', '4季度']
  },
  toolbox: {  // 工具栏
    feature: {  // 各工具配置项
      saveAsImage: {}  // 保存为图片
    }
  },
  grid: {  // 直角坐标系内绘图网格
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true   // grid 区域是否包含坐标轴的刻度标签
  },
  xAxis: [   // x 轴
    {
      type: 'category',
      boundaryGap: false,
      data: [{% for year in range(min_year, current_year + 1) %}{{ year }}, {% endfor %}]
      }
    ],
  yAxis: {},
  series: [
    {
      name: '1季度',
      type: 'line',
      areaStyle: { normal: {} },
      data: [{% for year in range(min_year, current_year + 1) %}{{ get_quarter_data(df = df, field = field, year = year, quarter = 1) }}, {% endfor %}]
      },
  {
    name: '2季度',
    type: 'line',
    areaStyle: { normal: {} },
    data: [{% for year in range(min_year, current_year + 1) %}{{ get_quarter_data(df = df, field = field, year = year, quarter = 2) }}, {% endfor %}]
      },
  {
    name: '3季度',
    type: 'line',
    areaStyle: { normal: {} },
    data: [{% for year in range(min_year, current_year + 1) %}{{ get_quarter_data(df = df, field = field, year = year, quarter = 3) }}, {% endfor %}]
      },
  {
    name: '4季度',
    type: 'line',
    label: {
      normal: {
        show: true,
        position: 'top'
      }
    },
    areaStyle: { normal: {} },
    data: [{% for year in range(min_year, current_year + 1) %}{{ get_quarter_data(df = df, field = field, year = year, quarter = 4) }}, {% endfor %}]
      },
    ]
  });
{% endmacro %}

{%- macro render_quarter_ratio(id, min_year, current_year, df, field, title, get_quarter_data) %}
var {{ id }} = echarts.init(document.getElementById('{{ id }}'));
{{ id }}.setOption({
  title: { text: '{{ title }}' },
  tooltip: {  // 提示框组件
    trigger: 'axis'
  },
  legend: {  // 图例组件
    data: ['1季度', '2季度', '3季度', '4季度']
  },
  toolbox: {  // 工具栏
    feature: {  // 各工具配置项
      saveAsImage: {}  // 保存为图片
    }
  },
  grid: {  // 直角坐标系内绘图网格
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true   // grid 区域是否包含坐标轴的刻度标签
  },
  xAxis: [   // x 轴
    {
      type: 'category',
      boundaryGap: false,
      data: [{% for year in range(min_year, current_year + 1) %}{{ year }}, {% endfor %}]
      }
    ],
  yAxis: {},
  series: [
    {
      name: '1季度',
      type: 'line',
      data: [{% for year in range(min_year, current_year + 1) %}{{ get_quarter_data(df = df, field = field, year = year, quarter = 1) }}, {% endfor %}]
      },
  {
    name: '2季度',
    type: 'line',
    data: [{% for year in range(min_year, current_year + 1) %}{{ get_quarter_data(df = df, field = field, year = year, quarter = 2) }}, {% endfor %}]
      },
  {
    name: '3季度',
    type: 'line',
    data: [{% for year in range(min_year, current_year + 1) %}{{ get_quarter_data(df = df, field = field, year = year, quarter = 3) }}, {% endfor %}]
      },
  {
    name: '4季度',
    type: 'line',
    label: {
      normal: {
        show: true,
        position: 'top'
      }
    },
    areaStyle: { normal: {} },
    data: [{% for year in range(min_year, current_year + 1) %}{{ get_quarter_data(df = df, field = field, year = year, quarter = 4) }}, {% endfor %}]
      },
    ]
  });
{% endmacro %}
