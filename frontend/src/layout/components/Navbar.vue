<template>
  <div class="navbar">
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      router
    >
      <el-menu-item index="industries">行业</el-menu-item>
      <el-menu-item index="concepts">概念</el-menu-item>
      <el-menu-item index="sections">板块</el-menu-item>
      <el-menu-item index="territories">地域</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import ErrorLog from '../../components/ErrorLog'

export default {
  name: 'Navbar',
  components: {
    ErrorLog
  },
  data() {
    return {
      activeIndex: 'industries',
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      this.activeIndex = keyPath
    }
  }
}
</script>
