<template>
  <div>
    <!-- 调试表单 -->
    <div class="div-line" style="height: 50px;">
      <span style="width: 10%; float: left;">
        <el-select v-model="api.method" placeholder="请求方法"  style="width: 100%">
          <el-option v-for="item in methods" :key="item.value" :label="item.label" :value="item.value">
          </el-option>
        </el-select>
      </span>
      <span style="width: 80%; float: left;">
        <el-input v-model="api.url" placeholder="请输入接口"></el-input>
      </span>
      <span style="width: 10%; float: left;">
          <el-button type="primary">发送</el-button>
      </span>
    </div>

    <div class="div-line">
      <el-radio v-model="api.params_type" label="params">params</el-radio>
      <el-radio v-model="api.params_type" label="data">form-data</el-radio>
      <el-radio v-model="api.params_type" label="json">JSON</el-radio>
    </div>
    
    <div class="div-line">
      <el-tabs v-model="activeJSON" @tab-click="handleClick">
        <el-tab-pane label="Headers" name="first">
          <vueJsonEditor v-model="api.header" :mode="'code'"></vueJsonEditor>
        </el-tab-pane>
        <el-tab-pane label="Params/Body" name="second">
          <vueJsonEditor v-model="api.params_body" :mode="'code'"></vueJsonEditor>
        </el-tab-pane>
      </el-tabs>
    </div>
    <div class="div-line">
      <el-input type="textarea"
        :rows="5"
        placeholder="Response"
        v-model="result">
      </el-input>
    </div>

    <div class="div-line">
      <el-collapse v-model="activeNames" @change="handleChange">
        <el-collapse-item title="断言" name="1">
         <el-input type="textarea"
            :rows="5"
            placeholder="Assert"
            v-model="assertText">
          </el-input>
        </el-collapse-item>
        <el-collapse-item title="保存用例" name="2">
          <div>保存用例</div>
        </el-collapse-item>       
      </el-collapse>
    </div>



  </div>
</template>

<script>
// import ModuleApi from '../../request/module'
import vueJsonEditor from 'vue-json-editor'

  export default {
    components: {
      vueJsonEditor
    },
    data(){
      return {
        methods:[
          {value: 'get', label: 'GET'}, 
          {value: 'post', label: 'POST'},
          {value: 'put', label: 'PUT'},
          {value: 'delete', label: 'DELETE'}
        ],
        api: {
          method: 'get',
          url: '',
          header: {},
          params_type: 'params',
          params_body: {},
          result: '',
        },
        activeJSON: 'first',
        activeNames: ['1']
      }
    },
    created() {
      console.log("created")
    },
    mounted() {
      console.log("mounted")
    },
    methods: {
      handleClick(tab, event) {
        console.log(tab, event);
      },

      handleChange(val) {
        console.log(val);
      }

    }

  }
</script>

<style>
div.jsoneditor {
    border: thin solid #ced4da;
}

div.jsoneditor-menu {
    display: none;
}

.ace-jsoneditor .ace_gutter {
    background: white;
}

div.jsoneditor-outer.has-main-menu-bar {
    margin-top: 0px;
    padding-top: 0px;
}

.per-label {
    margin-right: 10px;
    margin-bottom: 4px;
    font-size: 1rem;
}
</style>
<style scoped>
.debug-button {
  height: 50px;
  text-align: right;
}

.div-line {
  height: auto;
  width: 100%;
  text-align: left;
  margin-bottom: 10px;
}

</style>