import request from '@/HttpCommon.js'


class CaseApi {
  debugCase(data) {
    return request.post('/v1/case/debug/', data)
  }

  assertCase(data) {
    return request.post('/v1/case/assert/', data)
  }
  
  getCases(data) {
    return request.get('/v1/case/list', data)
  }

  getCase(cid) {
    return request.get('/v1/case/'+cid+'/info')
  }

  deleteCase(cid) {
    return request.delete('/v1/case/'+cid+'/')
  }

  createCase(data) {
    return request.post('/v1/case/create/', data)
  }

  updateCase(cid, data) {
    return request.put('/v1/case/'+cid+'/', data)
  }

  getCaseTree() {
    return request.get('/v1/case/tree')
  }
}

export default new CaseApi()