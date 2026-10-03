"""
DrixPay website v2 build script
Usage: python _src/build.py

  _src/pages/en/*.html  ->  site root      (default language)
  _src/pages/zh/*.html  ->  zh/

Placeholders available in page partials:
  {{i:icon-name}}  -> inline SVG icon
  {{card}}         -> DrixPay card visual
"""
import re
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "_src" / "pages"

# ---------------------------------------------------------------- icons
STROKE = '<svg class="ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
FILL = '<svg class="ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">{}</svg>'

ICONS = {
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "coins": '<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><path d="m16.71 13.88.7.71-2.82 2.82"/>',
    "bank": '<path d="M3 22h18"/><path d="M6 18v-7"/><path d="M10 18v-7"/><path d="M14 18v-7"/><path d="M18 18v-7"/><path d="m12 2 9 5H3z"/>',
    "layers": '<path d="m12 2 10 5-10 5L2 7z"/><path d="m2 17 10 5 10-5"/><path d="m2 12 10 5 10-5"/>',
    "transfer": '<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/><path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>',
    "exchange": '<path d="m17 2 4 4-4 4"/><path d="M3 11v-1a4 4 0 0 1 4-4h14"/><path d="m7 22-4-4 4-4"/><path d="M21 13v1a4 4 0 0 1-4 4H3"/>',
    "wallet": '<rect x="3" y="6" width="18" height="14" rx="2"/><path d="M3 10h18"/><path d="M16 15h2"/><path d="M6 6V5a2 2 0 0 1 2-2h8"/>',
    "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "check-circle": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "x-circle": '<circle cx="12" cy="12" r="10"/><path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "key": '<circle cx="7.5" cy="15.5" r="5.5"/><path d="m21 2-9.6 9.6"/><path d="m15.5 7.5 3 3L22 7l-3-3"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "user-check": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="m16 11 2 2 4-4"/>',
    "user-plus": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M19 8v6"/><path d="M22 11h-6"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "scan": '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3"/><path d="m16 16-1.9-1.9"/>',
    "ban": '<circle cx="12" cy="12" r="10"/><path d="m4.9 4.9 14.2 14.2"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "external": '<path d="M7 17 17 7"/><path d="M7 7h10v10"/>',
    "plus": '<path d="M12 5v14"/><path d="M5 12h14"/>',
    "menu": '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    "phone": '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M12 18h.01"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    "building": '<rect x="4" y="2" width="16" height="20" rx="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M12 6h.01"/><path d="M12 10h.01"/><path d="M12 14h.01"/><path d="M16 10h.01"/><path d="M16 14h.01"/><path d="M8 10h.01"/><path d="M8 14h.01"/>',
    "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
    "plane": '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
    "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    "monitor": '<rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/><path d="m10 7 5 3-5 3z"/>',
    "coffee": '<path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><path d="M6 2v2"/><path d="M10 2v2"/><path d="M14 2v2"/>',
    "nfc": '<path d="M8.5 7.5a6 6 0 0 1 0 9"/><path d="M12 5a10 10 0 0 1 0 14"/><path d="M5 10a2.5 2.5 0 0 1 0 4"/>',
    "percent": '<path d="M19 5 5 19"/><circle cx="6.5" cy="6.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "eye": '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>',
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/>',
    "store": '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M2 7h20v3a2 2 0 0 1-2 2 2.7 2.7 0 0 1-2-1 2.7 2.7 0 0 1-2 1 2.7 2.7 0 0 1-2-1 2.7 2.7 0 0 1-2 1 2.7 2.7 0 0 1-2-1 2.7 2.7 0 0 1-2 1 2 2 0 0 1-2-2z"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "terminal": '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "copy": '<rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    "incoming": '<path d="M17 7 7 17"/><path d="M17 17H7V7"/>',
    "trend": '<path d="m22 7-8.5 8.5-5-5L2 17"/><path d="M16 7h6v6"/>',
    "snow": '<path d="M2 12h20"/><path d="M12 2v20"/><path d="m20 16-4-4 4-4"/><path d="m4 8 4 4-4 4"/><path d="m16 4-4 4-4-4"/><path d="m8 20 4-4 4 4"/>',
}
FILLED = {
    "android": '<path d="M6 18c0 .55.45 1 1 1h1v3.5a1.5 1.5 0 003 0V19h2v3.5a1.5 1.5 0 003 0V19h1c.55 0 1-.45 1-1V8H6v10zM3.5 8C2.67 8 2 8.67 2 9.5v7c0 .83.67 1.5 1.5 1.5S5 17.33 5 16.5v-7C5 8.67 4.33 8 3.5 8zm17 0c-.83 0-1.5.67-1.5 1.5v7c0 .83.67 1.5 1.5 1.5s1.5-.67 1.5-1.5v-7c0-.83-.67-1.5-1.5-1.5zm-4.97-5.84l1.3-1.3c.2-.2.2-.51 0-.71-.2-.2-.51-.2-.71 0l-1.48 1.48A5.84 5.84 0 0012 1c-.96 0-1.86.23-2.66.63L7.85.15c-.2-.2-.51-.2-.71 0-.2.2-.2.51 0 .71l1.31 1.31A5.983 5.983 0 006 7h12c0-1.99-.97-3.75-2.47-4.84zM10 5H9V4h1v1zm5 0h-1V4h1v1z"/>',
    "apple": '<path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>',
}


