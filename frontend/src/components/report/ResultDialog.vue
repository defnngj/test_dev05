<template>
  <div class="project-dialog">
    <el-dialog :title=showTitle :visible.sync="showStatus" @close="cancelProject()" width="70%">
      <div>
        <div id="myChart" :style="{width: '380px', height: '380px'}" style="margin: 0 auto;"></div>
      </div>
      <div>
        <el-table :data="tableData" border style="width: 80%; margin: 0 auto;">
          <el-table-column prop="name" label="名称" min-width="20%">
          </el-table-column>
          <el-table-column prop="passed" label="通过" min-width="10%">
          </el-table-column>
          <el-table-column prop="error" label="错误" min-width="10%">
          </el-table-column>
          <el-table-column prop="failure" label="失败" min-width="10%">
          </el-table-column>
          <el-table-column prop="skipped" label="跳过" min-width="10%">
          </el-table-column>
          <el-table-column prop="run_time" label="运行时长" min-width="10%">
          </el-table-column>
        </el-table>
      </div>
      <el-divider content-position="left">详细日志</el-divider>
      <div>
        <el-input
          type="textarea"
          :rows="20"
          placeholder="XML日志"
          v-model="logDetail">
        </el-input>
      </div>
    </el-dialog>
  </div>
</template>

<script>
  import ResultApi from '../../request/result'
  // > npm install echarts -S
  import * as echarts from 'echarts'
  
  export default {
    props: ['rid'],
    data() {
      return {
        showStatus: true,
        showTitle: '',
        inResize: true,
        option: {
          tooltip: {
            trigger: 'item'
          },
          legend: {
            top: '5%',
            left: 'center'
          },
          series: [
            {
              name: 'Access From',
              type: 'pie',
              radius: ['40%', '70%'],
              avoidLabelOverlap: false,
              itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
              },
              label: {
                show: false,
                position: 'center'
              },
              emphasis: {
                label: {
                  show: true,
                  fontSize: '40',
                  fontWeight: 'bold'
                }
              },
              labelLine: {
                show: false
              },
              data: [
                { value: 1, name: 'skipped' },
                { value: 1, name: 'passed' },
                { value: 1, name: 'failure' },
                { value: 1, name: 'error' }
              ]
            }
          ]
        },
        tableData: [],
        logDetail: '',
      }
    },
    created() {
    },
    mounted() {
      console.log("自动被执行mounted")
      this.$nextTick(() => {
        this.initChart()
      })
    
    },
    methods: {
      // 初始化图表
      async initChart() {
        var myChart = echarts.init(document.getElementById('myChart'));

        const resp = await ResultApi.getResult(this.rid)
        if(resp.success == true){
          resp.data.passed = parseInt(resp.data.tests) - parseInt(resp.data.failure) - parseInt(resp.data.error) - parseInt(resp.data.skipped)
          this.option.series[0].data[0].value = resp.data.skipped
          this.option.series[0].data[1].value = resp.data.passed
          this.option.series[0].data[2].value = resp.data.failure 
          this.option.series[0].data[3].value = resp.data.error 
        }
        myChart.setOption(this.option);
        // 表格
        this.tableData.push(resp.data)
        // 日志
        this.logDetail = resp.data.result
        console.log("--->", this.tableData)
      },

      // 关闭dialog
      cancelProject() {
        this.$emit('cancel', {})
      },

    }

  }
</script>

<style scoped>
.dialog-footer {
  float: right;
}
</style>