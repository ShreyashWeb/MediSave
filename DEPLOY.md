# MediSave Deployment & Operations Guide

This guide details deployment options for **MediSave**, ranging from local development with Docker Compose to production deployment on cloud infrastructure (AWS/GCP/DigitalOcean) with Ollama Gemma 4 acceleration.

---

## 📋 Architecture Overview

MediSave consists of three interconnected components:

1. **Frontend PWA:** Static HTML5/CSS/JavaScript with Service Worker caching (`/frontend`). Can be served directly by FastAPI or hosted separately on a static CDN (Vercel, Cloudflare Pages, Netlify).
2. **Backend REST API:** Lightweight FastAPI service in Python (`/backend`) providing RapidFuzz search, pricing normalization, and Ollama bridge.
3. **Local LLM Engine:** Ollama instance serving the **Gemma 4** open-weights model on `http://localhost:11434`.

---

## Option 1: Docker Compose (All-in-One Local / VPS)

The fastest way to deploy MediSave with automated container networking:

### `docker-compose.yml`

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: medisave-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_models:/root/.ollama
    restart: unless-stopped
    # Optional GPU support (uncomment if NVIDIA GPU is available):
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]

  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    container_name: medisave-backend
    ports:
      - "8000:8000"
    environment:
      - GEMMA_BASE_URL=http://ollama:11434
      - GEMMA_MODEL=gemma4
      - GEMMA_TIMEOUT_SECONDS=45.0
      - ALLOWED_ORIGINS=*
    depends_on:
      - ollama
    restart: unless-stopped

volumes:
  ollama_models:
```

### Starting the Stack

```bash
# 1. Start containers
docker compose up -d

# 2. Pull Gemma 4 model into the Ollama container
docker exec -it medisave-ollama ollama pull gemma4

# 3. Verify health
curl http://localhost:8000/api/health
```

MediSave is now live at `http://localhost:8000`.

---

## Option 2: Production Cloud VM (Ubuntu 22.04 / 24.04 LTS)

### Recommended Hardware
- **CPU:** 4+ vCPUs (x86_64 or ARM64)
- **RAM:** 8 GB RAM minimum (16 GB recommended for Gemma 4 7B/9B quantized)
- **Disk:** 40 GB NVMe SSD
- **GPU (Optional):** NVIDIA T4, A10G, or RTX 3060+ for sub-second vision perception

### Step-by-Step Installation

#### 1. System Setup
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv git curl nginx
```

#### 2. Install and Configure Ollama
```bash
curl -fsSL https://ollama.ai/install.sh | sh

# Enable Ollama systemd service
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull Gemma 4 model
ollama pull gemma4
```

#### 3. Clone Repository & Setup Virtual Environment
```bash
cd /var/www
sudo git clone https://github.com/your-username/medisave.git
cd medisave
sudo chown -R $USER:$USER /var/www/medisave

python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python scripts/build_dataset.py
```

#### 4. Configure Systemd Service for MediSave Backend
Create `/etc/systemd/system/medisave.service`:

```ini
[Unit]
Description=MediSave FastAPI Service
After=network.target ollama.service

[Service]
User=ubuntu
WorkingDirectory=/var/www/medisave
ExecStart=/var/www/medisave/venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --workers 4
Restart=always
Environment="GEMMA_BASE_URL=http://127.0.0.1:11434"
Environment="GEMMA_MODEL=gemma4"

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable medisave
sudo systemctl start medisave
```

#### 5. Configure Nginx Reverse Proxy with SSL (Certbot)
Create `/etc/nginx/sites-available/medisave`:

```nginx
server {
    server_name medisave.yourdomain.com;

    # Client-side max body size for photo uploads (max 10MB)
    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Enable gzip compression for fast mobile loading
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
```

Enable site and acquire SSL certificate:
```bash
sudo ln -s /etc/nginx/sites-available/medisave /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Install Let's Encrypt SSL
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d medisave.yourdomain.com
```

---

## Option 3: Testing on Real Smartphones via Cloudflare Tunnel / Ngrok

Testing mobile camera capture and barcode scanning requires HTTPS on mobile devices.

### Using Cloudflare Quick Tunnel (Free & Instant)
```bash
# Start your local MediSave server
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# In a separate terminal, launch Cloudflare Tunnel
cloudflared tunnel --url http://localhost:8000
```
`cloudflared` outputs a secure HTTPS URL (e.g. `https://random-words.trycloudflare.com`).  
Open this URL on your mobile phone's browser to test camera prescription scanning directly!

---

## 🔒 Security & Privacy Checklist

- [x] **No Prescription Storage:** Ensure no disk volume is mounted for uploads. Photos must remain strictly in volatile memory.
- [x] **Client-Side Downscaling:** `camera.js` resizes all photos to max 1280px canvas JPEG before dispatch to reduce cellular data usage.
- [x] **Rate Limiting:** Protect `/api/extract-from-image` behind Nginx `limit_req_zone` (e.g., 10 requests/minute per IP) to prevent GPU resource exhaustion.
- [x] **CORS Restraints:** Set `ALLOWED_ORIGINS` in `.env` to your verified production domain.
- [x] **Offline Cache Header:** Service Worker (`sw.js`) serves cached JSON datasets (`Cache-First`), allowing full functionality even when the backend is unreachable.
