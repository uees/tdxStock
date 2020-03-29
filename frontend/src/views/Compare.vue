<template>
  <el-row>
    <el-col :span="24">
      <div class="block">
        <el-cascader
          v-model="value"
          :options="options"
          @change="handleChange"
        ></el-cascader>
      </div>
    </el-col>
  </el-row>
</template>

<script>
import { mapState } from 'vuex'
import {compare_stock, stocksApi} from '../api'

export default {
  name: 'Compare',
  data() {
    return {
      value: [],
    }
  },
  computer: {
    ...mapState('basedata', {
      territories: state => state.territories.data,
      sections: state => state.sections.data,
      concepts: state => state.concepts.data,
      industries: state => state.industries.data,
      reportTypes: state => state.reportTypes.data,
      accountingSubjects: state => state.accountingSubjects
    })
  },
  methods: {
    handleChange() {

    }
  }
}
</script>
