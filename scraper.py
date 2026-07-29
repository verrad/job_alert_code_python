import requests

# ISI DENGAN TOKEN & CHAT ID KAMU
TELEGRAM_TOKEN = "8924446972:AAEHAYNunKKY3ug9ZxyLw4SBvB5T8L8KbzM"
CHAT_ID = "5889763908"

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

if __name__ == "__main__":
    hasil = scrape_jobs()
    print(f"Ditemukan {len(hasil)} lowongan")
    
    # Ambil 5 lowongan pertama saja dulu buat tes (biar tidak spam ratusan pesan sekaligus)
    lowongan_untuk_dikirim = hasil[:10]
    
    pesan = "🔔 <b>Lowongan Kerja Terbaru</b>\n\n"
    for job in lowongan_untuk_dikirim:
        pesan += f"<b>{job['title']}</b>\n"
        pesan += f"🏢 {job['company']}\n"
        pesan += f"🔗 {job['link']}\n\n"
    
    hasil_kirim = kirim_ke_telegram(pesan)
    
    if hasil_kirim.get("ok"):
        print("✅ Pesan berhasil dikirim ke Telegram!")
    else:
        print("❌ Gagal kirim pesan:", hasil_kirim)