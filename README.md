# ThreatHunter - Network Monitoring Dashboard

A comprehensive web-based Security Operations Center (SOC) tool for network traffic analysis, threat detection, and security monitoring.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)

## 🎯 Project Overview

ThreatHunter is a full-stack network security monitoring dashboard designed for cybersecurity students, analysts, and security professionals. It provides real-time visualization of network behavior, automated threat detection, and comprehensive alerting capabilities.

### Key Features

- 📦 **PCAP File Analysis** - Upload and analyze network capture files
- 🔍 **Packet Inspection** - Extract and query packet data with filtering
- ⚠️ **Automated Threat Detection**
  - Port scan detection
  - Traffic spike identification
  - Suspicious port monitoring
  - Excessive request detection
- 📊 **Interactive Analytics** - Protocol distribution, traffic timelines, top talkers
- 🎨 **Modern UI** - Responsive React dashboard with real-time updates
- 🗄️ **Scalable Database** - SQLite for development, PostgreSQL-ready for production

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│      React Frontend (Vite)          │
│   Tailwind CSS + Recharts           │
└─────────────────┬───────────────────┘
                  │ REST API
┌─────────────────▼───────────────────┐
│      FastAPI Backend                │
│   Python 3.11+ + PyShark            │
├─────────────────────────────────────┤
│  • Packet Processing Service        │
│  • Threat Detection Engine          │
│  • Alert Manager                    │
│  • Analytics Engine                 │
└─────────────────┬───────────────────┘
                  │
┌─────────────────▼───────────────────┐
│    SQLAlchemy ORM + SQLite          │
│  (PostgreSQL migration ready)       │
└─────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** with pip
- **Node.js 18+** with npm
- **Wireshark/tshark** (for PyShark)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/threathunter.git
cd threathunter
```

**2. Backend Setup**
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Initialize database
python -c "from app.database.session import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

**3. Frontend Setup**
```bash
cd ../frontend
npm install
```

**4. Install Wireshark/tshark**

**Windows:**
- Download from https://www.wireshark.org/download.html
- Check "Install TShark" during installation

**macOS:**
```bash
brew install wireshark
```

**Linux:**
```bash
sudo apt-get install tshark
```

### Running the Application

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```
Backend runs at: `http://localhost:8000`
API docs at: `http://localhost:8000/api/docs`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
Frontend runs at: `http://localhost:5173`

## 📚 Usage

### 1. Upload PCAP File
- Navigate to Upload page (`/upload`)
- Drag and drop or browse for `.pcap`, `.pcapng`, or `.cap` file
- Wait for processing (automatic threat detection runs)

### 2. View Dashboard
- Overview statistics
- Top source/destination IPs
- Protocol distribution
- Active threat count

### 3. Analyze Threats
- Visit Threat Center (`/threats`)
- Filter by severity, status, or alert type
- Update alert status (active → acknowledged → resolved)

### 4. Explore Analytics
- Protocol distribution pie chart
- Traffic over time visualization
- Session statistics

## 🔒 Threat Detection

### Port Scan Detection
**Algorithm:** Tracks unique destination ports per source IP within 60-second windows.

**Thresholds:**
- Medium: 20+ unique ports
- High: 50+ unique ports

### Traffic Spike Detection
**Algorithm:** Identifies minutes where packet count exceeds 3x baseline average.

**Severity:** Medium

### Suspicious Port Detection
**Monitored Ports:**
- Telnet (23) - High
- FTP (21) - Medium
- SMB (445) - High
- RDP (3389) - Medium
- SQL (1433, 3306) - Medium

### Excessive Requests
**Algorithm:** Counts packets per source IP within 60-second windows.

**Thresholds:**
- Medium: 100+ packets/min
- High: 500+ packets/min

## 📁 Project Structure