def icon(name):
    if name in FILLED:
        return FILL.format(FILLED[name])
    if name not in ICONS:
        raise KeyError(f"unknown icon: {name}")
    return STROKE.format(ICONS[name])


CARD = """<div class="dcard" role="img" aria-label="DrixPay card">
  <div class="dcard-top"><img src="assets/img/logo-white.png" alt="" width="132" height="37">{{i:nfc}}</div>
  <div class="dcard-chip"></div>
  <div class="dcard-num">6523 •••• •••• 4256</div>
  <div class="dcard-bottom"><span>CARD HOLDER</span><div class="dcard-net"><span></span><span></span></div></div>
</div>"""



# ---------------------------------------------------------------- languages
LANG_MENU = [("en", "English"), ("zh", "简体中文"), ("zh-TW", "繁體中文"), ("ko", "한국어"), ("ja", "日本語"),
             ("ms", "Bahasa Melayu"), ("mn", "Монгол"), ("id", "Bahasa Indonesia"), ("th", "ไทย")]

LANG = {
    "en": {
        "dir": "", "prefix": "", "html_lang": "en", "og_locale": "en_US", "label": "English",
        "nav": [("index.html", "home", "Home"), ("products.html", "products", "Personal"),
                ("cooperation.html", "business", "Business"), ("security.html", "security", "Security"),
                ("about-us.html", "about", "About"), ("faq.html", "faq", "Help Center")],
        "skip": "Skip to main content", "home": "DrixPay home", "main_nav": "Main navigation",
        "mobile_nav": "Mobile navigation", "open_menu": "Open menu", "select_lang": "Select language",
        "download": "Download app", "soon": "{name} version coming soon",
        "footer_tagline": "Global payments powered by stablecoins.",
        "cols": [
            ("Personal", [("products.html#card", "DrixPay Card"), ("products.html#wallet", "Multi-currency wallet"),
                          ("products.html#transfer", "Transfers"), ("products.html#exchange", "Currency exchange"),
                          ("download.html", "Download app")]),
            ("Business", [("cooperation.html", "Card issuing API"), ("cooperation.html#whitelabel", "White-label cards"),
                          ("https://open.dxpayapp.com/", "Open Platform"), ("cooperation.html#contact", "Contact sales")]),
            ("Company", [("about-us.html", "About us"), ("security.html", "Security and compliance"),
                         ("lawyer-statement.html", "Legal statement")]),
            ("Support", [("faq.html", "Help center"), ("security.html#official", "Official channels"),
                         ("security.html#risk", "Risk disclosure"), ("mailto:support@drixpay.com", "Contact support")]),
        ],
        "risk": "<b>Risk disclosure:</b> Crypto asset prices are volatile and you may lose part or all of your funds. DrixPay has never promised fixed returns, principal protection or guaranteed profits. Use this service only where permitted by law.",
        "rights": "All rights reserved.",
        "reg": "Registered in Colorado, USA · FinCEN MSB No.",
    },
    "zh": {
        "dir": "zh", "prefix": "../", "html_lang": "zh-CN", "og_locale": "zh_CN", "label": "简体中文",
        "nav": [("index.html", "home", "首页"), ("products.html", "products", "个人服务"),
                ("cooperation.html", "business", "企业服务"), ("security.html", "security", "安全合规"),
                ("about-us.html", "about", "关于我们"), ("faq.html", "faq", "帮助中心")],
        "skip": "跳到主要内容", "home": "DrixPay 首页", "main_nav": "主导航",
        "mobile_nav": "移动端导航", "open_menu": "打开菜单", "select_lang": "选择语言",
        "download": "下载 App", "soon": "{name} 版本即将上线",
        "footer_tagline": "以稳定币驱动全球支付。",
        "cols": [
            ("个人", [("products.html#card", "DrixPay 卡"), ("products.html#wallet", "多币种钱包"),
                      ("products.html#transfer", "转账"), ("products.html#exchange", "货币兑换"),
                      ("download.html", "下载 App")]),
            ("企业", [("cooperation.html", "发卡 API"), ("cooperation.html#whitelabel", "白标卡"),
                      ("https://open.dxpayapp.com/", "开放平台"), ("cooperation.html#contact", "商务合作")]),
            ("公司", [("about-us.html", "关于我们"), ("security.html", "安全与合规"),
                      ("lawyer-statement.html", "平台声明")]),
            ("支持", [("faq.html", "帮助中心"), ("security.html#official", "官方渠道"),
                      ("security.html#risk", "风险提示"), ("mailto:support@drixpay.com", "联系客服")]),
        ],
        "risk": "<b>风险提示：</b>加密资产价格波动较大，可能导致部分或全部资金损失。DrixPay 从未承诺固定收益、保本或保证盈利。请在法律允许的地区使用本服务。",
        "rights": "保留所有权利。",
        "reg": "美国科罗拉多州注册 · FinCEN MSB 注册编号",
    },
}
SITE = "https://www.drixpay.com/"


