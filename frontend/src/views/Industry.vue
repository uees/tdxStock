<template>
  <el-row>
    <el-col :span="24">
      <el-tag
        v-for="stock in stocks"
        :key="stock.id"
        class="stock-tag"
      >
        {{ stock.name }}
      </el-tag>
    </el-col>
  </el-row>
</template>

<script>
import { industriesApi } from '@/api'

export default {
  name: 'Industry',
  props: ['id'],
  data () {
    return {
      stocks: []
    }
  },
  created () {
    this.getStocks()
  },
  methods: {
    async getStocks () {
      const industry = await industriesApi.show(this.id)
      this.stocks = industry.stocks
    }
  }
}
</script>

<style scoped>
.stock-tag {
  margin-left: 12px;
  margin-bottom: 12px;
}
</style>
