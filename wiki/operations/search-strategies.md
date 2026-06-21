# B2B 外贸搜索策略（吸收自 Codex foreign-trade-lead-agent）

## 通用搜索模式

```
{product} importer {country}
{product} wholesaler {country}
{product} distributor {country}
{product} buyer {country}
{product} procurement {country}
{product} official website contact {country}
{product} vendor OR supplier OR procurement {country}
{product} wholesale directory {country}
{product} exhibitor OR trade show {country}
{product} contact email WhatsApp {country}
```

## 决策人搜索

```
{product} "Purchasing Manager" {country} email
{product} "Procurement Manager" {country} WhatsApp
{product} "Sourcing Manager" distributor {country}
{product} "Import Manager" importer {country}
```

## 中国采购意图（客户从中国采购）

```
{product} importer source from China {country}
{product} buyer China supplier {country}
{product} distributor China sourcing {country}
{product} private label importer China {country}
```

## 按国家/地区策略

### 美国
- 关键词: importer, distributor, wholesale, retail chain, Amazon seller, promotional products, procurement
- 渠道: 官网, Thomasnet, 展会名录, 行业协会

### 欧洲（德国为主）
- 关键词: importer, distributor, wholesaler, EU, GmbH, B2B, trade fair, Messe
- 渠道: Europages, Kompass, 展会名录, 官方经销商网站

### 中东
- 关键词: UAE, Dubai, Saudi, distributor, trading, import, project supplier, hotel supplier
- 渠道: 商会名录, 贸易名录, 展会页面, 贸易公司官网

### 俄罗斯/CIS
- 关键词: importer, distributor, wholesale, официальный сайт, контакты, поставщик, оптом
- 中英双语 + 本地语言关键词

### 拉丁美洲
- 关键词: importador, distribuidor, mayorista, proveedor, contacto, WhatsApp
- 英语 + 西班牙语/葡萄牙语关键词

## LinkedIn 公司页面搜索

```
site:linkedin.com/company {product} importer {country}
site:linkedin.com/company {product} distributor {country}
site:linkedin.com/company {product} wholesaler {country}
```

仅用于公开公司证据，不爬个人资料。

## 线索资质评分

| 维度 | 分值 |
|---|---|
| 产品相关度 | 30 |
| 客户类型匹配 | 20 |
| 市场/国家匹配 | 15 |
| 联系方式完整度 | 20 |
| 来源可信度 | 15 |
| **总分** | **100** |

## 线索分级

| 级别 | 含义 |
|---|---|
| 正式线索 | 有公开来源+产品相关+可联系 |
| 待验证候选 | 有来源但联系方式不全或证据弱 |
| 不达标跳过 | 缺来源/缺联系/不相关 |
| 重复已跳过 | 按域名/公司/邮箱/WhatsApp去重 |

## 证据等级

| 等级 | 含义 | 用途 |
|---|---|---|
| A | 官网或官方联系页证明公司和联系方式 | 正式线索 |
| B | B2B/展会/协会页面证明公司和联系方式 | 正式线索（若联系和匹配够强） |
| C | 公开公司社媒页面证明存在但无联系方式 | 候选，需其他来源确认 |
| D | 搜索摘要或弱目录 | 不作为正式线索 |

## 开发信角度（按客户类型）

| 客户类型 | 切入角度 |
|---|---|
| Importer | 稳定供应、出口文件、整柜/散货能力 |
| Wholesaler | 批发价、MOQ、包装、产品范围 |
| Distributor | 品类匹配、区域供应、OEM/私有品牌 |
| Retailer | 零售包装、试单、货架-ready款式 |
| E-commerce seller | 快速打样、变体、包装、市场平台兼容规格 |
| Hotel/Hospitality | 耐用性、补货、批量供应 |
| Promotional gift | Logo定制、包装、打样周期 |

## 去重规则

按以下字段去重：
- 标准化网站域名
- 标准化公司名
- 精确邮箱
- WhatsApp号码
- 电话号码
- 联系页面URL

---

Source: 小红书Codex项目 foreign-trade-lead-agent by zhangruiying12138-web
Absorbed: 2026-06-21
