<template>
  <el-row>
    <el-col :span="24">
      <el-tabs
        v-model="activeName"
        type="border-card"
      >
        <el-tab-pane
          v-for="industry in industries"
          :key="industry.id"
          :label="industry.name"
          :name="industry.name"
        >
          <ul>
            <li
              v-for="industry in industry.children"
              :key="industry.id"
              class="top-tag"
            >
              <template v-if="Array.isArray(industry.children) && industry.children.length > 0">
                <span>{{industry.name}}</span>
                <ul>
                  <li
                    v-for="industry in industry.children"
                    :key="industry.id"
                    class="top-tag"
                  > {{industry.name}} </li>
                </ul>
              </template>

              <span v-else> {{industry.name}} </span>
            </li>
          </ul>
        </el-tab-pane>
      </el-tabs>
    </el-col>
  </el-row>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'IndustryList',
  data() {
    return {
      activeName: '证监会行业(新)'
    };
  },
  computed: {
    ...mapState('basedata', {
      industries: state => state.industries.data,
    }),
  }
}
</script>
