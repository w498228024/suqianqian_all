/**
 * AI Skill 库 - Skill 详情页
 * Md 渲染 + 一键复制 + 下载 MD + 收藏
 */
const { get, post } = require('../../utils/request')
const { log } = require('../../utils/logger')

Page({
  data: {
    skill: null,
    mdBlocks: [],
    isFavorited: false,
    favAnimating: false,
    adEnabled: false,
    loading: true,
  },

  onLoad(options) {
    if (options.id) {
      this.skillId = options.id
      this.loadDetail(options.id)
      this.loadAdSwitch()
    }
  },

  async loadDetail(id) {
    this.setData({ loading: true })
    try {
      const res = await get(`/api/skills/${id}`)
      this.setData({ skill: res })
      wx.setNavigationBarTitle({ title: res.title || 'Skill 详情' })
      this.renderMd(res.content || '')
      // 检查收藏状态
      const app = getApp()
      if (app.globalData.isLoggedIn) {
        this.checkFavorite(id)
      }
    } catch (e) {
      log('Detail', '加载详情失败', e.message)
      wx.showToast({ title: '加载失败', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },

  async checkFavorite(id) {
    try {
      const res = await get(`/api/skills/favorites/status?skill_id=${id}`)
      this.setData({ isFavorited: !!res.is_favorited })
    } catch (e) { /* ignore */ }
  },

  async loadAdSwitch() {
    try {
      const res = await get('/api/settings/ad-switch')
      this.setData({ adEnabled: res.ad_enabled })
    } catch (e) { /* ignore */ }
  },

  /** 简易 Markdown 渲染为 blocks */
  renderMd(text) {
    const blocks = []
    const lines = text.split('\n')
    let inCodeBlock = false
    let codeContent = ''
    let codeLang = ''

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]

      // 代码块
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          blocks.push({ type: 'code', lang: codeLang, content: codeContent.trimEnd() })
          codeContent = ''
          inCodeBlock = false
        } else {
          inCodeBlock = true
          codeLang = line.slice(3).trim()
        }
        continue
      }
      if (inCodeBlock) {
        codeContent += line + '\n'
        continue
      }

      // 标题
      if (line.startsWith('### ')) {
        blocks.push({ type: 'h3', content: line.slice(4) })
      } else if (line.startsWith('## ')) {
        blocks.push({ type: 'h2', content: line.slice(3) })
      } else if (line.startsWith('# ')) {
        blocks.push({ type: 'h1', content: line.slice(2) })
      }
      // 列表
      else if (line.startsWith('- ') || line.startsWith('* ')) {
        blocks.push({ type: 'li', content: line.slice(2) })
      } else if (/^\d+\.\s/.test(line)) {
        blocks.push({ type: 'oli', content: line.replace(/^\d+\.\s/, '') })
      }
      // 分割线
      else if (/^---+$/.test(line.trim())) {
        blocks.push({ type: 'hr' })
      }
      // 空行
      else if (line.trim() === '') {
        blocks.push({ type: 'br' })
      }
      // 普通段落
      else {
        blocks.push({ type: 'p', content: line })
      }
    }

    // 处理未闭合的代码块
    if (inCodeBlock && codeContent) {
      blocks.push({ type: 'code', lang: codeLang, content: codeContent.trimEnd() })
    }

    this.setData({ mdBlocks: blocks })
  },

  /** 一键复制全文 */
  onCopy() {
    const content = this.data.skill.content || ''
    wx.setClipboardData({
      data: content,
      success: () => wx.showToast({ title: '已复制到剪贴板', icon: 'success' }),
    })
  },

  /** 下载 MD 文件 */
  onDownload() {
    const skill = this.data.skill
    if (!skill) return
    const content = skill.content || ''
    const filePath = `${wx.env.USER_DATA_PATH}/${skill.title}.md`

    const fs = wx.getFileSystemManager()
    fs.writeFile({
      filePath,
      data: content,
      encoding: 'utf-8',
      success: () => {
        wx.openDocument({
          filePath,
          fileType: 'md',
          showMenu: true,
          success: () => log('Detail', '打开文档成功'),
          fail: (err) => {
            log('Detail', '打开文档失败', err)
            wx.showToast({ title: '已保存到本地', icon: 'success' })
          },
        })
      },
      fail: (err) => {
        log('Detail', '写入文件失败', err)
        wx.showToast({ title: '保存失败', icon: 'none' })
      },
    })
  },

  /** 收藏/取消收藏（乐观更新 + 心跳动画） */
  async onFavorite() {
    const app = getApp()
    if (!app.requireLogin()) return

    // 乐观更新：先翻转状态 + 触发动画
    const prev = this.data.isFavorited
    const next = !prev
    this.setData({ isFavorited: next, favAnimating: true })

    // 动画结束后移除动画 class
    setTimeout(() => this.setData({ favAnimating: false }), 400)

    try {
      const res = await post(`/api/skills/${this.skillId}/collect`)
      // 以服务端返回为准
      const serverState = !!res.collected
      this.setData({ isFavorited: serverState })
      wx.showToast({
        title: serverState ? '已收藏' : '已取消',
        icon: 'success',
        duration: 1200,
      })
    } catch (e) {
      // 失败时回滚
      this.setData({ isFavorited: prev })
      wx.showToast({ title: e.message || '操作失败', icon: 'none' })
    }
  },
})