```
threathunter/
├── backend/
│   ├── app/
│   │   ├── api/v1/           # REST API endpoints
│   │   ├── models/           # Database ORM models
│   │   ├── schemas/          # Pydantic validation schemas
│   │   ├── services/         # Business logic
│   │   ├── detectors/        # Threat detection engines
│   │   ├── database/         # Database configuration
│   │   ├── utils/            # PCAP parser utilities
│   │   ├── config.py         # App configuration
│   │   └── main.py           # FastAPI application
│   ├── data/                 # SQLite DB, uploads, reports
│   ├── tests/                # Unit and integration tests
│   ├── requirements.txt
│   └── run.py
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/            # Route pages
│   │   ├── services/         # API integration
│   │   ├── utils/            # Utility functions
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

## 🔌 API Endpoints

### Sessions
- `POST /api/v1/sessions/upload` - Upload PCAP file
- `GET /api/v1/sessions` - List all sessions
- `GET /api/v1/sessions/{id}` - Get session details
- `DELETE /api/v1/sessions/{id}` - Delete session

### Packets
- `GET /api/v1/packets` - Query packets with filters

### Alerts
- `GET /api/v1/alerts` - List alerts
- `GET /api/v1/alerts/{id}` - Get alert details
- `PATCH /api/v1/alerts/{id}` - Update alert status

### Analytics
- `GET /api/v1/analytics/overview` - Dashboard overview
- `GET /api/v1/analytics/protocol-distribution` - Protocol stats
- `GET /api/v1/analytics/traffic-over-time` - Traffic timeline

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
pytest --cov=app tests/
```

### Frontend Tests
```bash
cd frontend
npm run lint
```

## 🛠️ Configuration

### Backend Configuration (`.env`)
```env
DATABASE_URL=sqlite:///./data/database/threathunter.db
MAX_UPLOAD_SIZE=104857600  # 100MB
PORT_SCAN_THRESHOLD_MEDIUM=20
PORT_SCAN_THRESHOLD_HIGH=50
EXCESSIVE_REQUESTS_MEDIUM=100
EXCESSIVE_REQUESTS_HIGH=500
```

### Frontend Configuration (`.env`)
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🚢 Deployment

### Docker (Coming Soon)
```bash
docker-compose up -d
```

### Manual Deployment

**Backend:**
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

**Frontend:**
```bash
npm run build
# Serve dist/ folder with Nginx or any static server
```

## 📈 Roadmap

### Phase 1: Foundation ✅
- [x] Project setup
- [x] PCAP upload and parsing
- [x] Database models
- [x] Basic API endpoints
- [x] Frontend skeleton

### Phase 2: Threat Detection ✅
- [x] Port scan detector
- [x] Traffic spike detector
- [x] Suspicious port detector
- [x] Excessive requests detector
- [x] Alert management

### Phase 3: Analytics & Visualization ✅
- [x] Dashboard with stats cards
- [x] Protocol distribution chart
- [x] Traffic over time chart
- [x] Threat center page

### Phase 4: Reporting (Coming Soon)
- [ ] Incident report generation
- [ ] PDF export
- [ ] JSON export
- [ ] Report templates

### Phase 5: Advanced Features (Future)
- [ ] Live packet capture (Scapy)
- [ ] User authentication
- [ ] WebSocket real-time updates
- [ ] Machine learning anomaly detection
- [ ] GeoIP location mapping
- [ ] Custom detection rules
- [ ] Email/Slack notifications
- [ ] Multi-session comparison

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Known Issues

- Large PCAP files (>100MB) may take time to process
- SQLite may have concurrency issues (use PostgreSQL for production)
- PyShark requires tshark to be in PATH

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Built for cybersecurity education and portfolio demonstration.

## 🙏 Acknowledgments

- **PyShark** - PCAP parsing
- **FastAPI** - Modern Python web framework
- **React** - UI framework
- **Recharts** - Data visualization
- **Tailwind CSS** - Styling framework

## 📞 Support

For issues, questions, or feature requests, please open a GitHub issue.

---

**⚠️ Disclaimer:** This tool is designed for educational purposes and authorized security testing only. Always obtain proper authorization before analyzing network traffic.
