// app.js
App({
  onLaunch() {
    // 初始化云能力（云托管需要）
    if (wx.cloud) {
      wx.cloud.init({ traceUser: true })
    }
    this.checkLoginStatus()
  },

  checkLoginStatus() {
    const token = wx.getStorageSync('token')
    this.globalData.isLoggedIn = !!token
  },

  setLoginStatus(token) {
    wx.setStorageSync('token', token)
    this.globalData.isLoggedIn = true
  },

  clearLoginStatus() {
    wx.removeStorageSync('token')
    this.globalData.isLoggedIn = false
  },

  /** 检查是否已登录，未登录跳转登录页 */
  requireLogin() {
    if (!this.globalData.isLoggedIn) {
      wx.navigateTo({ url: '/pages/login/login' })
      return false
    }
    return true
  },

  globalData: {
    isLoggedIn: false,
  },
})
