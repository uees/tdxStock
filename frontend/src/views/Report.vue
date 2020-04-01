<template>
  <el-row>
    <el-col :span="24">
      <h1>{{stock.name}} {{stock.code}}</h1>

      <div class="xueqiu-data"
           style="margin-bottom: 24px">
        <a :href="`https://xueqiu.com/S/${stock.code}`"
           target="_blank">K线</a>
        <a :href="`https://xueqiu.com/snowman/S/${stock.code}/detail#/ZYCWZB`"
           target="_blank"
           class="element2">主要指标</a>
        <a :href="`https://xueqiu.com/snowman/S/${stock.code}/detail#/GSLRB`"
           target="_blank"
           class="element2">利润表</a>
        <a :href="`https://xueqiu.com/snowman/S/${stock.code}/detail#/ZCFZB`"
           target="_blank"
           class="element2">资产负债表</a>
        <a :href="`https://xueqiu.com/snowman/S/${stock.code}/detail#/XJLLB`"
           target="_blank"
           class="element2">现金流量表</a>
      </div>

      <div class="report-type-content">
        <el-select v-model="reportType"
                   placeholder="请选择报表类型">
          <el-option v-for="item in reportTypes"
                     :key="item.slug"
                     :label="item.name"
                     :value="item.slug" />
        </el-select>

        <el-cascader v-model="subjectsValue"
                     :options="accountingSubjects[reportType]"
                     :props="Object.assign({}, props, { checkStrictly: true })"
                     class="element2"
                     @change="handleChangeSubject" />
      </div>
    </el-col>

    <el-col :span="24"
            style="margin-top: 24px">
      <el-select v-model="quarter"
                 clearable
                 @clear="clearQuarter"
                 placeholder="季度报">
        <el-option label="一季报"
                   value="1" />
        <el-option label="半年报"
                   value="2" />
        <el-option label="三季报"
                   value="3" />
        <el-option label="年报"
                   value="4" />
      </el-select>

      <el-switch v-model="is_single"
                 class="element2"
                 active-text="单季度" />

      <div class="submit-content">
        <el-button type="primary"
                   @click="handleCompare">
          查看趋势
        </el-button>
        <el-button type="info"
                   class="element2"
                   @click="handleDownload">
          下载数据
        </el-button>
      </div>
    </el-col>

    <el-col :span="24">
      <div id="chart-container" />
    </el-col>
  </el-row>
</template>

<script>
import { mapState } from 'vuex'
import { Chart } from '@antv/g2'
import { compare_stock, stocksApi } from '../api'

export default {
  name: 'Report',
  props: ['id'],
  data () {
    return {
      quarter: '',
      is_single: false,
      reportType: undefined,
      subjectsValue: [],
      props: {
        value: 'id',
        label: 'name',
        children: 'children'
      },
      chart: undefined,
      compareData: [],
      subject: undefined,
      stock: undefined
    }
  },
  computed: {
    ...mapState('basedata', {
      reportTypes: state => state.reportTypes.data,
      accountingSubjects: state => state.accountingSubjects
    }),
    subject_id: function () {
      return this.subjectsValue[this.subjectsValue.length - 1]
    },
    filename: function () {
      let result = `${this.reportType}-${this.subject.name}`

      if (this.stock) {
        result = `${this.stock.name}-${result}`
      }

      return result
    }
  },
  mounted() {
    this.getStock()
  },
  methods: {
    async getStock () {
      const stock = await stocksApi.show(this.id)
      this.stock = stock
    },
    handleDownload () {
      import('../vendor/Export2Excel').then(excel => {
        const tHeader = ['公司', '季度', '数据', 'Str', 'DataType']
        const data = this.compareData2json()
        excel.export_json_to_excel({
          header: tHeader,
          data,
          filename: this.filename,
          autoWidth: true,
          bookType: 'xlsx'
        })
        this.downloadLoading = false
      })
    },
    compareData2json () {
      return this.compareData.map(item => {
        return [
          item.stock,
          new Date(item.quarter.replace(/-/g,'/')),
          item.value_number,
          item.value,
          item.value_type
        ]
      })
    },
    handleChangeSubject (value) {
      let subjects = this.accountingSubjects[this.reportType]
      let subject
      for (const id of value) {
        subject = subjects.find(subject => subject.id === id)
        subjects = subject.children
      }
      this.subject = subject
    },
    handleCompare () {
      if (this.subject_id) {
        compare_stock({
          stocks: this.id,
          subject: this.subject_id,
          is_single: this.is_single,
          quarter: this.quarter
        }).then(response => {
          this.compareData = response.map(item => {
            if (item.value_number === null) {
              item.value_number = 0
            }
            return item
          })
          this.drawChart()
        })
      } else {
        window.alert('没选择股票，或者没选择会计科目')
      }
    },
    clearQuarter () {
      this.quarter = ''
    },
    drawChart () {
      this.chart && this.chart.destroy()
      // Step 1: 创建 Chart 对象
      this.chart = new Chart({
        container: 'chart-container',
        width: 1200,
        height: 600
      })

      // Step 2: 载入数据源
      this.chart.data(this.compareData)

      // 度量定义
      this.chart.scale({
        value_number: {
          type: 'linear', // 线性度量
          formatter: function(value, index) {
            if (value) {
              return Number(value).toLocaleString()
            }
            return value
          }
        }
      })

      // Step 3：创建图形语法，绘制柱状图
      this.chart.point().position('quarter*value_number').color('stock')
      this.chart.line().position('quarter*value_number').color('stock')

      // Step 4: 渲染图表
      this.chart.render()
    }
  }
}
</script>

<style lang="scss" scoped>
.report-type-content {
  margin-bottom: 24px;
}

.element2 {
  margin-left: 12px;
}

.submit-content {
  margin-top: 24px;
}
</style>
