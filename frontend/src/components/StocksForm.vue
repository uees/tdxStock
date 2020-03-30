<template>
  <div class="stocks-form">
    <el-button-group style="margin-bottom: 12px">
      <el-button type="primary"
                 icon="el-icon-edit"
                 size="mini"
                 @click="handleCreate"> 添加 </el-button>
      <el-button type="primary"
                 icon="el-icon-close"
                 size="mini"
                 @click="handleClear"> 清除所有 </el-button>
    </el-button-group>

    <el-table :data="stocks">
      <el-table-column label="股票">
        <template slot-scope="scope">
          <el-autocomplete v-model="scope.row.name"
                           :fetch-suggestions="querySearchAsync"
                           label="name"
                           value-key="name"
                           placeholder="请输入内容"
                           @select="handleSelect(scope)"></el-autocomplete>
        </template>
      </el-table-column>

      <el-table-column align="center"
                       label="操作"
                       width="220">
        <template slot-scope="scope">
          <el-button type="danger"
                     icon="el-icon-delete"
                     size="small"
                     @click="handleDelete(scope)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import {Stock} from '../defines/models'
import {stocksApi} from '../api'

export default {
  name: 'StocksForm',
  data() {
    return {

    }
  },
  computed: {
    ...mapState('compare', [
      'stocks',
      'index'
    ])
  },
  methods: {
    handleCreate() {
      this.$store.commit('compare/ADD_STOCK', Stock())
    },
    handleDelete(scope) {
      this.$store.commit('compare/DELETE_STOCK', scope.$index)
    },
    handleClear() {
      this.$store.commit('compare/SET_STOCKS', [Stock(),])
    },
    handleSelect(scope) {
      return (stock) => {
        if (this.stocks.findIndex(element => element.id === stock.id) === -1) {
          this.$store.commit('compare/UPDATE_STOCK', {
            index: scope.$index,
            stock: stock
          })
        }
      }
    },
    async querySearchAsync(queryString, cb) {
      const {results} = await stocksApi.list({ params: {q: queryString} })
      cb(results)
    }
  }
}
</script>

<style>
</style>
