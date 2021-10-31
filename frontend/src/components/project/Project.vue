<template>
  <div class="project">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>项目管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <el-card class="box-card">
      <div class="filter-line">
        <el-button type="primary" @click="showCreate()">创建</el-button>
      </div>

      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="name" label="名称" min-width="20%">
        </el-table-column>
        <el-table-column prop="describe" label="描述" min-width="45%">
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="15%">
          <template slot-scope="scope">
          <span v-if="scope.row.status === true">
            <el-tag>开启</el-tag>
          </span>
          <span v-else>
            <el-tag type="info">关闭</el-tag>
          </span>
        </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" min-width="20">
          <template slot-scope="scope">
            <el-button @click="handleClick(scope.row)" type="text" size="small">编辑</el-button>
            <el-button type="text" size="small">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <projectDialog v-if="showDailog" @cancel="cancelProject"></projectDialog>
  </div>
</template>

<script>
import ProjectApi from '../../request/project'
import projectDialog from './projectDialog.vue'

  export default {
    components: {
      projectDialog
    },
    data(){
      return {
        tableData: [],
        showDailog: false,
        query: {
          page: 1,
          size: 5,
        }
      }
    },
    created() {
      console.log("自动被执行created")
      console.log("父组件", this.showDailog)
    },
    mounted() {
      console.log("自动被执行mounted")
      this.initProject()
    },
    methods: {
      async initProject() {
        const resp = await ProjectApi.getProjects(this.query)
        console.log("resp--->", resp)
        if (resp.success == true) {
          console.log("success")
          this.tableData = resp.data.projectList
        } else {
          this.$message.error(resp.error.message);
        }
      },

      // 显示创建窗口
      showCreate() {
        this.showDailog = true
      },

      // 子组件的回调
      cancelProject() {
        console.log("子组件把自己关闭了")
        this.showDailog = false
        this.initProject()
      }

    }

  }
</script>

<style scoped>
.filter-line {
  height: 50px;
  text-align: left;
}

</style>