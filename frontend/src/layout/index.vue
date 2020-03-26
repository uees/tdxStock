<template>
  <el-container>
    <el-header style="font-size: 12px">
      <navbar />
    </el-header>
    <el-main>
      <app-main />
    </el-main>
  </el-container>
</template>

<script>
import { Navbar, AppMain } from './components'

export default {
  name: 'Layout',
  components: {
    Navbar,
    AppMain
  }
}
</script>

<style lang="scss" scoped>
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}
</style>