def page_url(lang, file):
    path = "" if file == "index.html" else file
    return SITE + (LANG[lang]["dir"] + "/" if LANG[lang]["dir"] else "") + path


def switch_href(cur, target, file):
    """Relative link from the current page to the same page in another language."""
    if target == cur:
        return file
    if target == "en":
        return "../" + file
    return f"{LANG[target]['dir']}/{file}"


HEAD = """<!DOCTYPE html>
<html lang="{html_lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index, follow">
<meta name="author" content="DrixPay Innovations LLC">
<meta name="theme-color" content="#0a0e0b">
<meta name="format-detection" content="telephone=no">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{url_en}">
<link rel="alternate" hreflang="zh-Hans" href="{url_zh}">
<link rel="alternate" hreflang="x-default" href="{url_en}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="DrixPay">
<meta property="og:locale" content="{og_locale}">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:image" content="https://www.drixpay.com/image/down_bg.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<a class="skip-link" href="#main">{skip}</a>
"""


def header(lang, file, active):
    L = LANG[lang]
    cur = ' aria-current="page"'
    links = "".join(f'<a href="{h}"{cur if k == active else ""}>{t}</a>' for h, k, t in L["nav"])
    mlinks = "".join(f'<a href="{h}"{cur if k == active else ""}>{t}{{{{i:arrow}}}}</a>' for h, k, t in L["nav"])
    items, opts = [], []
    for code, name in LANG_MENU:
        checked = "true" if code == lang else "false"
        if code in LANG:
            href = switch_href(lang, code, file)
            items.append(f'<a role="menuitemradio" aria-checked="{checked}" hreflang="{LANG[code]["html_lang"]}" href="{href}">{name}</a>')
            opts.append(f'<option value="{href}"{" selected" if code == lang else ""}>{name}</option>')
        else:
            soon = L["soon"].format(name=name)
            items.append(f'<button role="menuitemradio" aria-checked="false" data-soon="{soon}">{name}</button>')
            opts.append(f'<option value="" data-soon="{soon}">{name}</option>')
    return f"""<header class="site-header">
  <div class="container">
    <a class="brand" href="index.html" aria-label="{L['home']}"><img src="assets/img/logo-white.png" alt="DrixPay" width="132" height="37"></a>
    <nav class="main-nav" aria-label="{L['main_nav']}">{links}</nav>
    <div class="header-actions">
      <div class="lang">
        <button class="lang-btn" aria-haspopup="true" aria-expanded="false">{{{{i:globe}}}}<span>{L['label']}</span></button>
        <div class="lang-menu" role="menu" aria-label="{L['select_lang']}">{"".join(items)}</div>
      </div>
      <a class="btn btn-primary btn-sm" href="download.html">{{{{i:download}}}}{L['download']}</a>
      <button class="nav-toggle" aria-label="{L['open_menu']}" aria-expanded="false" aria-controls="mobile-nav">{{{{i:menu}}}}</button>
    </div>
  </div>
</header>
<nav class="mobile-nav" id="mobile-nav" aria-label="{L['mobile_nav']}">
  {mlinks}
  <label class="mobile-lang">{{{{i:globe}}}}<select class="lang-select" aria-label="{L['select_lang']}">{"".join(opts)}</select></label>
  <a class="btn btn-primary" href="download.html">{{{{i:download}}}}{L['download']}</a>
</nav>
"""


