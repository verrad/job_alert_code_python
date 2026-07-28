import requests

def scrape_jobs():
    url = "https://remoteok.com/api"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Elemen pertama biasanya cuma metadata, bukan lowongan asli — kita skip
    jobs = data[1:]
    
    hasil = []
    for job in jobs:
        hasil.append({
            "title": job.get("position", "Tanpa judul"),
            "company": job.get("company", "Tanpa nama"),
            "link": job.get("url", "")
        })
    
    return hasil

if __name__ == "__main__":
    hasil = scrape_jobs()
    print(f"Ditemukan {len(hasil)} lowongan\n")
    for job in hasil[:5]:
        print(f"- {job['title']} di {job['company']}")
        print(f"  Link: {job['link']}\n")