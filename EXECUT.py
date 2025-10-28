import time
from datetime import datetime
from colorama import *
import requests
from requests.sessions import Session
import random
import threading
import concurrent.futures

print(Fore.RED + '''
LORDHOZOO - TikTok Report Bot ULTRA
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

def get_proxies():
    """Mendapatkan proxy dari berbagai sumber dengan lebih cepat"""
    proxy_sources = [
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
        "https://api.proxyscrape.com/v2/?request=getproxies&protocol=https&timeout=5000&country=all",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
        "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
        "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTP_RAW.txt"
    ]
    
    all_proxies = []
    
    def fetch_proxies(source):
        try:
            response = requests.get(source, timeout=5)
            if response.status_code == 200:
                proxies = response.text.strip().split('\n')
                return [p.strip() for p in proxies if p.strip()]
        except:
            pass
        return []
    
    # Multi-threading untuk fetch proxy lebih cepat
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = executor.map(fetch_proxies, proxy_sources)
        for result in results:
            all_proxies.extend(result)
    
    return list(set(all_proxies))

def test_proxy_fast(proxy):
    """Test proxy dengan timeout sangat singkat"""
    try:
        test_url = "http://httpbin.org/ip"
        response = requests.get(test_url, 
                              proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'}, 
                              timeout=3)
        return response.status_code == 200
    except:
        return False

def mass_proxy_test(proxies, max_workers=20):
    """Test banyak proxy sekaligus dengan multi-threading"""
    working_proxies = []
    
    def test_and_collect(proxy):
        if test_proxy_fast(proxy):
            working_proxies.append(proxy)
            return True
        return False
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(test_and_collect, proxies)
    
    return working_proxies

print(Fore.CYAN + "🚀 Mengumpulkan proxy dengan ultra speed...")
proxies = get_proxies()
print(Fore.GREEN + f"✅ Found {len(proxies)} total proxies")

# Test proxy dengan multi-threading
print(Fore.CYAN + "⚡ Testing proxies dengan multi-threading...")
working_proxies = mass_proxy_test(proxies[:100])  # Test 100 proxy pertama

print(Fore.GREEN + f"✅ {len(working_proxies)} proxy bekerja siap spam!")

if not working_proxies:
    print(Fore.RED + "❌ Tidak ada proxy yang bekerja!")
    input('Press Enter to close the program')
    exit()

# Global counters
success_count = 0
fail_count = 0
lock = threading.Lock()

def send_report(proxy, attempt_id):
    """Fungsi untuk mengirim report dengan kecepatan maksimal"""
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
        
        # Timeout sangat singkat untuk kecepatan maksimal
        response = session.post(
            tiktok_url, 
            proxies={'http': f'http://{proxy}', 'https': f'http://{proxy}'},
            timeout=5,  # Timeout pendek untuk speed
            verify=False  # Nonaktifkan SSL verification untuk speed
        )
        
        with lock:
            success_count += 1
            now = datetime.now().strftime("%H:%M:%S")
            print(Fore.GREEN + f'[{now}] ✅ SPAM #{success_count} - Proxy: {proxy[:20]}...')
            
    except Exception as e:
        with lock:
            fail_count += 1
            now = datetime.now().strftime("%H:%M:%S")
            print(Fore.RED + f'[{now}] ❌ FAIL #{fail_count} - Proxy: {proxy[:20]}...')

def ultra_spam_mode():
    """Mode spam ultra dengan multi-threading maksimal"""
    print(Fore.RED + "🔥🔥🔥 ULTRA SPAM MODE ACTIVATED! 🔥🔥🔥")
    print(Fore.YELLOW + "💣 Memulai spam unlimited dengan kecepatan maksimal...")
    
    thread_count = min(50, len(working_proxies) * 2)  # Gunakan lebih banyak thread
    
    while True:
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=thread_count) as executor:
                # Submit unlimited tasks
                futures = []
                for i in range(1000):  # Unlimited spam loop
                    proxy = random.choice(working_proxies)
                    future = executor.submit(send_report, proxy, i)
                    futures.append(future)
                
                # Tunggu sebagian selesai sebelum lanjut
                concurrent.futures.wait(futures, timeout=1)
                
                # Print status setiap 10 detik
                now = datetime.now().strftime("%H:%M:%S")
                print(Fore.CYAN + f"[{now}] 📊 STATUS: {success_count} Success | {fail_count} Failed | Threads: {thread_count}")
                
        except Exception as e:
            print(Fore.RED + f"Error in main loop: {e}")
            continue

def continuous_spam():
    """Spam continuous dengan rotasi proxy"""
    print(Fore.RED + "🎯 CONTINUOUS SPAM MODE!")
    
    spam_cycle = 0
    while True:
        spam_cycle += 1
        print(Fore.MAGENTA + f"\n🔄 SPAM CYCLE #{spam_cycle} - Starting massive attack...")
        
        # Gunakan ThreadPool untuk parallel requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            # Buat batch requests
            batch_size = min(50, len(working_proxies))
            futures = []
            
            for i in range(batch_size):
                proxy = working_proxies[i % len(working_proxies)]
                future = executor.submit(send_report, proxy, i)
                futures.append(future)
            
            # Tunggu batch selesai
            concurrent.futures.wait(futures, timeout=2)
        
        # Status update
        now = datetime.now().strftime("%H:%M:%S")
        print(Fore.CYAN + f"[{now}] 🚀 CYCLE #{spam_cycle} COMPLETE - Total: {success_count} Success | {fail_count} Failed")
        
        # Very short delay antara cycles
        time.sleep(0.5)

# Pilih mode spam
print(Fore.YELLOW + "\n🎛️  Pilih Mode Spam:")
print("1. ULTRA SPAM MODE (Maximum Speed)")
print("2. CONTINUOUS SPAM MODE (Stable)")
choice = input("Pilih mode (1/2): ").strip()

if choice == "1":
    ultra_spam_mode()
else:
    continuous_spam()
