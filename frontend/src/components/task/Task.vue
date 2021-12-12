<template>
  <div class="task">
    <div style="height: 30px;">
      <el-breadcrumb separator-class="el-icon-arrow-right">
        <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
        <el-breadcrumb-item>任务管理</el-breadcrumb-item>
      </el-breadcrumb>
    </div>
    <el-card class="box-card">
      <div class="filter-line">
        <el-button type="primary" @click="showCreate()">创建</el-button>
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
        <el-table-column prop="describe" label="描述" min-width="30%">
        </el-table-column>
        <el-table-column prop="status" label="状态" min-width="15%">
          <template slot-scope="scope">
            <span v-if="scope.row.status === 0">
              <el-tag>未执行</el-tag>
            </span>
            <span v-else-if="scope.row.status === 1">
              <el-tag>执行中</el-tag>
            </span>
            <span v-else-if="scope.row.status === 2">
              <el-tag>已完成</el-tag>
            </span>
            <span v-else>
              <el-tag>{{scope.row.status}}</el-tag>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="create_time" label="创建时间" min-width="30%">
        </el-table-column>
        <el-table-column fixed="right" label="任务" width="50">
          <template slot-scope="scope">
            <el-button @click="runTask(scope.row)" type="primary" size="mini" circle icon="el-icon-time"></el-button>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template slot-scope="scope">
            <el-button @click="showEdit(scope.row)" type="primary" size="mini" circle icon="el-icon-edit"></el-button>
            <el-button @click="deleteTask(scope.row)" type="danger" size="mini" circle icon="el-icon-delete"></el-button>
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
    <TaskDialog v-if="showDailog" :tid=taskId @cancel="cancelTask"></TaskDialog>
  </div>
</template>

<script>
import TaskApi from '../../request/task'
import TaskDialog from './TaskDialog.vue'

  export default {
    components: {
      TaskDialog
    },
    data(){
      return {
        loading: false,
        taskId: 0,
        tableData: [],
        showDailog: false,
        total: 0,
        query: {
          page: 1,
          size: 5,
        },
        taskHeartbeat:null
      }
    },
    created() {
      console.log("父组件", this.showDailog)
    },
    mounted() {
      this.initTask()
      this.taskHeartbeat = setInterval(() => {
        this.initTask()
      }, 5000);
    },
    destroyed() {
      // 销毁时候清除定时器
      clearInterval(this.taskHeartbeat);
    },
    methods: {
      async initTask() {
        this.loading = true
        const resp = await TaskApi.getTasks(this.query)
        if (resp.success == true) {
          this.tableData = resp.data.taskList
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
        this.taskId = row.id
        this.showDailog = true
      },

      // 删除一条任务信息
      async deleteTask(row) {
        const resp = await TaskApi.deleteTask(row.id)
        if (resp.success == true) {
          this.$message.success("删除成功！")
          this.initTask()
        } else {
          this.$message.error("删除失败");
        }
      },

      
      // 子组件的回调
      cancelTask() {
        this.showDailog = false
        this.taskId = 0
        this.initTask()
      },
      
      // 删除一条任务信息
      async runTask(row) {
        const resp = await TaskApi.runTask(row.id)
        if (resp.success == true) {
          this.$message.success("运行成功！")
          this.initTask()
        } else {
          this.$message.error("运行失败");
        }
      },

      // 修改每页显示个数
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`)
        this.query.size = val
        this.initTask()
      },

      // 点给第几页
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`)
        this.query.page = val
        this.initTask()
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
