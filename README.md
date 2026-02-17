# 🌦️ WeatherApp-OCI 

**Production Flask deployment on OCI Linux VM**

## 🖥️ Architecture

```
Browser → Load Balancer (80.225.200.198:80) → Linux VM (10.0.0.130:80) → Podman → Flask
                                                      ↓ CURRENT (Cost-Safe)
Browser → VM Public IP (80.225.224.206:80) → Podman Container → Flask ✓
                    ↓
VCN 10.0.0.0/16 + Security Lists (TCP/80) + firewalld
```

## ✅ PRODUCTION STATUS
| Access Method | URL | Status | Database |
|---------------|-----|--------|----------|
| **Load Balancer** | http://80.225.200.198 | ✅ Backend OK | **SQLite Active** |
| **Direct VM** | http://80.225.224.206 | ✅ Working | **Data Persisted** |
<img width="905" height="190" alt="{341EADB0-EA61-4E2E-9760-7C69152C9ADC}" src="https://github.com/user-attachments/assets/bcc3af66-98e8-4523-b33b-7687af972dd7" />


## 🛠️ Production Deployment (Copy-Paste)

```bash
# 1. Linux Server Setup
sudo yum install podman git -y

# 2. Clone & Deploy
git clone https://github.com/Parvezali4953/OCI-Deployment-Project.git
cd OCI-Deployment-Project/app
podman build -t weatherapp:prod .
podman run -d -p 80:80 --name weatherapp weatherapp:prod

# 3. Verify
curl localhost/health          # 200 {"status":"healthy"}
curl localhost/                # WeatherApp HTML ✓
```

## 🔧 PRODUCTION DEBUGGING 
```
❌ 502 Bad Gateway → ✅ 200 OK (Real Production Fix)
1. Flask port=80 (not 5000) ✓
2. Load Balancer Backend: Private IP 10.0.0.130:80 ✓
3. OCI Security Lists: TCP/80 ingress ✓
4. VM Firewall: sudo firewall-cmd --add-service=http ✓
5. Health Check: /health → 200 JSON ✓
```

## 📊 OCI INFRASTRUCTURE SPEC

| Component | Configuration | Status |
|-----------|---------------|--------|
| **Linux VM** | VM.Standard.E3.Flex (1 OCPU/16GB) | ✅ Running |
| **Networking** | VCN 10.0.0.0/16 + Public Subnet | ✅ Port 80 |
| **Container** | Podman weatherapp:prod | ✅ 0.0.0.0:80->80 |
| **Load Balancer** | Flexible Shape (10Mbps) | ✅ Demo Complete |
| **Storage** | 50GB Block Volume | Ready |

## 🗄️ CLOUD DATABASE

**✅ Production SQLite Database Implementation**

| Feature | Status | Rackspace Keyword |
|---------|--------|------------------|
| **SQLAlchemy ORM** | ✅ WeatherRecord model | SQL Fundamentals |
| **DDL Creation** | ✅ Auto table creation | Database Design |
| **DML Persistence** | ✅ Every query → INSERT | Data Manipulation |
| **Health Monitoring** | ✅ `{"db_connected":true}` | Performance Monitoring |
| **Production Ready** | ✅ Live DB writes | Backup/Recovery Ready |

**Live Database Demo:**

curl localhost/health

<img width="859" height="36" alt="{1A97E978-55DE-405C-922C-02BDB78DE5E5}" src="https://github.com/user-attachments/assets/dbb6fbaa-1083-4cdd-b974-a46da0d4adb7" />

curl -X POST http://localhost/weather -d "city=Mumbai"

<img width="926" height="209" alt="{8EF9778D-85F6-42D1-AFAE-56655588FA38}" src="https://github.com/user-attachments/assets/6d7e2fcb-464f-4290-a1f1-1d9736d61b5c" />

Database Schema:
```bash
CREATE TABLE weather_record (
    id INTEGER PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    temperature FLOAT NOT NULL,
    description VARCHAR(100),
    humidity INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

Production Stack: OCI Console → VCN → Load Balancer → Linux VM → Podman → SQLite DB

## 🚀 Quick Start (Anyone Can Deploy)

```bash
git clone https://github.com/Parvezali4953/OCI-Deployment-Project.git
cd OCI-Deployment-Project/app
podman build -t weatherapp .
podman run -d -p 80:80 weatherapp
curl localhost/  # LIVE WeatherApp! 🌦️
```
## 📸 PRODUCTION SCREENSHOTS

1. Load Balancer Backend Set: Status OK (GREEN)
<img width="1250" height="98" alt="{83FD4BBA-AFD7-425C-B18F-8B47A58FF57C}" src="https://github.com/user-attachments/assets/8094044d-4d3a-4ba1-8c89-d97a0e08730d" />

2. curl 80.225.200.198 → WeatherApp via LB
<img width="883" height="142" alt="{81A66898-AF36-4EF8-A9C1-B5F6B0F8E95E}" src="https://github.com/user-attachments/assets/3f3ef98d-ef03-4933-bd7c-5d148d8604ad" />

3. OCI Console → VM Details + VCN
<img width="1170" height="77" alt="{33C148C2-F1FC-41BE-848A-57FE979452B6}" src="https://github.com/user-attachments/assets/b5698716-bdce-49d9-bb81-88a3536c3400" />
<img width="1191" height="371" alt="{87635668-42A9-4C65-B238-762C841D8309}" src="https://github.com/user-attachments/assets/cd390234-5e4e-49c2-b35b-efa4c4d5fd18" />

4. podman ps → Container healthy
<img width="930" height="38" alt="{4C9A95D2-F3C7-4B27-A753-1335F9489102}" src="https://github.com/user-attachments/assets/87405f78-26b3-4ff9-8908-8b1884b02626" />

