<template>
  <div class="navbar">
    <el-menu :default-active="activeIndex"
             mode="horizontal"
             @select="handleSelect">
      <el-submenu v-for="industry in industries"
                  :key="industry.id"
                  :index="'industry-' + industry.id">
        <template slot="title">{{industry.name}}</template>
        <industry-menu :industries="industry.children" />
      </el-submenu>

      <el-submenu index="concept">
        <template slot="title">概念</template>
        <el-menu-item v-for="concept in concepts"
                      :key="concept.id"
                      :index="String(concept.id)">
          {{ concept.name }}
        </el-menu-item>
      </el-submenu>

      <el-submenu index="section"
                  disabled>
        <template slot="title">板块</template>
        <el-menu-item v-for="section in sections"
                      :key="section.id"
                      :index="String(section.id)">
          {{ section.name }}
        </el-menu-item>
      </el-submenu>

      <el-submenu index="territory">
        <template slot="title">地域</template>
        <el-menu-item v-for="territory in territories"
                      :key="territory.id"
                      :index="String(territory.id)">
          {{ territory.name }}
        </el-menu-item>
      </el-submenu>
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
        activeIndex: 'industry-1',
        activeIndex2: '1'
      };
    },
  computed: {
    ...mapState('basedata', {
      industries: state => state.industries.data,
      concepts: state => state.concepts.data,
      sections: state => state.sections.data,
      territories: state => state.territories.data
    }),
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    }
  }
}
</script>
