<template>
  <div class="result">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>报告管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <el-card class="box-card">
      <div class="filter-line">
        <!-- <el-input v-model="input" placeholder="请输入内容" style=" width: 200px;"></el-input> -->
        <el-select v-model="taskId" clearable placeholder="请选择任务名称"  @change="selectTask()">
          <el-option
            v-for="item in taskOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          >
          </el-option>
        </el-select>
        <!-- <el-button type="primary" @click="showCreate()">搜索</el-button> -->
      </div>
      <!-- 表格 -->
      <el-table :data="tableData"
          v-loading="loading"
          element-loading-text="拼命加载中"
          element-loading-spinner="el-icon-loading"
          element-loading-background="rgba(0, 0, 0, 0.8)"
          style="width: 100%">
        <el-table-column prop="name" label="名称" min-width="20%">
        </el-table-column>
        <el-table-column prop="tests" label="用例" min-width="10%">
        </el-table-column>
        <el-table-column prop="error" label="错误" min-width="10%">
        </el-table-column>
        <el-table-column prop="failure" label="失败" min-width="10%">
        </el-table-column>
        <el-table-column prop="skipped" label="跳过" min-width="10%">
        </el-table-column>
        <el-table-column prop="run_time" label="运行时长" min-width="10%">
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="20%">
        </el-table-column>
        <el-table-column prop="task_name" label="任务" min-width="20%">
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button @click="showResult(scope.row)" type="primary" size="mini" circle icon="el-icon-s-data"></el-button>
            <!-- <el-button @click="showEdit(scope.row)" type="primary" size="mini" circle icon="el-icon-edit"></el-button> -->
            <el-button @click="deleteResult(scope.row)" type="danger" size="mini" circle icon="el-icon-delete"></el-button>
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
    <ResultDialog v-if="showDailog" :rid=resultId @cancel="cancelResult"></ResultDialog>
  </div>
</template>

<script>
import ResultApi from '../../request/result'
import TaskApi from '../../request/task'
import ResultDialog from './ResultDialog.vue'

  export default {
    components: {
      ResultDialog
    },
    data(){
      return {
        loading: false,
        resultId: 0,
        tableData: [],
        showDailog: false,
        total: 0,
        query: {
          page: 1,
          size: 5,
        },
        resultHeartbeat:null,
        taskOptions: [],
        taskId: ""
      }
    },
    created() {
      console.log("父组件", this.showDailog)
    },
    mounted() {
      this.initResult()
      this.initTask()
    //   this.resultHeartbeat = setInterval(() => {
    //     this.initResult()
    //   }, 5000);
    },
    destroyed() {
      // 销毁时候清除定时器
      // clearInterval(this.resultHeartbeat);
    },
    methods: {
      async initTask() {
        const query = {page: 1, size: 1000}
        const resp = await TaskApi.getTasks(query)
        if (resp.success == true) {
          const data = resp.data.taskList
          for (let i = 0; i < data.length; i++) {
            this.taskOptions.push({
              value: data[i].id,
              label: data[i].name,
            })
          }
        } else {
          this.$message.error(resp.error.message);
        }
      },
      async initResult() {
        this.loading = true
        if(this.taskId == ""){
          this.query.taskId = ""
        } else {
          this.query.taskId = this.taskId
        }
        const resp = await ResultApi.getResults(this.query)
        if (resp.success == true) {
          this.tableData = resp.data.resultList
          this.total = resp.data.total
        } else {
          this.$message.error(resp.error.message);
        }
        this.loading = false
      },

      // 根据任务名称搜索
      selectTask() {
        console.log("this.taskId", this.taskId)
        // this.query.task_id = this.taskId
        this.initResult()
      },

      // 显示编辑窗口
      showResult(row) {
        console.log("row.id", row.id)
        this.resultId = row.id
        this.showDailog = true
      },

      // 显示创建窗口
      showCreate() {
        this.showDailog = true
      },

      // 显示编辑窗口
      showEdit(row) {
        console.log("row.id", row.id)
        this.resultId = row.id
        this.showDailog = true
      },

      // 删除一条任务信息
      async deleteResult(row) {
        const resp = await ResultApi.deleteResult(row.id)
        if (resp.success == true) {
          this.$message.success("删除成功！")
          this.initResult()
        } else {
          this.$message.error("删除失败");
        }
      },

      
      // 子组件的回调
      cancelResult() {
        this.showDailog = false
        this.resultId = 0
        this.initResult()
      },
      
      // 删除一条任务信息
      async runResult(row) {
        const resp = await ResultApi.runResult(row.id)
        if (resp.success == true) {
          this.$message.success("运行成功！")
          this.initResult()
        } else {
          this.$message.error("运行失败");
        }
      },

      // 修改每页显示个数
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`)
        this.query.size = val
        this.initResult()
      },

      // 点给第几页
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`)
        this.query.page = val
        this.initResult()
      }

    }

  }
</script>


<style scoped>
.filter-line {
  float: right;
  height: 50px;
}
.foot-page {
  margin-top: 20px;
    float: right;
    margin-bottom: 20px;
}

</style>
