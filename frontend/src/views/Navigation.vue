<template>
  <div class="navigation">
    <el-container style="height: 100%; border: 1px solid #eee">
      <el-aside width="160px" style="background-color: rgb(84, 92, 100)">
        <!-- <h1>重定向</h1> -->
        <img class="logo" alt="itest logo" src="../assets/itestLogo.png" />
        <el-menu
          default-active="onRoutes"
          class="el-menu-vertical-demo"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
        >
          <!-- 项目管理 -->
          <router-link to="/">
            <el-menu-item index="1">
              <i class="el-icon-menu"></i>
              <span slot="title">项目管理</span>
            </el-menu-item>
          </router-link>
          <router-link to="/module">
            <el-menu-item index="2">
              <i class="el-icon-s-grid"></i>
              <span slot="title">模块管理</span>
            </el-menu-item>
          </router-link>
          <router-link to="/case">
            <el-menu-item index="3">
              <i class="el-icon-s-data"></i>
              <span slot="title">用例管理</span>
            </el-menu-item>
          </router-link>
          <router-link to="/task">
            <el-menu-item index="4">
              <i class="el-icon-s-order"></i>
              <span slot="title">任务管理</span>
            </el-menu-item>
          </router-link>
        </el-menu>
      </el-aside>

      <el-container>
        <el-header style="text-align: right; font-size: 12px">
          <span>王小虎</span>
          <el-dropdown>
            <i class="el-icon-setting" style="margin-right: 15px"></i>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item>查看</el-dropdown-item>
              <el-dropdown-item>新增</el-dropdown-item>
              <el-dropdown-item>删除</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
        </el-header>
        <el-main>
          <router-view> </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  computed: {
    onRoutes() {
      if (this.$route.path === '/module') {
        return '2'
      } else if (this.$route.path === '/case') {
        return '3'
      } else if (this.$route.path === '/task') {
        return '4'
      } 
      return '1'
    }
  },
  data() {
    const item = {
      date: "2016-05-02",
      name: "王小虎",
      address: "上海市普陀区金沙江路 1518 弄",
    };
    return {
      tableData: Array(20).fill(item),
    };
  },
};
</script>

<style>
.navigation {
  height: 800px;
}

.nav {
  height: 100%;
}
.el-container {
  height: 100%;
}

a {
  text-decoration: none;
}

.router-link-active {
  text-decoration: none;
}

.logo {
  margin-top: 20px;
  margin-bottom: 10px;
  height: 15px;
}
.el-header {
  background-color: #b3c0d1;
  color: #333;
  line-height: 60px;
}

.el-aside {
  color: #333;
}
</style>

