<template>
  <div class="project-dialog">
    <el-dialog title="创建项目" :visible.sync="showStatus" @close="cancelProject()">
      <el-form ref="form" :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input type="textarea" v-model="form.desc"></el-input>
        </el-form-item>
        <el-form-item label="状态">
          <span style="float: left;">
            <el-switch v-model="form.delivery"></el-switch>
          </span>
        </el-form-item>
        <el-form-item>
          <div class="dialog-footer">
            <el-button @click="cancelProject()">取消</el-button>
            <el-button type="primary" @click="onSubmit()">创建</el-button>
          </div>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
// import ProjectApi from '../../request/project'

  export default {
    props: [],
    data(){
      return {
        showStatus: true,
        form: {
          name: '',
          desc: '',
          delivery: true
        }, 
      }
    },
    created() {
      console.log("自动被执行created")
      console.log("子组件", this.showStatus)
    },
    mounted() {
      console.log("自动被执行mounted")
    //   this.initProject()
    },
    methods: {
      // 关闭dialog
      cancelProject() {
        console.log("我把自己关闭了")
        this.$emit('cancel', {})
      },

      // 创建项目按钮
      onSubmit() {
        console.log("创建额")
      }

    }

  }
</script>

<style scoped>
.dialog-footer {
  float: right;
}
</style>