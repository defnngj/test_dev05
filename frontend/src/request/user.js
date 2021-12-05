import request from '@/HttpCommon.js'


class UserApi {

  login(data) {
    return request.post('/v1/login/', data)
  }

  logout(data) {
    return request.delete('/v1/login/', data)
  }
  
  register(data) {
    return request.post('/v1/register/', data)
  }

}

export default new UserApi()