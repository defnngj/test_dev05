<template>
  <div class="case">
    <!-- 面包屑 -->
    <div v-if="isList" style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>用例管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <div v-else style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item >
          <a @click="showDebug()">用例管理</a>
        </el-breadcrumb-item>
        <el-breadcrumb-item>用例调试</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <!-- 卡片 -->
    <el-card  class="box-card">
      <div v-if="isList" class="filter-line">
        <el-button type="primary" @click="showDebug()">创建</el-button>
      </div>
      <div v-else class="filter-line">
        <el-page-header @back="showDebug()" content="API"></el-page-header>
      </div>
        
      <div v-if="isList">
        <!-- 表格 -->
        <el-table :data="tableData" v-loading="loading" style="width: 100%">
          <el-table-column prop="name" label="名称" min-width="20%">
          </el-table-column>
          <el-table-column prop="method" label="方法" min-width="10%">
          </el-table-column>
          <el-table-column prop="url" label="URL" min-width="30%">
          </el-table-column>
          <el-table-column prop="module_name" label="模块" min-width="15%">
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
      </div>
      <div v-else>
        <CaseDebug :cid=caseId></CaseDebug>
      </div>
    </el-card>
  </div>
</template>

<script>
import ModuleApi from '../../request/module'
import CaseApi from '../../request/case'
import CaseDebug from './CaseDebug.vue'

  export default {
    components: {
      CaseDebug
    },
    data(){
      return {
        isList: true,
        loading: false,
        moduleId: 0,
        tableData: [],
        showDailog: false,
        total: 0,
        query: {
          page: 1,
          size: 5,
        },
        caseId: 0,
      }
    },
    created() {
      console.log("父组件", this.showDailog)
    },
    mounted() {
      this.initCases()
    },
    methods: {
      // 初始化用例列表
      async initCases() {
        this.loading = true
        const resp = await CaseApi.getCases(this.query)
        if (resp.success == true) {
          this.tableData = resp.data.caseList
          this.total = resp.data.total
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 显示创建窗口
      showDebug() {        
        // this.showDailog = true
        if (this.isList === true) {
          this.isList = false
        } else {
          this.isList = true
          this.caseId = 0
        }
      },

      // 显示编辑窗口
      showEdit(row) {
        this.caseId = row.id
        this.showDebug()
      },

      // 删除一条项目信息
      async deleteModule(row) {
        this.$confirm('是否要删除用例?', '提示', {
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