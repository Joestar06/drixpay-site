# DrixPay 官网 v2

纯静态多页站点，无框架依赖。双击 `index.html` 即可预览。

- **英文（默认）**：站点根目录 `/`
- **简体中文**：`/zh/`
- 页头语言菜单可在两种语言间切换同一页面；其余 7 种语言显示"即将上线"

## 页面

| 文件 | 英文 | 中文 |
|---|---|---|
| `index.html` | Home | 首页 |
| `products.html` | Personal | 个人服务 |
| `cooperation.html` | Business | 企业服务（沿用旧 URL） |
| `security.html` | Security | 安全合规 |
| `about-us.html` | About | 关于我们（沿用旧 URL） |
| `faq.html` | Help Center | 帮助中心（沿用旧 URL） |
| `lawyer-statement.html` | Legal statement | 平台声明（沿用旧 URL，原文保留） |
| `download.html` | Download | 下载 |

## 修改方式

**不要直接改根目录或 `zh/` 下的 html**，改 `_src` 后运行：

```
python _src/build.py
```

- 页面正文：`_src/pages/en/*.html`、`_src/pages/zh/*.html`（两种语言结构一致，改一边记得同步另一边）
- 公共头部、尾部、导航文案、图标：`_src/build.py`（`LANG` 字典）
- 样式：`assets/css/style.css`
- 脚本：`assets/js/main.js`
- 新增语言：在 `LANG` 中加一项，并新建 `_src/pages/<语言>/`

## 文案原则

官方、陈述式。不用口号、反问句、比喻和营销形容词；中文使用"您"。金额与界面截图均标注为示例。

## 上线前待确认

- [ ] 香港牌照的具体类型与编号；"受香港金管局监管"的表述需法务确认
- [ ] Logo 提供 SVG 矢量版（现为 132×37 PNG，高分屏略糊）
- [ ] 费率、限额、支持币种、可用地区（页面目前写"以 App 内为准"）
- [ ] 补充《用户协议》《隐私政策》页面
- [ ] 其余 7 种语言的翻译
- [ ] 服务器配置旧路径 301 跳转：`/cooperation` `/about-us` `/lawyer-statement` `/faq` → 对应 `.html`
