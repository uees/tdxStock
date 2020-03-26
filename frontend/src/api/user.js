import request from '../utils/request'
import RestApi from '../utils/restapi'

export function login(data) {
  return request.post('/auth/login', data, {
    notAuth: true
  })
}

export function logout() {
  return request({
    url: '/auth/logout',
    method: 'delete'
  })
}

export function refreshToken() {
  return request.put('/auth/refresh')
}

export function getInfo() {
  return request({
    url: '/user',
    method: 'get',
    params: {
      include: 'roles'
    }
  })
}

export function changePassword(data) {
  return request.put('/user/password', data)
}

export function changeProfile(data) {
  return request.patch('/user', data)
}

export const usersApi = new RestApi({
  url: '/users'
})

export const rolesApi = new RestApi({
  url: '/roles'
})
