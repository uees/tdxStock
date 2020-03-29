<template>
  <div class="navbar">
    <el-menu
      :default-active="activeIndex"
      mode="horizontal"
      @select="handleSelect"
    >
      <el-menu-item index="industries">
        行业
      </el-menu-item>

      <el-menu-item index="concepts">
        概念
      </el-menu-item>

      <el-menu-item
        index="sections"
        disabled
      >
        板块
      </el-menu-item>

      <el-menu-item index="territories">
        地域
      </el-menu-item>

      <el-menu-item index="compare">
        比较
      </el-menu-item>

      <el-menu-item>
        <error-log class="errLog-container right-menu-item hover-effect" />
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script>
import ErrorLog from '../../components/ErrorLog'

export default {
  name: 'Navbar',
  components: {
    ErrorLog
  },
  data () {
    return {
      activeIndex: 'industries'
    }
  },
  methods: {
    handleSelect (key, keyPath) {
      // console.log(key, keyPath);
      const to_path = '/' + key
      if (this.$router.history.current.path !== to_path) {
        this.$router.push(to_path)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.errLog-container {
  display: inline-block;
  vertical-align: top;
}

.right-menu-item {
  display: inline-block;
  padding: 0 8px;
  height: 100%;
  font-size: 18px;
  color: #5a5e66;
  vertical-align: text-bottom;

  &.hover-effect {
    cursor: pointer;
    transition: background 0.3s;

    &:hover {
      background: rgba(0, 0, 0, 0.025);
    }
  }
}
</style>
