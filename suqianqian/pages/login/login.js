/**
 * AI Skill 库 - 登录页
 * 通过 wx.login() 获取 code，发送到云托管后端完成登录
 */
const request = require('../../utils/request')
const { log } = require('../../utils/logger')

Page({
  data: {
    isLogging: false,
    showTips: false,
    tipsText: '',
  },

  onLoad() {
    const token = wx.getStorageSync('token')
    if (token) {
      getApp().globalData.isLoggedIn = true
      wx.switchTab({ url: '/pages/index/index' })
    }
  },

  async handleLogin() {
    if (this.data.isLogging) return
    this.setData({ isLogging: true })
    log('Login', '开始登录')

    try {
      const loginRes = await new Promise((resolve, reject) => {
        wx.login({ success: resolve, fail: reject })
      })

      if (!loginRes.code) {
        throw new Error('获取登录凭证失败')
      }

      const res = await request.post('/api/auth/login', { code: loginRes.code })
      log('Login', '登录成功')

      wx.setStorageSync('token', res.token)
      getApp().globalData.isLoggedIn = true

      wx.switchTab({ url: '/pages/index/index' })
    } catch (err) {
      log('Login', '登录失败', err.message)
      this.showTips(err.message || '登录失败，请重试')
    } finally {
      this.setData({ isLogging: false })
    }
  },

  showTips(text) {
    this.setData({ showTips: true, tipsText: text })
    setTimeout(() => {
      this.setData({ showTips: false })
    }, 3000)
  },
})
