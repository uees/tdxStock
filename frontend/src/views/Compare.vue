<template>
  <el-row>
    <el-col :span="24">
      <div class="report-type-content">
        <el-select v-model="reportType"
                   placeholder="请选择报表类型">
          <el-option v-for="item in reportTypes"
                     :key="item.slug"
                     :label="item.name"
                     :value="item.slug">
          </el-option>
        </el-select>

        <el-cascader v-model="subjectsValue"
                     :options="accountingSubjects[reportType]"
                     :props="props"
                     class="element2"></el-cascader>
      </div>
    </el-col>

    <el-col :span="24">
      <el-radio-group v-model="compareType"
                      style="margin-bottom: 30px;">
        <el-radio-button label="industry">行业</el-radio-button>
        <el-radio-button label="concept">概念</el-radio-button>
        <el-radio-button label="stock">Stock</el-radio-button>
      </el-radio-group>
    </el-col>

    <el-col :span="24">
      <div class="block">
        <el-cascader v-model="industriesValue"
                     v-show="compareType === 'industry'"
                     :options="industries"
                     :props="props"
                     @change="handleChangeIndustry"></el-cascader>
        <stocks-form v-show="compareType === 'stock'" />
        <el-select v-model="concept_id"
                   v-show="compareType === 'concept'"
                   placeholder="请选择概念"
                   @change="handleChangeConcept">
          <el-option v-for="concept in concepts"
                     :key="concept.id"
                     :label="concept.name"
                     :value="concept.id">
          </el-option>
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
                 active-text="单季度">
      </el-switch>

      <div class="submit-content">
        <el-button type="primary"
                   @click="handleCompare">开始比较</el-button>
        <el-button type="success"
                   class="element2"
                   @click="drawChart">分面</el-button>
        <el-button type="success"
                   class="element2"
                   @click="drawChart2">趋势</el-button>
        <el-button type="info"
                   class="element2">下载数据</el-button>
      </div>
    </el-col>

    <el-col :span="24">
      <div id="chart-container"></div>
    </el-col>
  </el-row>
</template>

<script>
import { mapState } from 'vuex'
import { Chart } from '@antv/g2'
import {compare_stock, industriesApi, conceptsApi} from '../api'
import StocksForm from '../components/StocksForm'

export default {
  name: 'Compare',
  components: {
    StocksForm
  },
  data() {
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
      compareData: []
    }
  },
  computed: {
    ...mapState('basedata', {
      territories: state => state.territories.data,
      sections: state => state.sections.data,
      concepts: state => state.concepts.data,
      industries: state => state.industries.data,
      reportTypes: state => state.reportTypes.data,
      accountingSubjects: state => state.accountingSubjects,
    }),
    ...mapState('compare', ['stocks']),
    stocksString: function() {
      return ''
    },
    industry_id: function() {
      return this.industriesValue[this.industriesValue.length - 1]
    },
    subject_id: function() {
      return this.subjectsValue[this.subjectsValue.length - 1]
    },
    stocks_str: function() {
      const ids = []
      for (const stock of this.stocks) {
        if (stock && stock.id) {
          ids.push(stock.id)
        }
      }
      return ids.join(',')
    }
  },
  methods: {
    handleChangeIndustry(value) {
      if (this.industry_id) {
        this.get_stocks_by_industry(this.industry_id).then(stocks => {
          this.$store.commit('compare/SET_STOCKS', stocks)
        })
      }
    },
    handleChangeConcept(value) {
      if (this.concept_id) {
        this.get_stocks_by_concept(this.concept_id).then(stocks => {
          this.$store.commit('compare/SET_STOCKS', stocks)
        })
      }
    },
    handleCompare() {
      if (this.stocks_str && this.subject_id) {
        compare_stock({
          stocks: this.stocks_str,
          subject: this.subject_id,
          is_single: this.is_single,
          quarter: this.quarter
        }).then(response => {
          this.compareData = response
          this.drawChart2()
        })
      } else {
        window.alert("没选择股票，或者没选择会计科目")
      }
    },
    clearQuarter() {
      this.quarter = ''
    },
    drawChart() {
      this.chart && this.chart.destroy()
      // Step 1: 创建 Chart 对象
      this.chart = new Chart({
        container: 'chart-container',
        autoFit: false,
        width: 1200,
        height: 600,
        padding: [0, 100, 0, 100],
      })

      // Step 2: 载入数据源
      this.chart.data(this.compareData);

      this.chart.scale({
        value_number: {
          sync: true,
        },
      });

      // Step 3：创建图形语法
      this.chart.facet('rect', {
        fields: [null, 'stock'],
        rowTitle: {
          style: {
            textAlign: 'start',
            fontSize: 12,
          },
        },
        eachView(view) {
          view.area().position('quarter*value_number');
          view.line().position('quarter*value_number');
          view
            .point()
            .position('quarter*value_number')
            .shape('circle');
        },
      });

      // Step 4: 渲染图表
      this.chart.render();
    },
    drawChart2() {
      this.chart && this.chart.destroy()
      // Step 1: 创建 Chart 对象
      this.chart = new Chart({
        container: 'chart-container',
        width: 1200,
        height: 600,
      })

      // Step 2: 载入数据源
      this.chart.data(this.compareData);

      // Step 3：创建图形语法，绘制柱状图
      this.chart.point().position('quarter*value_number').color('stock');
      this.chart.line().position('quarter*value_number').color('stock');

      // Step 4: 渲染图表
      this.chart.render();
    },
    async get_stocks_by_industry(industry_id) {
      const industry = await industriesApi.show(industry_id)
      return industry.stocks
    },
    async get_stocks_by_concept(concept_id) {
      const concept = await conceptsApi.show(concept_id)
      return concept.stocks
    },
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
