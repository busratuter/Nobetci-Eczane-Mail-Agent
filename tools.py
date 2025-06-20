from agno.tools.decorator import tool
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os


@tool
def nobetci_eczane_cek(il: str, ilce: str) -> str:
    """
    Belirtilen il ve ilçedeki nöbetçi eczaneleri çeker.
    Args:
        il (str): Şehir adı (örn: 'İstanbul')
        ilce (str): İlçe adı (örn: 'Kadıköy')
    Returns:
        str: Eczane listesi (her eczane için ad, adres, telefon)
    """
    print(f"[DEBUG] Eczane verisi çekiliyor: il={il}, ilce={ilce}")

    # urlde türkçe karakterler olamayacağı için bunları dönüştürüyoruz
    tr_map = {'ş': 's', 'Ş': 'S', 'ı': 'i', 'İ': 'I', 'ğ': 'g', 'Ğ': 'G', 'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C'}
    
    # türkçe karakterleri ASCII karşılıkları ile değiştirip sonra hepsini küçük harfe çeviriyoruz
    il_clean = il
    ilce_clean = ilce
    for key, value in tr_map.items():
        il_clean = il_clean.replace(key, value)
        ilce_clean = ilce_clean.replace(key, value)
    
    il_clean = il_clean.lower()
    ilce_clean = ilce_clean.lower()
    
    url = f"https://www.eczaneler.gen.tr/nobetci-{il_clean}-{ilce_clean}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"[DEBUG] Hata: Sayfa alınamadı. Status code: {response.status_code}")
        return f"{il} {ilce} için nöbetçi eczane bilgisi alınamadı."

    soup = BeautifulSoup(response.text, 'html.parser')
    eczaneler = []
    
    # site verileri bir tablo içinde gösteriyor. bu yüzden tablodaki her bir satırı (tr) seçiyoruz
    for row in soup.select("table.table tr"):
        if row.find('th'): 
            continue
        
        name_tag = row.select_one("a")
        if not name_tag:
            continue
            
        ad = name_tag.text.strip()
        cell_text = row.select_one("td").text
        
        try:
            # adres ve telefonu, hücredeki tüm metinden eczane adını çıkararak ayırmaya çalışıyoruz
            address_part = cell_text.replace(ad, '').strip()
            
            # telefon numarasını metnin sonundaki sayısal ifadeden buluyoruz.
            tel_start_index = -1
            for i in range(len(address_part) - 1, 0, -1):
                if address_part[i].isdigit() and not address_part[i-1].isalpha():
                    tel_start_index = i
                    while tel_start_index > 0 and (address_part[tel_start_index-1].isdigit() or address_part[tel_start_index-1] in '() -'):
                         tel_start_index -= 1
                    break
            
            if tel_start_index != -1:
                adres = address_part[:tel_start_index].strip()
                tel = address_part[tel_start_index:].strip()
            else:
                adres = address_part
                tel = "Telefon bulunamadı"

        except Exception:
            adres = "Adres ayrıştırılamadı"
            tel = "Telefon ayrıştırılamadı"

        eczaneler.append(f"{ad}\nAdres: {adres}\nTel: {tel}\n")

    print(f"[DEBUG] {len(eczaneler)} eczane bulundu.")
    if not eczaneler:
        return f"{il} {ilce} için nöbetçi eczane bulunamadı. Lütfen URL'yi veya site yapısını kontrol edin."
        
    return '\n---\n'.join(eczaneler)

from dotenv import load_dotenv
load_dotenv()

@tool
def mail_gonder(to: str, subject: str, content: str) -> str:
    user = os.getenv("GMAIL_USER")
    password = os.getenv("GMAIL_PASSWORD")

    if not user or not password:
        return "GMAIL_USER veya GMAIL_PASSWORD ortam değişkeni bulunamadı!"
    msg = MIMEText(content)
    msg["Subject"] = subject
    msg["From"] = user
    msg["To"] = to
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(user, password)
        server.sendmail(user, [to], msg.as_string())

    print("[DEBUG] Mail gönderildi!")
    
    return "E-posta gönderildi."
