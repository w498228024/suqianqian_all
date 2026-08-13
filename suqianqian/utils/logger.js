/**
 * AI Skill 库 - 通用日志工具
 */

// ==================== 日志开关 ====================
// 开发环境设为 true，生产环境设为 false
const LOG_ENABLED = true

/**
 * 通用日志方法
 * @param {string} tag - 日志标签（模块名）
 * @param {string} msg - 日志内容
 * @param {*} data - 附加数据（可选）
 */
function log(tag, msg, data) {
  if (!LOG_ENABLED) return
  const time = new Date().toLocaleTimeString()
  const prefix = `[${time}][${tag}]`
  if (data !== undefined) {
    console.log(`${prefix} ${msg}`, data)
  } else {
    console.log(`${prefix} ${msg}`)
  }
}

/**
 * 错误日志
 */
function error(tag, msg, data) {
  if (!LOG_ENABLED) return
  const time = new Date().toLocaleTimeString()
  const prefix = `[${time}][${tag}]`
  if (data !== undefined) {
    console.error(`${prefix} ${msg}`, data)
  } else {
    console.error(`${prefix} ${msg}`)
  }
}

module.exports = { log, error, LOG_ENABLED }
