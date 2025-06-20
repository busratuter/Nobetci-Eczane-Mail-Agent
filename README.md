# Nöbetçi Eczane Mail Agent

Bu proje, [agno agent framework](https://github.com/agno-agi/agno) kullanılarak geliştirilmiştir. Agno, zincirleme araçlar (tool chaining) ve doğal dil ile görev otomasyonu için modern bir Python agent altyapısı sunar. Bu sayede, projenin tüm iş akışı doğal dil promptları ile tetiklenebilir ve agent, arka planda tanımlı araçları (eczane verisi çekme, e-posta gönderme gibi) otomatik olarak zincirler.

Belirli bir il ve ilçe için nöbetçi eczaneleri çekip, sonucu e-posta ile gönderen bir Python agent uygulamasıdır.

## Özellikler
- Belirtilen şehir ve ilçe için nöbetçi eczaneleri webden çeker.
- Sonuçları Gmail SMTP ile belirttiğiniz e-posta adresine gönderir.
- Tamamen otomatik ve zincirleme agent mimarisi.

## Kurulum

1. **Depoyu klonlayın:**
   ```bash
   git clone https://github.com/kullaniciadi/nobetci-eczane-agent.git
   cd nobetci-eczane-agent
   ```
2. **Gerekli kütüphaneleri yükleyin:**
   ```bash
   pip install -r requirements.txt
   ```
3. **.env dosyasını oluşturun:**
   `.env.example` dosyasını kopyalayıp `.env` olarak adlandırın ve kendi Gmail bilgilerinizi girin.
   ```bash
   cp .env.example .env
   # .env dosyasını düzenleyin
   ```

## Gmail Uygulama Parolası
- Gmail hesabınızda 2 adımlı doğrulama aktif olmalı.
- [Google App Passwords](https://myaccount.google.com/apppasswords) üzerinden uygulama parolası oluşturun.
- Parolayı .env dosyasına boşluksuz olarak girin.

## Kullanım

```bash
python main.py
```

## Dosya Yapısı
- `main.py` : Giriş noktası, prompt ile agent'ı başlatır.
- `tools.py` : Eczane çekme ve mail gönderme fonksiyonları.
- `agent.py` : Agent tanımı ve zincirleme yapı.
- `nobetci_eczane_agent.py` : Alternatif agent/tool tanımları.

## Katkı
Pull request ve issue açabilirsiniz.

## Lisans
MIT
