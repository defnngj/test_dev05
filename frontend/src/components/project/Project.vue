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

      <el-table :data="tableData"
          v-loading="loading"
          element-loading-text="拼命加载中"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)"
          style="width: 100%">
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
            <el-button @click="showEdit(scope.row)" type="primary" size="mini" circle icon="el-icon-edit"></el-button>
            <el-button @click="deleteProject(scope.row)" type="danger" size="mini" circle icon="el-icon-delete"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="foot-page">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :page-sizes="[5, 10, 20, 50]" 
          :page-size=query.size
          background
          layout="total, sizes, prev, pager, next"
          :total=total>
        </el-pagination>

      </div>
    </el-card>
    <projectDialog v-if="showDailog" :pid=projectId @cancel="cancelProject"></projectDialog>
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
        loading: false,
        projectId: 0,
        tableData: [],
        showDailog: false,
        total: 0,
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
        this.loading = true
        const resp = await ProjectApi.getProjects(this.query)
        console.log("resp--->", resp)
        if (resp.success == true) {
          console.log("success")
          this.tableData = resp.data.projectList
          this.total = resp.data.total
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 显示创建窗口
      showCreate() {
        this.showDailog = true
      },

      // 显示编辑窗口
      showEdit(row) {
        console.log("row.id", row.id)
        this.projectId = row.id
        this.showDailog = true
      },

      // 删除一条项目信息
      async deleteProject(row) {
        console.log("row.id", row.id)
        const resp = await ProjectApi.deleteProject(row.id)
        console.log("resp--->", resp)
        if (resp.success == true) {
          this.$message.success("删除成功！")
          this.initProject()
        } else {
          this.$message.error("删除失败");
        }

      },
      // 子组件的回调
      cancelProject() {
        console.log("子组件把自己关闭了")
        this.showDailog = false
        this.projectId = 0
        this.initProject()
      },

      // 修改每页显示个数
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`)
        this.query.size = val
        this.initProject()
      },

      // 点给第几页
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`)
        this.query.page = val
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
.foot-page {
  margin-top: 20px;
    float: right;
    margin-bottom: 20px;
}

</style>