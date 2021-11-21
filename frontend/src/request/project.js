import request from '@/HttpCommon.js'


class ProjectApi {
    getProjects(data) {
      return request.get('/v1/project/', data)
    }

    getProject(pid) {
      return request.get('/v1/project/'+pid+'/')
    }

    deleteProject(pid) {
      return request.delete('/v1/project/'+pid+'/')
    }
  
    createProject(data) {
      return request.post('/v1/project/', data)
    }
  
    updateProject(pid, data) {
      return request.put('/v1/project/'+pid+'/', data)
    }
    
    getModules(project_id, data) {
      return request.get('/v1/project/'+project_id+'/module/', data)
    }

  }
  
  export default new ProjectApi()