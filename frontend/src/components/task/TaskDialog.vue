<template>
  <div class="task-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelTask()">
      <el-form v-if="inResize === true" :rules="rules" ref="form" :model="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="form.describe"></el-input>
        </el-form-item>
        <el-form-item label="选择用例">
          <div class="div-tree">
            <el-tree :data="data" :props="defaultProps" show-checkbox
              @node-click="handleNodeClick"
              @check-change="handleCheckChange"
              node-key="id"
              :default-checked-keys="checkId">
            </el-tree>
          </div>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="cancelTask()">取消</el-button>
            <el-button type="primary" @click="onSubmit('form')">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  import TaskApi from '../../request/task'
  import CaseApi from '../../request/case'

  export default {
    props: ['tid'],
    data() {
      return {
        showStatus: true,
        showTitle: '',
        form: {
          id: 0,
          name: '',
          describe: '',
          cases: []
        },
         rules: {
          name: [
            { required: true, message: '请输入任务名称', trigger: 'blur' }
          ]
        },
        inResize: true,
        data:[],
        defaultProps: {
          children: 'children',
          label: 'label'
        },
        checkId: []
      }
    },
    created() {
      if (this.tid === 0) {
        this.showTitle = "创建任务"
      } else {
        this.showTitle = "编辑任务"
        this.getTask()
      }
      // 强制刷新
      this.inResize = false;
      this.$nextTick(() => {
        this.inResize = true;
      });
    },
    mounted() {
      console.log("自动被执行mounted")
      // this.initTask()
      this.InitCaseTree()
    },
    methods: {
      handleCheckChange(data, checked) {
        // console.log("aaa", data, checked);
        // console.log("aaa1", data.id);
        if(data.id != undefined) {
          console.log("操作的叶子节点", data.id, checked);
          if(checked == true) {
            this.form.cases.push(data.id)
          } else {
            // this.form.cases.remove(data.id)
            // arr2.splice(1,2,'ttt'); 
            for (var i = 0; i < this.form.cases.length; i++) {
              if(this.form.cases[i] == data.id) {
                this.form.cases.splice(i, 1);
              }
            }
          }
        }
        console.log("cases", this.form.cases)
      },
      handleNodeClick(data) {
        console.log("bbb", data);
      },

      // 获取用例树
      async InitCaseTree() {
        const resp = await CaseApi.getCaseTree()
        if (resp.success == true) {
          console.log(resp.data)
          this.data = resp.data
        } else {
          this.$message.error(resp.error.message);
        }
      },

      // 获取一条任务信息
      async getTask() {
        const resp = await TaskApi.getTask(this.tid)
        if (resp.success == true) {
          this.form = resp.data
          this.checkId = resp.data.cases
        } else {
          this.$message.error(resp.error.message);
        }
      },

      // 关闭dialog
      cancelTask() {
        this.$emit('cancel', {})
      },

      // 创建任务按钮
      onSubmit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.tid === 0) {
              TaskApi.createTask(this.form).then(resp => {
                if (resp.success == true) {
                  this.$message.success("创建成功！")
                  this.cancelTask()
                } else {
                  this.$message.error("创建失败！");
                }
              })
            } else {
              this.form.id = this.tid
              TaskApi.updateTask(this.form).then(resp => {
                if (resp.success == true) {
                  this.$message.success("更新成功！")
                  this.cancelTask()
                } else {
                  this.$message.error("更新失败！");
                }
              })
            }
            
          } else {
            return false;
          }
        });
        
      },

    }

  }
</script>

<style>
.el-tree {
  background: #f1f3fa !important;
}
</style>
<style scoped>
.dialog-footer {
  float: right;
}
.div-tree {
  max-height: 180px;
  overflow: auto;
}
</style>