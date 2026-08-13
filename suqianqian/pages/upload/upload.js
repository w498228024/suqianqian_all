/**
 * AI Skill 库 - 上传页
 * 用户投稿 Skill，提交后进入待审核状态
 */
const { get, post } = require('../../utils/request')
const { log } = require('../../utils/logger')

const FIT_TOOLS = ['Ollama', 'OpenWebUI', 'Dify', 'ChatGLM', 'LM Studio', '其他']

Page({
  data: {
    title: '',
    desc: '',
    content: '',
    category: '',
    subCategory: '',
    categories: [],
    subCategories: [],
    fitTools: FIT_TOOLS,
    selectedTools: [],
    tags: '',
    sourceType: '原创',
    sourceTypes: ['原创', '开源改编', '用户投稿'],
    license: 'MIT',
    licenses: ['MIT', 'Apache2.0', '原创版权', 'CC-BY-4.0'],
    submitting: false,
    agreed: false,
  },

  onLoad() {
    this.loadCategories()
  },

  onShow() {
    const app = getApp()
    if (!app.globalData.isLoggedIn) {
      wx.showToast({ title: '请先登录', icon: 'none' })
    }
  },

  async loadCategories() {
    try {
      const res = await get('/api/categories')
      this.setData({ categories: res.categories || [] })
    } catch (e) {
      log('Upload', '加载分类失败', e.message)
    }
  },

  onTitleInput(e) { this.setData({ title: e.detail.value }) },
  onDescInput(e) { this.setData({ desc: e.detail.value }) },
  onContentInput(e) { this.setData({ content: e.detail.value }) },
  onTagsInput(e) { this.setData({ tags: e.detail.value }) },

  onCategoryChange(e) {
    const idx = e.detail.value
    const cat = this.data.categories[idx]
    this.setData({
      category: cat.name,
      subCategory: '',
      subCategories: cat.sub_categories || [],
    })
  },

  onSubCategoryChange(e) {
    const idx = e.detail.value
    this.setData({ subCategory: this.data.subCategories[idx] })
  },

  onToolToggle(e) {
    const tool = e.currentTarget.dataset.tool
    const selected = this.data.selectedTools
    const idx = selected.indexOf(tool)
    if (idx >= 0) {
      selected.splice(idx, 1)
    } else {
      selected.push(tool)
    }
    this.setData({ selectedTools: [...selected] })
  },

  onSourceTypeChange(e) {
    this.setData({ sourceType: this.data.sourceTypes[e.detail.value] })
  },

  onLicenseChange(e) {
    this.setData({ license: this.data.licenses[e.detail.value] })
  },

  onAgreeChange(e) {
    this.setData({ agreed: e.detail.value })
  },

  async onSubmit() {
    const app = getApp()
    if (!app.globalData.isLoggedIn) {
      wx.navigateTo({ url: '/pages/login/login' })
      return
    }

    const { title, desc, content, category, subCategory, selectedTools, tags, sourceType, license, agreed } = this.data

    if (!title.trim()) return wx.showToast({ title: '请输入标题', icon: 'none' })
    if (!category) return wx.showToast({ title: '请选择分类', icon: 'none' })
    if (!content.trim()) return wx.showToast({ title: '请输入正文内容', icon: 'none' })
    if (!agreed) return wx.showToast({ title: '请勾选版权协议', icon: 'none' })

    this.setData({ submitting: true })
    try {
      const tagList = tags.split(/[,，、\s]+/).filter(t => t.trim())
      await post('/api/skills', {
        title: title.trim(),
        desc: desc.trim(),
        content,
        category,
        sub_category: subCategory,
        tags: tagList,
        fit_tools: selectedTools,
        source_type: sourceType,
        license,
      })
      wx.showToast({ title: '提交成功，等待审核', icon: 'success' })
      // 重置表单
      this.setData({
        title: '', desc: '', content: '', category: '', subCategory: '',
        subCategories: [], selectedTools: [], tags: '', sourceType: '原创',
        license: 'MIT', agreed: false,
      })
    } catch (e) {
      log('Upload', '提交失败', e.message)
      wx.showToast({ title: e.message || '提交失败', icon: 'none' })
    } finally {
      this.setData({ submitting: false })
    }
  },
})
