<template>
  <div class="login">
    <h1>测试平台</h1>

    <el-tabs v-model="activeName" type="border-card" style="width: 350px;">
      <!-- 登录 -->
      <el-tab-pane label="登录" name="login">
        <el-form :model="form" :rules="rules" ref="form" class="demo-form">
          <div class="main-login-input">
            <el-form-item prop="username">
              <el-input placeholder="请输账号" v-model="form.username">
                <template slot="prepend">账号</template>
              </el-input>
            </el-form-item>
          </div>
          <div class="main-login-input">
            <el-form-item prop="password">
              <el-input v-model="form.password" type="password" placeholder="请输入密码">
                <template slot="prepend">密码</template>
              </el-input>
            </el-form-item>
          </div>
          <div class="main-login-button">
            <el-button id="loginButton" type="primary" @click="submitForm('form')">登录</el-button>
          </div>
        </el-form>
      </el-tab-pane>

      <!-- 注册 -->
      <el-tab-pane label="注册" name="register">
        <el-form :model="regForm" :rules="regRules" ref="regForm" class="demo-form">
          <div class="main-login-input">
            <el-form-item prop="username">
              <el-input placeholder="请输账号" v-model="regForm.username">
                <template slot="prepend">账号</template>
              </el-input>
            </el-form-item>
          </div>
          <div class="main-login-input">
            <el-form-item prop="password1">
              <el-input v-model="regForm.password1" placeholder="请输入密码" type="password">
                <template slot="prepend">设置密码</template>
              </el-input>
            </el-form-item>
          </div>
          <div class="main-login-input">
            <el-form-item prop="password2">
              <el-input v-model="regForm.password2" placeholder="请再次输入密码" type="password">
                <template slot="prepend">确认密码</template>
              </el-input>
            </el-form-item>
          </div>
          <div class="main-login-button">
            <el-button id="loginButton" type="danger" @click="registerForm('regForm')">注册</el-button>
          </div>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    
  </div>
</template>

<script>
import UserApi from  "../request/user"

export default {
  name: "login",
  data() {
    return {
      activeName: "login",
      form: {
        username: "admin",
        password: "admin123456",
      },
      rules: {
        username: [{ required: true, message: "请输入账号", trigger: "blur" }],
        password: [{ required: true, message: "请输入密码", trigger: "blur" }],
      },
      regForm: {
        username: "zhangsan",
        password1: "abc123456",
        password2: "abc123456",
      },
      regRules: {
        username: [{ required: true, message: "请输入账号", trigger: "blur" }],
        password1: [{ required: true, message: "请输入设置密码", trigger: "blur" }],
        password2: [{ required: true, message: "请输入重复密码", trigger: "blur" }],
      },
    };
  },
  methods: {
    // 表单验证
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
          if (valid) {
          // this.loginSubmit();
          UserApi.login(this.form).then(resp => {
            if (resp.success == true) {
              console.log("resp-->", resp);
              sessionStorage.token = resp.data.Token
              sessionStorage.user = resp.data.User
              // this.$store.commit('login', resp.data.Token)
              this.$router.push({path: '/main/project'})
              this.$message.success("登录成功！")
              // console.log('wtf', this.$route.query.redirect);
              // this.$router.push(this.$route.query.redirect || '/project');
            } else {
              this.$message.error(resp.error.message);
            }
          })
        }
      });
    },
    // 用户注册
    registerForm(formName) {
      this.$refs[formName].validate((valid) => {
          if (valid) {
          // this.loginSubmit();
          UserApi.register(this.regForm).then(resp => {
            if (resp.success == true) {
              this.$message.success("注册成功！")
            } else {
              this.$message.error(resp.error.message);
            }
          })
        }
      });
    },

  },
  mounted() {},
};
</script>

<!-- element-ui style -->
<style>
.login #loginButton {
  width: 300px;
  height: auto;
}
</style>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.login {
  width: 300px;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}
.main-login-input {
  margin-top: 5px;
  margin-bottom: 10px;
}
h1,
h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>