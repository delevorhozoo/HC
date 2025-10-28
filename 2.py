import time
from datetime import datetime
from colorama import *
import requests
from requests.sessions import Session
import random
import threading
import concurrent.futures
import json

print(Fore.RED + '''
LORDHOZOO - TikTok Report Bot ULTRA FIXED
''' + Fore.WHITE)

tiktok_url = input("Enter tiktok report request url: ")

# Extended user agents untuk variasi lebih banyak
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
]

def get_proxies_multiple_sources():
    """Mendapatkan proxy dari BANYAK sumber berbeda dengan fallback"""
    
    proxy_sources = [
        # Free API sources
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=10000&country=all",
        "https://proxylist.geonode.com/api/proxy-list?protocols=http&limit=500&page=1&sort_by=lastChecked&sort_type=desc",
        "https://www.proxy-list.download/api/v1/get?type=http",
        
        # GitHub raw files
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt",
        "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
        "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt",
        
        # Additional sources
        "https://openproxylist.xyz/http.txt",
        "https://proxyspace.pro/http.txt",
        "https://multiproxy.org/txt_all/proxy.txt"
    ]
    
    all_proxies = []
    
    def fetch_proxies(source):
        try:
            print(Fore.CYAN + f"🔍 Fetching from: {source[:50]}...")
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                # Handle different response formats
                if 'geonode.com' in source:
                    # JSON format
                    data = response.json()
                    proxies = [f"{p['ip']}:{p['port']}" for p in data.get('data', [])]
                else:
                    # Text format
                    content = response.text.strip()
                    proxies = [p.strip() for p in content.split('\n') if p.strip()]
                
                print(Fore.GREEN + f"✅ Got {len(proxies)} proxies from {source[:30]}...")
                return proxies
        except Exception as e:
            print(Fore.RED + f"❌ Failed to fetch from {source[:30]}: {str(e)[:50]}")
        return []
    
    # Multi-threading untuk fetch proxy lebih cepat
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(fetch_proxies, proxy_sources)
        for result in results:
            all_proxies.extend(result)
    
    # Remove duplicates and invalid formats
    unique_proxies = list(set([p for p in all_proxies if ':' in p and p.count(':') == 1]))
    print(Fore.YELLOW + f"📊 Total unique proxies: {len(unique_proxies)}")
    return unique_proxies

def get_fallback_proxies():
    """Fallback proxy list jika semua sumber gagal"""
    fallback_proxies = [
        # Some common free proxies (might not work but worth trying)
        "45.77.56.213:3128",
        "138.197.157.32:3128", 
        "167.71.5.83:3128",
        "159.203.61.169:3128",
        "165.227.15.78:3128",
        "134.209.29.120:3128",
        "167.99.131.11:3128",
        "159.65.69.186:3128",
        "206.189.184.83:3128",
        "68.183.25.78:3128"
    ]
    return fallback_proxies

def test_proxy_advanced(proxy):
    """Test proxy dengan multiple test methods"""
    test_urls = [
        "http://httpbin.org/ip",
        "http://api.ipify.org",
        "http://icanhazip.com"
    ]
    
    for test_url in test_urls:
        try:
            response = requests.get(
                test_url, 
                proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, 
                timeout=5
            )
            if response.status_code == 200:
                print(Fore.GREEN + f"✅ Proxy {proxy} works via {test_url}")
                return True
        except:
            continue
    
    return False