def footer(lang):
    L = LANG[lang]
    cols = ""
    for title, links in L["cols"]:
        lis = ""
        for href, text in links:
            if href.startswith("http"):
                lis += f'<li><a href="{href}" target="_blank" rel="noopener">{text}{{{{i:external}}}}</a></li>'
            else:
                lis += f'<li><a href="{href}">{text}</a></li>'
        cols += f'<div class="footer-col"><h4>{title}</h4><ul>{lis}</ul></div>\n      '
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="assets/img/logo-white.png" alt="DrixPay" width="132" height="37">
        <p>{L['footer_tagline']}</p>
        <a class="mail" href="mailto:support@drixpay.com">{{{{i:mail}}}}support@drixpay.com</a>
      </div>
      {cols}
    </div>
    <div class="footer-risk">{L['risk']}</div>
    <div class="footer-bottom">
      <span>© <span data-year>2026</span> DrixPay Innovations LLC. {L['rights']}</span>
      <span>{L['reg']} <span class="mono">31000307531868</span></span>
    </div>
  </div>
</footer>
"""


SCRIPTS = {
    "qrcode": '<script src="https://cdn.jsdelivr.net/npm/qrcodejs@1.0.0/qrcode.min.js"></script>',
}


def phrase_breaks(text):
    """Headings use word-break: keep-all; add <wbr> after CJK punctuation so lines break between phrases."""
    def fix(m):
        return re.sub(r"([，、：；])(?!<br>|<wbr>)", r"\1<wbr>", m.group(0))
    return re.sub(r"<h[123][^>]*>.*?</h[123]>", fix, text, flags=re.S)


def render(text):
    text = text.replace("{{card}}", CARD)
    text = phrase_breaks(text)
    return re.sub(r"\{\{i:([a-z\-]+)\}\}", lambda m: icon(m.group(1)), text)


def parse(src):
    m = re.match(r"\s*<!--meta(.*?)-->", src, re.S)
    meta = {}
    for line in m.group(1).strip().splitlines():
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta, src[m.end():]


def build():
    for lang, L in LANG.items():
        out_dir = ROOT / L["dir"] if L["dir"] else ROOT
        out_dir.mkdir(exist_ok=True)
        for page in sorted((PAGES / lang).glob("*.html")):
            meta, body = parse(page.read_text(encoding="utf-8"))
            scripts = "".join(SCRIPTS[s] for s in meta.get("scripts", "").split() if s)
            html = (
                HEAD.format(title=meta["title"], description=meta["description"], html_lang=L["html_lang"],
                            og_locale=L["og_locale"], skip=L["skip"], canonical=page_url(lang, page.name),
                            url_en=page_url("en", page.name), url_zh=page_url("zh", page.name))
                + header(lang, page.name, meta["active"])
                + '<main id="main">\n' + body.strip() + "\n</main>\n"
                + footer(lang)
                + scripts
                + '<script src="assets/js/main.js"></script>\n</body>\n</html>\n'
            )
            html = render(html)
            if L["prefix"]:
                html = re.sub(r'((?:src|href)=")(assets/|favicon\.ico)', r"\1" + L["prefix"] + r"\2", html)
            (out_dir / page.name).write_text(html, encoding="utf-8")
            print("built", (L["dir"] + "/" if L["dir"] else "") + page.name)


if __name__ == "__main__":
    build()
