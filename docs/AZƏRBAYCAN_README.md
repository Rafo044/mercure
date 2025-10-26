# 🤖 MERCUR-E GitHub Bot - Azərbaycan dilində təlimat

## 📋 Layihə haqqında

**MERCUR-E** - GitHub repozitoriyalarını avtomatlaşdırmaq üçün tam funksional GitHub App. FastAPI və FastMCP ilə qurulub, AI inteqrasiyası dəstəkləyir.

## ✨ Əsas xüsusiyyətlər

### Komandalar
- `/test [workflow]` - GitHub Actions workflow-unu işə sal
- `/merge [method]` - Pull request-i birləşdir (squash/merge/rebase)
- `/report` - Status hesabatı yarat

### Texnologiyalar
- **FastAPI** - Müasir Python web framework
- **PyGithub** - GitHub API client
- **FastMCP** - AI inteqrasiyası üçün
- **Docker** - Konteynerləşdirmə
- **Nginx** - Reverse proxy və TLS

## 🚀 Sürətli başlanğıc

### 1. Quraşdırma

```bash
cd githubbot
./setup.sh
```

### 2. Konfiqurasiya

`.env` faylını redaktə edin:

```bash
nano .env
```

Aşağıdakı məlumatları daxil edin:
```env
GITHUB_APP_ID=sizin_app_id
GITHUB_WEBHOOK_SECRET=sizin_webhook_secret
```

### 3. Private key əlavə edin

GitHub App-dan yüklədiyiniz `.pem` faylını əlavə edin:

```bash
# Private key faylını kopyalayın
cp ~/Downloads/mercur-e.pem ./private-key.pem
chmod 600 private-key.pem
```

### 4. Botu işə salın

```bash
./run_local.sh
```

Bot `http://localhost:8000` ünvanında işləyəcək.

### 5. ngrok ilə expose edin

Başqa terminalda:

```bash
ngrok http 8000
```

ngrok-dan HTTPS URL-ni kopyalayın və GitHub App webhook URL-nə əlavə edin.

## 📁 Layihə strukturu

```
githubbot/
├── main.py              # Əsas FastAPI tətbiqi
├── config.py            # Konfiqurasiya
├── github_auth.py       # GitHub autentifikasiyası
├── security.py          # Təhlükəsizlik
├── commands.py          # Komanda işləyiciləri
├── mcp_server.py        # AI inteqrasiyası
├── requirements.txt     # Python asılılıqları
├── Dockerfile          # Docker image
├── docker-compose.yml  # Docker Compose
├── nginx.conf          # Nginx konfiqurasiyası
├── README.md           # Əsas sənədləşmə (İngilis dilində)
└── AZƏRBAYCAN_README.md # Bu fayl
```

## 🔧 GitHub App yaratmaq

### 1. GitHub App yaradın

1. GitHub Settings → Developer settings → GitHub Apps
2. "New GitHub App" düyməsini klikləyin
3. Məlumatları doldurun:
   - **Name**: MERCUR-E
   - **Homepage URL**: Sizin domen və ya GitHub repo
   - **Webhook URL**: `https://your-domain.com/webhook`
   - **Webhook secret**: Təsadüfi güclü şifrə

### 2. İcazələri təyin edin

Repository permissions:
- **Actions**: Read & write
- **Contents**: Read & write
- **Issues**: Read & write
- **Pull requests**: Read & write
- **Workflows**: Read & write

### 3. Event-lərə abunə olun

- [x] Issue comment
- [x] Pull request
- [x] Push

### 4. Private key yaradın

1. "Private keys" bölməsinə keçin
2. "Generate a private key" düyməsini klikləyin
3. Yüklənən `.pem` faylını `private-key.pem` olaraq saxlayın

## 🧪 Test etmək

### Lokal test

1. Botu işə salın: `./run_local.sh`
2. ngrok işə salın: `ngrok http 8000`
3. GitHub App webhook URL-ni yeniləyin
4. Test repozitoriyasında issue və ya PR yaradın
5. Komment əlavə edin: `/test`
6. Botun cavabını gözləyin

### Komandaları test edin

```bash
# Test komandası
/test

# Xüsusi workflow ilə test
/test ci.yml

# PR-ı birləşdir
/merge squash

# Hesabat yarat
/report
```

## 🐳 Docker ilə deployment

### Docker Compose ilə

```bash
# Build və start
docker-compose up -d

# Logları görmək
docker-compose logs -f

# Dayandırmaq
docker-compose down
```

### Sadəcə Docker

```bash
# Image build et
docker build -t mercur-e-bot .

# Container işə sal
docker run -d \
  --name mercur-e-bot \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/private-key.pem:/app/private-key.pem:ro \
  --env-file .env \
  mercur-e-bot
```

## 🌐 Production deployment

### 1. Server hazırlığı

