# ⚡ ProxyDDoS - The Most Powerful CC Stress Testing Tool of 2025
![License](https://img.shields.io/badge/license-MIT-green)  
> 🛡️ **ProxyDDoS** is a **DDoS stress testing tool** designed for 2025,
> simulating real user traffic to help evaluate your website’s resilience under load.
>
> Optimized with HTTP PROXY to mimic realistic traffic
> Supports Cloudflare, Google Shell, and other CDN services.

---

## 🚀 Key Features

- 🔹 **Complete Request Headers**  
 Simulates real browser behavior with spoofed IPs to increase authenticity and effectiveness.

- 🔹 **Auto Proxy Scraping & Validation**  
 Fastest and most accurate proxy checker—saves your time and boosts reliability.

- 🔹 **Rock-Solid Stability**  
 Built with proper multithreading and memory handling—**no core dumps!**

- 🔹 **Truly Anonymous**  
 Sensitive headers are hardcoded to prevent leaks. Your privacy is a priority.

---

## 🖥️ System Requirements

| Component       | Recommended Spec        |
|------------|-----------------|
| CPU     | 4 cores or more      |
| RAM     | At least 8 GB        |
| Network   | 100 Mbps or faster   |

---

## 📦 Installation

### ✅ Clone the Project
```bash
git clone https://github.com/GogoZin/ProxyDDoS
cd ProxyDDoS
```

### 🐧 For Linux
```bash
pip3 install -r requirements.txt
```

### 🧊 For Windows
```bash
py -m pip install -r requirements.txt
```

## 🏃 How to Use

### 🐧 Linux Run Command
```bash
python3 proxyddos.py <GET/POST/HEAD> <host> <port> <threads> <path> <args>
```

### 🧊 Windows Run Command
```bash
py proxyddos.py <GET/POST/HEAD> <host> <port> <threads> <path> <args>
```

### ✅ Example
```bash
python3 proxyddos.py GET example.com 443 500 / --fetch
```
---

## 📜 License

This project is licensed under the [MIT License](LICENSE)。

---

## ⚠️ Terms of Use

> 📌 Important：This tool is for educational and legal stress testing purposes only.
>  
> ❌ DO NOT use it for illegal activities (e.g. DDoS attacks, unauthorized testing).
> 
> 📄 By using this tool, you agree to these terms and the MIT license.
> 
> ⚖️ The author is not responsible for any consequences resulting from misuse.
> 
> 🙅 If you do not agree with the terms, do not download or use this tool.
>
> ---

## 🌟 Support & Some Quick Insights

Let’s say you send 400 requests—some proxies might not relay all of them.

That’s because each proxy has different speeds, limits, and behaviors.

You might see the same proxy IP show up with different ports.

That’s totally normal—it’s because each port has different performance (or it might even be a honeypot 👀).

If you want more consistent results, stick to paid private proxies.

Public proxies? Honestly, most of them are slow, unreliable, and unsafe.

That’s also why we hardcode the sensitive headers—for your safety.

If you like this project, don’t forget to leave a Star ⭐ Thanks for the support!
