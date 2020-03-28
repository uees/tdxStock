import request from './request'

export default class RestApi {
  constructor (config) {
    const options = {
      url: '',
      subPath: '',
      methods: ['list', 'store', 'update', 'destroy', 'show']
    }
    this.config = Object.assign({}, options, config)
    this.url = this.config.url
    if (this.config.subPath) {
      if (!this.url.endsWith('/')) {
        this.url = `${this.url}/`
      }
      this.url = `${this.url}${this.config.subPath}`
    }
    this.methods = this.config.methods
    this.applyApi()
  }

  applyApi () {
    if (this.methods.includes('list')) {
      this.list = (config) => {
        return request.get(this.url, config)
      }
    }

    if (this.methods.includes('store')) {
      this.store = (obj, config) => {
        return request.post(this.url, obj, config)
      }
    }

    if (this.methods.includes('update')) {
      this.update = (id, obj, config) => {
        if (!this.url.endsWith('/')) {
          this.url = `${this.url}/`
        }
        return request.patch(`${this.url}${id}`, obj, config)
      }
    }

    if (this.methods.includes('destroy')) {
      this.destroy = (id, config) => {
        if (!this.url.endsWith('/')) {
          this.url = `${this.url}/`
        }
        return request.delete(`${this.url}${id}`, config)
      }
    }

    if (this.methods.includes('show')) {
      this.show = (id, config) => {
        if (!this.url.endsWith('/')) {
          this.url = `${this.url}/`
        }
        return request.get(`${this.url}${id}`, config)
      }
    }
  }
}
