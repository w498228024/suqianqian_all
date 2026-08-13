/**
 * AI Skill 库 - 网络请求封装
 * 支持本地开发（wx.request → localhost）和云托管（wx.cloud.callContainer）两种模式
 *
 * 切换方式：修改下方 USE_CLOUD 变量
 *   false — 本地开发，直连 localhost:8000
 *   true  — 生产环境，走微信云托管
 */
const { log, error } = require('./logger')

// ==================== 模式切换 ====================
const USE_CLOUD = true  // ← 本地开发设为 false，部署时改为 true
const LOCAL_BASE_URL = 'http://localhost:8000'
const CONTAINER_NAME = 'flask-p0w8'  // 云托管服务名
const CLOUD_ENV = 'prod-d6gf8996d0722a6d3'  // 云托管环境 ID
// ==================== 模式切换 ====================

/**
 * 通用请求方法
 */
function request(url, options = {}) {
  const { method = 'GET', data = {}, header = {} } = options

  // 自动注入 token
  const token = wx.getStorageSync('token')
  if (token) {
    header['Authorization'] = `Bearer ${token}`
  }

  log('Request', `${method} ${url}`, { data, cloud: USE_CLOUD })

  if (USE_CLOUD) {
    // ===== 云托管模式 =====
    return new Promise((resolve, reject) => {
      wx.cloud.callContainer({
        config: { env: CLOUD_ENV },
        path: url,
        method,
        header: {
          'X-WX-SERVICE': CONTAINER_NAME,
          'Content-Type': 'application/json',
          ...header,
        },
        data,
        success: handleResponse(resolve, reject, method, url),
        fail: (err) => {
          error('Request', `${method} ${url} 失败`, err)
          reject(new Error('网络连接失败，请检查网络'))
        },
      })
    })
  } else {
    // ===== 本地开发模式 =====
    return new Promise((resolve, reject) => {
      wx.request({
        url: LOCAL_BASE_URL + url,
        method,
        data,
        header: {
          'Content-Type': 'application/json',
          ...header,
        },
        success: handleResponse(resolve, reject, method, url),
        fail: (err) => {
          error('Request', `${method} ${url} 失败`, err)
          reject(new Error('网络连接失败，请检查后端服务是否启动'))
        },
      })
    })
  }
}

/**
 * 统一响应处理
 */
function handleResponse(resolve, reject, method, url) {
  return (res) => {
    log('Response', `${method} ${url} [${res.statusCode}]`, res.data)
    if (res.statusCode >= 200 && res.statusCode < 300) {
      resolve(res.data)
    } else if (res.statusCode === 401) {
      wx.removeStorageSync('token')
      getApp().globalData.isLoggedIn = false
      wx.switchTab({ url: '/pages/index/index' })
      reject(new Error('登录已过期'))
    } else if (res.statusCode === 403) {
      reject(new Error(res.data.detail || '操作受限'))
    } else {
      const errMsg = res.data.detail || res.data.message || `请求失败 (${res.statusCode})`
      reject(new Error(errMsg))
    }
  }
}

/**
 * GET 请求
 */
function get(url, header = {}) {
  return request(url, { method: 'GET', header })
}

/**
 * POST 请求
 */
function post(url, data = {}, header = {}) {
  return request(url, { method: 'POST', data, header })
}

/**
 * PUT 请求
 */
function put(url, data = {}, header = {}) {
  return request(url, { method: 'PUT', data, header })
}

/**
 * DELETE 请求
 */
function del(url, header = {}) {
  return request(url, { method: 'DELETE', header })
}

/**
 * 上传文件
 */
function uploadFile(url, options = {}) {
  const { filePath, name = 'file', header = {}, timeout = 120000 } = options

  const token = wx.getStorageSync('token')
  if (token) {
    header['Authorization'] = `Bearer ${token}`
  }

  log('Upload', `POST ${url}`, { filePath: filePath?.substring(filePath.lastIndexOf('/') + 1), name, timeout })

  if (USE_CLOUD) {
    return new Promise((resolve, reject) => {
      wx.cloud.callContainer({
        config: { env: CLOUD_ENV },
        path: url,
        method: 'POST',
        header: { 'X-WX-SERVICE': CONTAINER_NAME, ...header },
        data: { filePath, name },
        success: (res) => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            try { resolve(JSON.parse(res.data)) } catch (e) { resolve(res.data) }
          } else {
            reject(new Error(`上传失败 (${res.statusCode})`))
          }
        },
        fail: (err) => reject(new Error('文件上传失败')),
      })
    })
  } else {
    return new Promise((resolve, reject) => {
      wx.uploadFile({
        url: LOCAL_BASE_URL + url,
        filePath,
        name,
        header,
        timeout,
        success: (res) => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            try { resolve(JSON.parse(res.data)) } catch (e) { resolve(res.data) }
          } else if (res.statusCode === 401) {
            wx.removeStorageSync('token')
            wx.navigateTo({ url: '/pages/login/login' })
            reject(new Error('登录已过期'))
          } else {
            reject(new Error(`上传失败 (${res.statusCode})`))
          }
        },
        fail: (err) => {
          const msg = err.errMsg || ''
          reject(new Error(msg.includes('timeout') ? '上传超时' : '文件上传失败'))
        },
      })
    })
  }
}

module.exports = {
  get,
  post,
  put,
  del,
  uploadFile,
}
