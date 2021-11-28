import request from '@/HttpCommon.js'


class TaskApi {

  getTasks(data) {
    return request.get('/v1/task/list/', data)
  }

  getTask(tid) {
    return request.get('/v1/task/'+tid+'/info')
  }

  deleteTask(tid) {
    return request.delete('/v1/task/'+tid+'/')
  }

  createTask(data) {
    return request.post('/v1/task/create/', data)
  }

  updateTask(data) {
    return request.put('/v1/task/update/', data)
  }
  
  runTask(tid) {
    return request.get('/v1/task/'+tid+'/running')
  }

}

export default new TaskApi()