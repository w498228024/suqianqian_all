/**
 * AI Skill 库 - 我的页面
 * 收藏、上传、关于、免责
 */
const { get } = require('../../utils/request')
const { log } = require('../../utils/logger')

Page({
  data: {
    isLoggedIn: false,
    activeTab: '', // 'favorites' | 'uploads' | ''
    favorites: [],
    uploads: [],
    loading: false,
    page: 1,
    hasMore: true,
  },

  onShow() {
    const app = getApp()
    this.setData({ isLoggedIn: app.globalData.isLoggedIn })
  },

  /** 跳转登录 */
  goLogin() {
    wx.navigateTo({ url: '/pages/login/login' })
  },

  /** 切换 Tab */
  onTabTap(e) {
    const tab = e.currentTarget.dataset.tab
    if (this.data.activeTab === tab) {
      this.setData({ activeTab: '' })
      return
    }
    this.setData({ activeTab: tab, page: 1, hasMore: true })
    if (tab === 'favorites') this.loadFavorites()
    if (tab === 'uploads') this.loadUploads()
  },

  /** 加载收藏 */
  async loadFavorites() {
    if (this.data.loading) return
    this.setData({ loading: true })
    try {
      const { page } = this.data
      const res = await get(`/api/skills/favorites/list?page=${page}&page_size=10`)
      const items = res.items || []
      this.setData({
        favorites: page === 1 ? items : [...this.data.favorites, ...items],
        hasMore: items.length >= 10,
        page: page + 1,
      })
    } catch (e) {
      log('Mine', '加载收藏失败', e.message)
    } finally {
      this.setData({ loading: false })
    }
  },

  /** 加载我的上传 */
  async loadUploads() {
    if (this.data.loading) return
    this.setData({ loading: true })
    try {
      const { page } = this.data
      const res = await get(`/api/skills/uploads/list?page=${page}&page_size=10`)
      const items = res.items || []
      this.setData({
        uploads: page === 1 ? items : [...this.data.uploads, ...items],
        hasMore: items.length >= 10,
        page: page + 1,
      })
    } catch (e) {
      log('Mine', '加载上传失败', e.message)
    } finally {
      this.setData({ loading: false })
    }
  },

  /** 进入详情 */
  onItemTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` })
  },

  /** 关于我们 */
  onAbout() {
    wx.showModal({
      title: 'AI Skill 库',
      content: 'AI Skill 库 —— 本地 AI 工具专用 Skill/Md 提示词素材平台\n\n版本: 1.0.0\n\n纯工具、无 AI 推理、无对话、无生成\n只提供：Skill 文本预览、一键复制、Md 文件下载、分类检索',
      showCancel: false,
    })
  },

  /** 免责声明 */
  onDisclaimer() {
    wx.showModal({
      title: '免责声明',
      content: '1. 本小程序仅提供 Skill 文本素材，需自备 Ollama / Dify / Open-WebUI 环境使用。\n\n2. 所有 Skill 内容均为用户投稿，平台不对内容的准确性、完整性作任何保证。\n\n3. 用户在使用 Skill 过程中产生的任何结果，与本小程序无关。\n\n4. 如发现侵权内容，请联系平台处理。',
      showCancel: false,
    })
  },

  /** 退出登录 */
  onLogout() {
    wx.showModal({
      title: '提示',
      content: '确定退出登录？',
      success: (res) => {
        if (res.confirm) {
          getApp().clearLoginStatus()
          this.setData({ isLoggedIn: false, activeTab: '', favorites: [], uploads: [] })
          wx.showToast({ title: '已退出', icon: 'success' })
        }
      },
    })
  },

  onReachBottom() {
    if (this.data.activeTab && this.data.hasMore && !this.data.loading) {
      if (this.data.activeTab === 'favorites') this.loadFavorites()
      if (this.data.activeTab === 'uploads') this.loadUploads()
    }
  },

  statusText(s) {
    return { published: '已发布', pending: '审核中', rejected: '已驳回' }[s] || s
  },
})
