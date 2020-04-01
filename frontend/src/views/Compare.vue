<template>
  <el-row>
    <el-col :span="24">
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
                     :props="props"
                     class="element2"
                     @change="handleChangeSubject" />
      </div>
    </el-col>

    <el-col :span="24">
      <el-radio-group v-model="compareType"
                      style="margin-bottom: 30px;">
        <el-radio-button label="industry">
          行业
        </el-radio-button>
        <el-radio-button label="concept">
          概念
        </el-radio-button>
        <el-radio-button label="stock">
          Stock
        </el-radio-button>
      </el-radio-group>
    </el-col>

    <el-col :span="24">
      <div class="block">
        <el-cascader v-model="industriesValue"
                     v-show="compareType === 'industry'"
                     :options="industries"
                     :props="props"
                     @change="handleChangeIndustry" />
        <stocks-form v-show="compareType === 'stock'" />
        <el-select v-model="concept_id"
                   v-show="compareType === 'concept'"
                   placeholder="请选择概念"
                   @change="handleChangeConcept">
          <el-option v-for="concept in concepts"
                     :key="concept.id"
                     :label="concept.name"
                     :value="concept.id" />
        </el-select>
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
          开始比较
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
import { compare_stock, industriesApi, conceptsApi } from '../api'
import StocksForm from '../components/StocksForm'

export default {
  name: 'Compare',
  components: {
    StocksForm
  },
  data () {
    return {
      quarter: '',
      is_single: false,
      concept_id: '',
      reportType: undefined,
      subjectsValue: [],
      industriesValue: [],
      compareType: 'industry',
      props: {
        value: 'id',
        label: 'name',
        children: 'children'
      },
      chart: undefined,
      compareData: [],
      industry: undefined,
      subject: undefined,
      concept: undefined
    }
  },
  computed: {
    ...mapState('basedata', {
      territories: state => state.territories.data,
      sections: state => state.sections.data,
      concepts: state => state.concepts.data,
      industries: state => state.industries.data,
      reportTypes: state => state.reportTypes.data,
      accountingSubjects: state => state.accountingSubjects
    }),
    ...mapState('compare', ['stocks']),
    industry_id: function () {
      return this.industriesValue[this.industriesValue.length - 1]
    },
    subject_id: function () {
      return this.subjectsValue[this.subjectsValue.length - 1]
    },
    stocks_str: function () {
      const ids = []
      for (const stock of this.stocks) {
        if (stock && stock.id) {
          ids.push(stock.id)
        }
      }
      return ids.join(',')
    },
    filename: function () {
      let result = `${this.reportType}-${this.subject.name}`

      if (this.industry) {
        result = `${this.industry.name}-${result}`
      }

      if (this.concept) {
        result = `${this.concept.name}-${result}`
      }

      return result
    }
  },
  methods: {
    handleDownload () {
      import('../vendor/Export2Excel').then(excel => {
        const tHeader = ['公司', '季度', '数据']
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
          item.quarter,
          item.value_number
        ]
      })
    },
    handleChangeIndustry (value) {
      this.concept = undefined
      if (this.industry_id) {
        this.get_stocks_by_industry(this.industry_id).then(stocks => {
          this.$store.commit('compare/SET_STOCKS', stocks)
        })
      }
    },
    handleChangeConcept (value) {
      this.industry = undefined
      if (this.concept_id) {
        this.get_stocks_by_concept(this.concept_id).then(stocks => {
          this.$store.commit('compare/SET_STOCKS', stocks)
        })
      }
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
      if (this.stocks_str && this.subject_id) {
        compare_stock({
          stocks: this.stocks_str,
          subject: this.subject_id,
          is_single: this.is_single,
          quarter: this.quarter
        }).then(response => {
          this.compareData = response
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
    },
    async get_stocks_by_industry (industry_id) {
      this.industry = await industriesApi.show(industry_id)
      return this.industry.stocks
    },
    async get_stocks_by_concept (concept_id) {
      this.concept = await conceptsApi.show(concept_id)
      return this.concept.stocks
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
