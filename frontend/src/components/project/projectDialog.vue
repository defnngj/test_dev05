<template>
  <div class="project-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelProject()">
      <el-form :rules="rules" ref="form" :model="form" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="form.describe"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <span style="float: left;">
            <el-switch v-model="form.status"></el-switch>
          </span>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="cancelProject()">取消</el-button>
            <el-button type="primary" @click="onSubmit('form')">保存</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
  import ProjectApi from '../../request/project'

  export default {
    props: ['pid'],
    data() {
      return {
        showStatus: true,
        showTitle: '',
        form: {
          name: '',
          describe: '',
          status: true
        },
         rules: {
          name: [
            { required: true, message: '请输入项目名称', trigger: 'blur' }
          ]
         }
      }
    },
    created() {
      if (this.pid === 0) {
        this.showTitle = "创建项目"
      } else {
        this.showTitle = "编辑项目"
        this.getProject()
      }
    },
    mounted() {
      console.log("自动被执行mounted")
    //   this.initProject()
    },
    methods: {

      // 获取一条项目信息
      async getProject() {
        const resp = await ProjectApi.getProject(this.pid)
        if (resp.success == true) {
          this.form = resp.data
        } else {
          this.$message.error(resp.error.message);
        }
      },

      // 关闭dialog
      cancelProject() {
        this.$emit('cancel', {})
      },

      // 创建项目按钮
      onSubmit(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            if(this.pid === 0) {
              ProjectApi.createProject(this.form).then(resp => {
                if (resp.success == true) {
                  this.$message.success("创建成功！")
                  this.cancelProject()
                } else {
                  this.$message.error("创建失败！");
                }
              })
            } else {
              ProjectApi.updateProject(this.pid, this.form).then(resp => {
                if (resp.success == true) {
                  this.$message.success("更新成功！")
                  this.cancelProject()
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

<style scoped>
.dialog-footer {
  float: right;
}
</style>