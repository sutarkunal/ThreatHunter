# ThreatHunter - Quick Start Guide

**Last Updated:** September 24, 2026

---

## ⚡ Quick Installation (5 Minutes)

### Step 1: Install Prerequisites

**Windows:**
```powershell
# Install Python 3.11+ from python.org
# Install Node.js 18+ from nodejs.org
# Install Wireshark from wireshark.org (check "Install TShark")
```

**macOS:**
```bash
brew install python node wireshark
```

**Linux:**
```bash
sudo apt-get install python3.11 python3-pip nodejs npm tshark
```

---

### Step 2: Setup Backend (2 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies (this takes ~1-2 minutes)
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
python -c "from app.database.session import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

---

### Step 3: Setup Frontend (2 minutes)

```bash
cd ../frontend

# Install dependencies (this takes ~1-2 minutes)
npm install
```

---

### Step 4: Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```
✅ Backend running at: **http://localhost:8000**  
✅ API docs at: **http://localhost:8000/api/docs**

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
✅ Frontend running at: **http://localhost:5173**

---

## 🎯 First Test (2 Minutes)

### Option A: Generate Test PCAP Files

```bash
# In project root
pip install scapy
python generate_test_pcap.py
```

This creates 5 test PCAP files you can upload.

### Option B: Use Your Own PCAP

If you have Wireshark, capture some traffic:
1. Open Wireshark
2. Start capture on your network interface
3. Browse the web for 30 seconds
4. Stop capture
5. Save as `.pcap` file

---

## 🚀 Using ThreatHunter

### 1. Upload PCAP File
1. Open **http://localhost:5173/upload**
2. Drag & drop a PCAP file (or click Browse)
3. Click "Upload File"
4. Wait 10-30 seconds for processing

### 2. View Dashboard
1. Go to **http://localhost:5173/**
2. Select your session
3. View statistics:
   - Total packets
   - Alerts generated
   - Active threats
   - Protocol distribution
   - Top IPs

### 3. Check Threats
1. Go to **http://localhost:5173/threats**
2. Filter alerts by severity/status
3. Update alert status (active → acknowledged → resolved)

### 4. Explore Analytics
1. Go to **http://localhost:5173/analytics**
2. View charts:
   - Protocol distribution (pie chart)
   - Traffic over time (line chart)
   - Session statistics

---

## 🐛 Troubleshooting

### Backend won't start

**Error: "ModuleNotFoundError: No module named 'fastapi'"**
```bash
# Make sure virtual environment is activated
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

**Error: "tshark not found"**
```bash
# Windows: Add Wireshark to PATH or reinstall with tshark option
# macOS: brew install wireshark
# Linux: sudo apt-get install tshark
```

### Frontend won't start

**Error: "Cannot find module"**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 5173 already in use"**
```bash
# Change port in vite.config.js or kill process using port
# Windows: netstat -ano | findstr :5173
# macOS/Linux: lsof -ti:5173 | xargs kill
```

### Upload fails

**Error: "Invalid file type"**
- Only `.pcap`, `.pcapng`, and `.cap` files are supported

**Error: "File too large"**
- Maximum file size is 100MB
- Use Wireshark to filter and save smaller captures

### No alerts generated

- This is normal for regular traffic
- Use test PCAP files from `generate_test_pcap.py`
- Or capture traffic while doing a port scan: `nmap localhost`

---

## 📚 API Testing

### Using Swagger UI
1. Open **http://localhost:8000/api/docs**
2. Try endpoints directly in browser
3. View request/response schemas

### Using curl

**Upload PCAP:**
```bash
curl -X POST "http://localhost:8000/api/v1/sessions/upload" \
  -F "file=@your_capture.pcap"
```

**List sessions:**
```bash
curl "http://localhost:8000/api/v1/sessions"
```

**Get analytics:**
```bash
curl "http://localhost:8000/api/v1/analytics/overview?session_id=1"
```

---

## 🎓 What to Try

### Test Port Scan Detection
```bash
# Generate port scan PCAP
python generate_test_pcap.py

