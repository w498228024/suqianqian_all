/**
 * AI Skill 库 - 分类页
 * 全部分类树状展示，点击筛选对应 Skill
 */
const { get } = require('../../utils/request')
const { log } = require('../../utils/logger')

Page({
  data: {
    categories: [],
    activeCategory: '',
    activeSub: '',
    skills: [],
    loading: false,
    page: 1,
    hasMore: true,
  },

  onLoad() {
    this.loadCategories()
  },

  onPullDownRefresh() {
    this.setData({ page: 1, hasMore: true, skills: [] })
    this.loadCategories().finally(() => wx.stopPullDownRefresh())
  },

  onReachBottom() {
    if (this.data.activeCategory && this.data.hasMore && !this.data.loading) {
      this.loadSkills()
    }
  },

  async loadCategories() {
    try {
      const res = await get('/api/categories')
      this.setData({ categories: res.categories || [] })
    } catch (e) {
      log('Classify', '加载分类失败', e.message)
    }
  },

  /** 点击一级分类 */
  onCategoryTap(e) {
    const cat = e.currentTarget.dataset.cat
    const isActive = this.data.activeCategory === cat
    this.setData({
      activeCategory: isActive ? '' : cat,
      activeSub: '',
      skills: [],
      page: 1,
      hasMore: true,
    })
    if (!isActive) {
      this.loadSkills()
    }
  },

  /** 点击二级分类 */
  onSubTap(e) {
    const sub = e.currentTarget.dataset.sub
    const isActive = this.data.activeSub === sub
    this.setData({
      activeSub: isActive ? '' : sub,
      skills: [],
      page: 1,
      hasMore: true,
    })
    this.loadSkills()
  },

  async loadSkills() {
    if (this.data.loading) return
    this.setData({ loading: true })
    try {
      const { page, activeCategory, activeSub } = this.data
      let url = `/api/skills?page=${page}&page_size=10&category=${encodeURIComponent(activeCategory)}`
      if (activeSub) url += `&sub_category=${encodeURIComponent(activeSub)}`
      const res = await get(url)
      const items = res.items || []
      this.setData({
        skills: page === 1 ? items : [...this.data.skills, ...items],
        hasMore: items.length >= 10,
        page: page + 1,
      })
    } catch (e) {
      log('Classify', '加载Skill失败', e.message)
    } finally {
      this.setData({ loading: false })
    }
  },

  onSkillTap(e) {
    const id = e.currentTarget.dataset.id
    wx.navigateTo({ url: `/pages/detail/detail?id=${id}` })
  },
})
