import request from '@/HttpCommon.js'


class ResultApi {

  getResults(data) {
    return request.get('/v1/result/list/', data)
  }

  getResult(tid) {
    return request.get('/v1/result/'+tid+'/info/')
  }

  deleteResult(tid) {
    return request.delete('/v1/result/'+tid+'/delete/')
  }
}

export default new ResultApi()