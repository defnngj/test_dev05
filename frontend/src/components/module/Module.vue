<template>
  <div class="module">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>模块管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <el-card class="box-card">
      <div class="filter-line">
        <el-button type="primary" @click="showCreate()">创建</el-button>
      </div>
      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" style="width: 100%">
        <el-table-column prop="name" label="名称" min-width="15%">
        </el-table-column>
        <el-table-column prop="describe" label="描述" min-width="30%">
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="10%">
          <template slot-scope="scope">
            <span v-if="scope.row.status === true">
              <el-tag>开启</el-tag>
            </span>
            <span v-else>
              <el-tag type="info">关闭</el-tag>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="project_name" label="项目" min-width="15%">
        </el-table-column>
        <el-table-column prop="create_time" label="创建" min-width="20%">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button @click="showEdit(scope.row)" type="primary" size="mini" circle icon="el-icon-edit"></el-button>
            <el-button @click="deleteModule(scope.row)" type="danger" size="mini" circle icon="el-icon-delete"></el-button>
          </template>
        </el-table-column>
      </el-table>
      <!-- 分页 -->
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
    <ModuleDialog v-if="showDailog" :mid=moduleId @cancel="cancelModule"></ModuleDialog>
  </div>
</template>

<script>
import ModuleApi from '../../request/module'
import ModuleDialog from './ModuleDialog.vue'

  export default {
    components: {
      ModuleDialog
    },
    data(){
      return {
        loading: false,
        moduleId: 0,
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
      console.log("父组件", this.showDailog)
    },
    mounted() {
      this.initModule()
    },
    methods: {
      // 初始化模块列表
      async initModule() {
        this.loading = true
        const resp = await ModuleApi.getModules(this.query)
        if (resp.success == true) {
          this.tableData = resp.data.moduleList
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
        this.moduleId = row.id
        this.showDailog = true
      },

      // 删除一条项目信息
      async deleteModule(row) {
        this.$confirm('是否要删除模块?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          ModuleApi.deleteModule(row.id).then(resp =>{
            if (resp.success == true) {
              this.$message.success("删除成功！")
              this.initModule()
            } else {
              this.$message.error("删除失败");
            }
          })
          
        })        
      },

      // 子组件的回调
      cancelModule() {
         console.log("接收到-子组件关闭")
        this.showDailog = false
        this.moduleId = 0
        this.initModule()
      },

      // 修改每页显示个数
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`)
        this.query.size = val
        this.initModule()
      },

      // 点给第几页
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`)
        this.query.page = val
        this.initModule()
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