# Upload port_scan_attack.pcap
# Expected: HIGH severity alert for port scanning
```

### Test Suspicious Port Detection
```bash
# Upload suspicious_ports.pcap
# Expected: MEDIUM/HIGH alerts for Telnet, SMB, RDP connections
```

### Test Excessive Requests
```bash
# Upload excessive_requests.pcap
# Expected: MEDIUM alert for single IP generating 200+ packets
```

### Test Multiple Threats
```bash
# Upload multiple_threats.pcap
# Expected: Multiple alerts of different types
```

---

## 📊 Expected Results

### Normal Traffic (normal_traffic.pcap)
- ✅ 120 packets processed
- ✅ 0-1 alerts (or none)
- ✅ Protocols: TCP, UDP, ICMP
- ✅ Processing time: ~5-10 seconds

### Port Scan Attack (port_scan_attack.pcap)
- ✅ 160+ packets processed
- ⚠️ **1 HIGH severity alert** (Port Scan)
- ✅ Alert shows 60+ unique ports scanned
- ✅ Processing time: ~10-15 seconds

### Suspicious Ports (suspicious_ports.pcap)
- ✅ 90+ packets processed
- ⚠️ **1-2 MEDIUM/HIGH alerts** (Suspicious Port)
- ✅ Alerts for Telnet, SMB, RDP, etc.
- ✅ Processing time: ~5-10 seconds

### Multiple Threats (multiple_threats.pcap)
- ✅ 400+ packets processed
- ⚠️ **3-4 alerts** (Port Scan, Suspicious Port, Excessive Requests)
- ✅ Multiple severity levels
- ✅ Processing time: ~15-30 seconds

---

## 🎯 Next Steps

### Explore the Code
```bash
# Backend structure
cd backend/app
ls -la api/v1/        # API endpoints
ls -la detectors/     # Threat detection algorithms
ls -la models/        # Database models

# Frontend structure
cd frontend/src
ls -la pages/         # React pages
ls -la components/    # React components
ls -la services/      # API integration
```

### Modify Detection Thresholds
```bash
# Edit backend/.env
PORT_SCAN_THRESHOLD_MEDIUM=20  # Change to 10 for more alerts
PORT_SCAN_THRESHOLD_HIGH=50    # Change to 30 for more alerts
EXCESSIVE_REQUESTS_MEDIUM=100  # Change to 50 for more alerts
```

### Add Your Own Detector
1. Create `backend/app/detectors/my_detector.py`
2. Extend `BaseDetector` class
3. Implement `detect()` method
4. Register in `alert_manager.py`

---

## 💡 Tips

### Performance
- First PCAP upload takes longer (database initialization)
- Subsequent uploads are faster
- Large files (>50MB) may take 1-2 minutes

### Development
- Backend auto-reloads on code changes (DEBUG=True)
- Frontend has hot module replacement (instant updates)
- Check browser console for frontend errors
- Check terminal for backend errors

### Best Practices
- Start with small PCAP files (<10MB, <10k packets)
- Test one threat type at a time
- Use the test PCAP generator for consistent results
- Check API docs for endpoint details

---

## 📞 Need Help?

### Check Logs
**Backend:**
```bash
# Terminal running python run.py shows all logs
# Look for ERROR or WARNING messages
```

**Frontend:**
```bash
# Browser DevTools → Console tab
# Browser DevTools → Network tab (for API calls)
```

### Verify Services
```bash
# Test backend
curl http://localhost:8000/health

# Should return: {"status": "healthy"}
```

### Common Issues
1. **No database file** → Run database initialization command
2. **Import errors** → Activate virtual environment
3. **Port conflicts** → Change ports or kill processes
4. **CORS errors** → Check backend CORS settings in .env

---

## ✅ Success Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Wireshark/tshark installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Database initialized
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] API docs accessible
- [ ] Test PCAP files generated
- [ ] Successfully uploaded a PCAP
- [ ] Viewed dashboard statistics
- [ ] Saw threat alerts
- [ ] Explored analytics charts

---

**🎉 Congratulations! ThreatHunter is running!**

For detailed documentation, see:
- `README.md` - Full documentation
- `PROJECT_SUMMARY.md` - Project overview
- `THREATHUNTER_ARCHITECTURE.md` - Architecture details
- `TODO.md` - Development roadmap