def mass_proxy_test_advanced(proxies, max_workers=15):
    """Test banyak proxy dengan metode yang lebih baik"""
    working_proxies = []
    lock = threading.Lock()
    
    def test_and_collect(proxy):
        if test_proxy_advanced(proxy):
            with lock:
                working_proxies.append(proxy)
            return True
        return False
    
    print(Fore.CYAN + f"⚡ Testing {len(proxies)} proxies with {max_workers} workers...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Use list to force execution and show progress
        results = list(executor.map(test_and_collect, proxies))
    
    return working_proxies

def get_direct_connection_proxies():
    """Method tanpa proxy (direct connection) sebagai last resort"""
    return ["direct"] * 10  # Return list of "direct" for no proxy

print(Fore.CYAN + "🚀 Mengumpulkan proxy dari multiple sources...")
proxies = get_proxies_multiple_sources()

# Jika tidak ada proxy yang didapat, gunakan fallback
if not proxies:
    print(Fore.YELLOW + "⚠️  No proxies from online sources, using fallback...")
    proxies = get_fallback_proxies()

print(Fore.GREEN + f"✅ Found {len(proxies)} total proxies to test")

# Test proxy dengan multi-threading
print(Fore.CYAN + "⚡ Testing proxies dengan advanced method...")
working_proxies = mass_proxy_test_advanced(proxies[:200])  # Test 200 proxy pertama

# Jika masih tidak ada proxy yang bekerja, gunakan direct connection
if not working_proxies:
    print(Fore.YELLOW + "⚠️  No working proxies found, using direct connection method...")
    working_proxies = get_direct_connection_proxies()
    print(Fore.GREEN + "✅ Using DIRECT CONNECTION method (no proxy)")

print(Fore.GREEN + f"✅ {len(working_proxies)} methods bekerja siap spam!")

# Global counters
success_count = 0
fail_count = 0
lock = threading.Lock()

def send_report_advanced(proxy_method, attempt_id):
    """Fungsi untuk mengirim report dengan multiple methods"""
    global success_count, fail_count
    
    try:
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/json',
            'Referer': 'https://www.tiktok.com/',
            'Origin': 'https://www.tiktok.com',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }
        
        session = Session()
        session.headers.update(headers)
        
        # Prepare proxies config
        if proxy_method == "direct":
            proxy_config = None  # No proxy, direct connection
            proxy_display = "DIRECT"
        else:
            proxy_config = {'http': f'http://{proxy_method}', 'https': f'http://{proxy_method}'}
            proxy_display = proxy_method[:20]
        
        # Send request
        response = session.post(
            tiktok_url, 
            proxies=proxy_config,
            timeout=10,
            verify=False
        )
        
        with lock:
            success_count += 1
            now = datetime.now().strftime("%H:%M:%S")
            print(Fore.GREEN + f'[{now}] ✅ SPAM #{success_count} - Method: {proxy_display}...')
            
    except Exception as e:
        with lock:
            fail_count += 1
            now = datetime.now().strftime("%H:%M:%S")
            print(Fore.RED + f'[{now}] ❌ FAIL #{fail_count} - Error: {str(e)[:30]}...')

def ultra_spam_mode_fixed():
    """Mode spam ultra dengan fallback methods"""
    print(Fore.RED + "🔥🔥🔥 ULTRA SPAM MODE ACTIVATED! 🔥🔥🔥")
    print(Fore.YELLOW + "💣 Memulai spam unlimited dengan multiple methods...")
    
    thread_count = min(20, len(working_proxies) * 2)
    
    while True:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                # Submit unlimited tasks
                futures = []
                for i in range(500):  # Reduced for stability
                    method = random.choice(working_proxies)
                    future = executor.submit(send_report_advanced, method, i)
                    futures.append(future)
                
                # Tunggu sebagian selesai sebelum lanjut
                concurrent.futures.wait(futures, timeout=2)
                
                # Print status
                now = datetime.now().strftime("%H:%M:%S")
                print(Fore.CYAN + f"[{now}] 📊 STATUS: {success_count} Success | {fail_count} Failed")
                
        except Exception as e:
            print(Fore.RED + f"Error in main loop: {e}")
            continue

def direct_attack_mode():
    """Mode direct attack tanpa proxy"""
    print(Fore.RED + "🎯 DIRECT ATTACK MODE - NO PROXY!")
    print(Fore.YELLOW + "⚡ Using direct connection for maximum speed...")
    
    while True:
        try:
            send_report_advanced("direct", success_count + fail_count)
            time.sleep(0.1)  # Very short delay
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(Fore.RED + f"Direct attack error: {e}")
            time.sleep(1)

# Pilih mode spam
print(Fore.YELLOW + "\n🎛️  Pilih Mode Spam:")
print("1. ULTRA SPAM MODE (With Proxies)")
print("2. DIRECT ATTACK MODE (No Proxy - Fastest)")
print("3. CONTINUOUS SPAM MODE (Stable)")

choice = input("Pilih mode (1/2/3): ").strip()

if choice == "1":
    ultra_spam_mode_fixed()
elif choice == "2":
    direct_attack_mode()
else:
    # Continuous mode dengan direct connection fallback
    print(Fore.RED + "🎯 CONTINUOUS SPAM MODE!")
    
    spam_cycle = 0
    while True:
        spam_cycle += 1
        print(Fore.MAGENTA + f"\n🔄 SPAM CYCLE #{spam_cycle} - Starting attack...")
        
        # Gunakan ThreadPool untuk parallel requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for i in range(20):  # Reduced batch size
                method = random.choice(working_proxies)
                future = executor.submit(send_report_advanced, method, i)
                futures.append(future)
            
            concurrent.futures.wait(futures, timeout=3)
        
        # Status update
        now = datetime.now().strftime("%H:%M:%S")
        print(Fore.CYAN + f"[{now}] 🚀 CYCLE #{spam_cycle} COMPLETE - Total: {success_count} Success | {fail_count} Failed")
        
        time.sleep(1)
