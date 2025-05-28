# ⚡ ProxyDDoS - 2025年最強效能的 CC 壓測工具
![License](https://img.shields.io/badge/license-MIT-green)  
> 🛡️ **ProxyDDoS** 是一款為 2025 年開發的 **壓力測試工具**，  
> 通過模擬真實用戶請求，幫助你測試網站的抗壓能力。
>
> 使用HTTP PROXY 最佳化模擬真實HTTP流量 

---

## 🚀 功能特色

- 🔹 **完整的請求標頭**  
 模擬標準瀏覽器行為 + 偽造 IP，提升真實度與效果。

- 🔹 **自動抓取並代理檢測**  
 全網最快速、最精準的代理檢測模組，省時高效。

- 🔹 **高穩定性**  
 多執行緒與記憶體管理完善，**不會出現 core dumped**！

- 🔹 **完全匿名**  
 將一些暴露敏感資訊的標頭寫死了 安全第一。

---

## 🖥️ 系統配置需求

| 項目       | 建議配置        |
|------------|-----------------|
| 處理器     | 4 核心以上      |
| 記憶體     | 8 GB 以上        |
| 網路速度   | 100 Mbps 以上   |

---

## 📦 安裝說明

### ✅ 下載專案
```bash
git clone https://github.com/GogoZin/ProxyDDoS
cd ProxyDDoS
```

### 🐧 Linux 安裝模組
```bash
pip3 install -r requirements.txt
```

### 🧊 Windows 安裝模組
```bash
py -m pip install -r requirements.txt
```

## 🏃 使用方式

### 🐧 Linux 執行命令
```bash
python3 proxyddos.py <GET/POST/HEAD> <host> <port> <threads> <path> <args>
```

### 🧊 Windows 執行命令
```bash
py proxyddos.py <GET/POST/HEAD> <host> <port> <threads> <path> <args>
```

### ✅ 範例
```bash
python3 proxyddos.py GET example.com 443 500 / --fetch
```
---

## 📜 授權條款

本專案使用 [MIT License](LICENSE)。

---

## ⚠️ 使用規章

> 📌 請注意：本工具僅供開發者學習與合法壓力測試用途。 
>  
> ❌ 禁止用於任何非法活動（如 DDoS 攻擊、未經授權的網站測試）。
> 
> 📄 使用本工具即表示您同意以上規章與 MIT 授權條款。
> 
> ⚖️ 作者對於任何非法用途造成的後果概不負責。
> 
> 🙅 不同意規章者請勿下載或使用本工具。
>
> ---

## 🌟 支持本專案

感謝使用 ProxyDDoS，歡迎 star ⭐ 支持！
