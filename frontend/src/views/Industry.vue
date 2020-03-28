<template>
  <el-row>
    <el-col :span="24">

    </el-col>
  </el-row>
</template>

<script>
export default {
  name: 'Industry',
  data() {
    return {
      id: undefined
    };
  },
  computed: {
    ...mapState('basedata', {
      industries: state => state.industries.data,
    }),
  },
  beforeRouteUpdate (to, from, next) {
    // react to route changes...
    // don't forget to call next()
    this.id = to.params.id
    this.getStocks()
    next()
  },
  methods: {
    getStocks() {

    }
  }
}
</script>