```bash
# Sistemi yenilə
sudo apt update && sudo apt upgrade -y

# Docker quraşdır
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Nginx quraşdır
sudo apt install nginx -y

# Certbot quraşdır (SSL üçün)
sudo apt install certbot python3-certbot-nginx -y
```

### 2. SSL sertifikatı əldə et

```bash
sudo certbot --nginx -d bot.sizindomen.com
```

### 3. Tətbiqi deploy et

```bash
# Layihə fayllarını serverə yüklə
cd /opt/mercur-e-bot

# .env konfiqurasiya et
nano .env

# Docker Compose ilə işə sal
docker-compose up -d
```

### 4. GitHub App webhook URL-ni yenilə

```
https://bot.sizindomen.com/webhook
```

## 🤖 AI inteqrasiyası

### FastMCP server işə sal

```bash
./run_mcp.sh
```

MCP server 8001 portunda işləyəcək.

### AI köməkçisi konfiqurasiya et

AI köməkçinizi MCP serverə qoşun:
```
http://localhost:8001
```

AI aşağıdakıları edə bilər:
- Kommentləri parse etmək
- PR-ları analiz etmək
- Komanda təklifləri vermək
- Hesabatlar yaratmaq

## 📚 Sənədləşmə

Ətraflı məlumat üçün:

- **README.md** - Tam sənədləşmə (İngilis dilində)
- **QUICKSTART.md** - 5 dəqiqəlik başlanğıc
- **DEPLOYMENT.md** - Production deployment təlimatı
- **TESTING.md** - Test təlimatları
- **AI_INTEGRATION.md** - AI inteqrasiyası
- **FAQ.md** - Tez-tez verilən suallar
- **SETUP_CHECKLIST.md** - Quraşdırma checklist

## 🔍 Problemlərin həlli

### Bot komandlara cavab vermir

1. Botun işlədiyini yoxlayın: `docker-compose ps`
2. Logları yoxlayın: `docker-compose logs -f`
3. GitHub App webhook deliveries-i yoxlayın
4. Webhook URL-nin düzgün olduğunu təsdiq edin

### Webhook signature validation xətası

1. `.env` faylındakı webhook secret-i yoxlayın
2. GitHub App settings-də webhook secret-i yoxlayın
3. Hər iki yerdə eyni olduğundan əmin olun

### Authentication xətaları

1. `GITHUB_APP_ID` düzgün olduğunu yoxlayın
2. `private-key.pem` faylının mövcud olduğunu yoxlayın
3. Botun repozitoriyada quraşdırıldığını təsdiq edin

## 🛠️ Faydalı komandalar

```bash
# Botu işə sal
./run_local.sh

# MCP server işə sal
./run_mcp.sh

# Quraşdırmanı yoxla
./verify_setup.sh

# Logları gör
tail -f logs/githubbot.log

# Docker logları
docker-compose logs -f

# Docker container-ləri yoxla
docker-compose ps

# Yenidən başlat
docker-compose restart
```

## 📊 Xüsusiyyətlər

### ✅ Hazır funksiyalar

- ✅ FastAPI webhook server
- ✅ GitHub App autentifikasiyası
- ✅ Webhook signature validation
- ✅ 3 slash komanda (/test, /merge, /report)
- ✅ GitHub Actions inteqrasiyası
- ✅ PR birləşdirmə
- ✅ Status hesabatları
- ✅ FastMCP AI inteqrasiyası
- ✅ Docker dəstəyi
- ✅ TLS/HTTPS dəstəyi
- ✅ PAM autentifikasiyası (opsional)
- ✅ Tam sənədləşmə

### 🔐 Təhlükəsizlik

- ✅ Webhook imza yoxlaması
- ✅ JWT autentifikasiyası
- ✅ TLS/HTTPS şifrələməsi
- ✅ Təhlükəsiz token saxlama
- ✅ Fayl silmə icazəsi yoxdur
- ✅ Rate limiting

## 🎯 İstifadə halları

1. **PR avtomatlaşdırması** - CI keçdikdən sonra avtomatik birləşdirmə
2. **Test işə salma** - Komment ilə test workflow-larını işə sal
3. **Status hesabatları** - PR və issue-lar üçün ətraflı hesabatlar
4. **AI köməyi** - AI ilə ağıllı PR analizi və tövsiyələr

## 📞 Dəstək

Problemlər və ya suallar üçün:

1. FAQ.md faylını yoxlayın
2. Logları nəzərdən keçirin
3. GitHub issue yaradın
4. Sənədləşməyə baxın

## 📝 Qeydlər

- Bütün fayllar İngilis dilində sənədləşdirilib
- Bu fayl yalnız əsas təlimatları əhatə edir
- Ətraflı məlumat üçün İngilis dilində sənədlərə baxın

## 🎉 Uğurlar!

MERCUR-E GitHub Bot-unuz hazırdır! 

Suallarınız varsa, sənədləşməyə baxın və ya issue yaradın.

**Xoş avtomatlaşdırma! 🤖**
