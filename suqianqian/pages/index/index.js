/**
 * AI Skill 库 - 首页
 * 搜索 + 分类标签 + Skill 卡片流 + Banner 广告
 */
const { get } = require('../../utils/request')
const { log } = require('../../utils/logger')

Page({
  data: {
    searchKey: '',
    categories: [],
    activeCategory: '',
    skills: [],
    page: 1,
    hasMore: true,
    loading: false,
    adEnabled: false,
    notice: '本小程序仅提供 Skill 文本素材，需自备 Ollama / Dify / Open-WebUI 环境使用',
  },

  onLoad() {
    this.loadCategories()
    this.loadSkills()
    this.loadAdSwitch()
  },

  onPullDownRefresh() {
    this.setData({ page: 1, hasMore: true, skills: [] })
    Promise.all([this.loadSkills(), this.loadCategories()]).finally(() => {
      wx.stopPullDownRefresh()
    })
  },

  onReachBottom() {
    if (this.data.hasMore && !this.data.loading) {
      this.loadSkills()
    }
  },

  /** 加载分类 */
  async loadCategories() {
    try {
      const res = await get('/api/categories')
      this.setData({ categories: res.categories || [] })
    } catch (e) {
      log('Index', '加载分类失败', e.message)
    }
  },

  /** 加载 Skill 列表 */
  async loadSkills() {
    if (this.data.loading) return
    this.setData({ loading: true })
    try {
      const { page, searchKey, activeCategory } = this.data
      let url = `/api/skills?page=${page}&page_size=10`
      if (searchKey) url += `&keyword=${encodeURIComponent(searchKey)}`
      if (activeCategory) url += `&category=${encodeURIComponent(activeCategory)}`
      const res = await get(url)
      const items = res.items || []
      this.setData({
        skills: page === 1 ? items : [...this.data.skills, ...items],
        hasMore: items.length >= 10,
        page: page + 1,
      })
    } catch (e) {
      log('Index', '加载Skill失败', e.message)
    } finally {
      this.setData({ loading: false })
    }
  },

  /** 加载广告开关 */
  async loadAdSwitch() {
    try {
      const res = await get('/api/settings/ad-switch')
      this.setData({ adEnabled: res.ad_enabled })
    } catch (e) { /* ignore */ }
  },

  /** 搜索输入 */
  onSearchInput(e) {
    this.setData({ searchKey: e.detail.value })
  },

  /** 搜索确认 */
  onSearch() {
    this.setData({ page: 1, hasMore: true, skills: [] })
    this.loadSkills()
  },

  /** 清空搜索 */
  onClearSearch() {
    this.setData({ searchKey: '', page: 1, hasMore: true, skills: [] })
    this.loadSkills()
  },

  /** 切换分类标签 */
  onCategoryTap(e) {
    const cat = e.currentTarget.dataset.cat
    const active = this.data.activeCategory === cat ? '' : cat
    this.setData({ activeCategory: active, page: 1, hasMore: true, skills: [] })
    this.loadSkills()
  },

  /** 进入详情 */
  onSkillTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` })
  },
})
