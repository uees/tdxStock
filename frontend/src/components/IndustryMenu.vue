<template>
  <fragment>
    <!-- root element 不能 v-for, 这里用 fragment 虚拟标签 -->
    <el-menu-item v-for="industry in industries"
                  :key="industry.id"
                  :index="industry.parent + '-' +industry.id">

      <template v-if="Array.isArray(industry.children) && industry.children.length > 0">
        <el-submenu :index="industry.parent + '-' +industry.id"
                    menu-trigger="click">
          <template slot="title">{{ industry.name }}</template>
          <industry-menu :industries="industry.children" />
        </el-submenu>
      </template>

      <span v-else>{{ industry.name }}</span>
    </el-menu-item>
  </fragment>
</template>

<script>
import { Fragment } from 'vue-fragment'

export default {
    name: 'industry-menu',
    components: { Fragment },
    props: {
        'industries': Array
    }
}
</script>
