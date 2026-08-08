import requests
import time

# ISI DENGAN TOKEN BARU & CHAT ID KAMU
TELEGRAM_TOKEN = "your_telegram_token"
CHAT_ID = "your_telegram_id"

def scrape_jobs():
    url = "https://remoteok.com/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    jobs = data[1:]
    
    hasil = []
    for job in jobs:
        hasil.append({
            "title": job.get("position", "Tanpa judul"),
            "company": job.get("company", "Tanpa nama"),
            "link": job.get("url", "")
        })
    
    return hasil

def kirim_ke_telegram(pesan):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": pesan,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    response = requests.post(url, data=payload)
    return response.json()

def proses_dan_kirim():
    hasil = scrape_jobs()
    lowongan_untuk_dikirim = hasil[:10]
    
    pesan = "🔔 <b>Lowongan Kerja Terbaru</b>\n\n"
    for job in lowongan_untuk_dikirim:
        pesan += f"<b>{job['title']}</b>\n"
        pesan += f"🏢 {job['company']}\n"
        pesan += f"🔗 {job['link']}\n\n"
    
    kirim_ke_telegram(pesan)

def cek_pesan_baru(last_update_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
    params = {"offset": last_update_id + 1, "timeout": 30}
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    print("Bot aktif, menunggu perintah dari Telegram...")
    last_update_id = 0
    bot_aktif = True
    
    while bot_aktif:
        updates = cek_pesan_baru(last_update_id)
        
        for update in updates.get("result", []):
            last_update_id = update["update_id"]
            
            if "message" in update and "text" in update["message"]:
                teks = update["message"]["text"]
                print(f"Pesan diterima: {teks}")
                
                if teks == "/cari":
                    kirim_ke_telegram("🔍 Sedang mencari lowongan...")
                    proses_dan_kirim()
                elif teks == "/start":
                    kirim_ke_telegram("👋 Bot siap! Ketik /cari untuk cari lowongan terbaru.")
                elif teks == "/exit":
                    kirim_ke_telegram("Bot di matikan")
                    bot_aktif = False
                    break
        if not bot_aktif:
            break  
        time.sleep(1)
