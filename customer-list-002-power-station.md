# 便携储能电源 — 已验证潜在客户清单
## 2026-06-03 更新（SMTP+官网+退信三重验证）

### 验证状态说明
- ✅ 有效：官网发布 + SMTP通过 或 Google catchall + 官网确认
- ⚠️ 待验证：Google catchall，官网有地址但无法SMTP确认
- 🚫 已死：PostMaster退信确认不存在
- 🔒 拒收：地址存在但服务器拒绝（发信声誉问题）

---

## 一、阿联酋/中东

### 1. Power & Sun UAE
- 网站：powernsun.com
- 邮箱：info@powernsun.com ⚠️（官网有但Zoho拒绝SMTP探针，无退信记录）
- 备用：info@powernsun.co.za, info@powernsun.in
- 业务：太阳能板、逆变器、电池供应商

### 2. EcoSmart International
- 网站：ecosmart-intl.com
- 邮箱：dubai@ecosmart-intl.com ⚠️（Google catchall，官网确认存在）
- 备用：contact@ecosmart-intl.com, info@ecosmart-intl.com, blr@ecosmart-intl.com
- 业务：能源解决方案，迪拜+班加罗尔双办公室

### 3. Solar Concierge Dubai 🚫
- 网站：solar-dubai.com
- 邮箱：help@solar-dubai.com 🚫（Google退信：does not exist）
- 替代方案：网站无其他公开发布邮箱，LinkedIn联系

---

## 二、菲律宾

### 4. Solar Philippines
- 网站：solarphilippines.ph
- 邮箱：inquiries@solarphilippines.ph ⚠️（官网有但Outlook拒绝SMTP探针，无退信记录）
- 业务：菲律宾太阳能安装

---

## 三、印度

### 5. Luminous Solar
- 网站：luminoussolar.com
- 邮箱：sales@luminoussolar.com ⚠️（Google catchall，官网确认存在）
- 业务：商业/农业/非营利太阳能方案

### 6. Su-Kam India
- 网站：su-kam.com
- 邮箱：customercare@su-kam.com ✅（Microsoft 365 SMTP确认有效）
- 业务：逆变器电池+太阳能方案

### 7. UTL
- 网站：utl.co.in
- 邮箱：info@utl.co.in ⚠️（SMTP超时，无退信记录）

---

## 四、东南亚零售商

| 公司 | 邮箱 | 状态 | 说明 |
|------|------|------|------|
| Selis Indonesia | candra.hermawan@selis.co.id | ⚠️ Google catchall | 官网确认 |
| ACE Hardware | customer.care@acehardware.co.id | 🔒 拒收 | Outlook 5.4.1 Access denied |
| Electronic City | cs@electroniccity.co.id | 🚫 已死 | PostMaster退信 |
| HomePro | customer.service@homepro.co.th | 🚫 已死 | 5.1.1 用户不存在 |
| Advice | contact@advice.co.th | 🚫 已死 | Google 5.1.1 不存在 |
| JIB | info@jib.co.th | 🔒 拒收 | Outlook 5.4.1 Access denied |
| FPT Shop | hotro@fpt.com.vn | 🔒 拒收 | Outlook 5.4.1 Access denied |
| Dien May Xanh | cskh@thegioididong.com | 🚫 已死 | 域名无MX记录，curl 000 |

---

## 五、全球

### 8. Inverter Supply
- 网站：invertersupply.com
- 邮箱：support@invertersupply.com ⚠️（SMTP超时，无退信记录）

### 9. The Solar Store
- 网站：thesolarstore.com
- 邮箱：info@thesolarstore.com ⚠️（Google catchall，官网确认存在）

### 10. Solar Panel Store
- 网站：solarpanelstore.com
- 邮箱：info@solarpanelstore.com ⚠️（Google catchall，官网确认存在）

---

## 优先发送顺序（6/3更新）

**可发送（8家）：**
Su-Kam ✅ → Luminous → EcoSmart → Solar Philippines → Power & Sun → Selis → The Solar Store → Solar Panel Store

**不可发送（7家死+3家拒收）：**
Solar Dubai 🚫, ACE Hardware 🔒, Electronic City 🚫, HomePro 🚫, Advice 🚫, JIB 🔒, FPT Shop 🔒, Dien May Xanh 🚫

**不确定（2家）：**
UTL（SMTP超时）, Inverter Supply（SMTP超时）

---

*验证方法：2026-06-03 SMTP RCPT TO + PostMaster退信记录交叉验证。Google catchall域名通过curl抓取官网确认地址发布。*
