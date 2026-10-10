# ThreatHunter Backend

Network Monitoring and Threat Detection API built with FastAPI and Python.

## Features

- 📦 **PCAP File Upload** - Support for .pcap, .pcapng, and .cap files
- 🔍 **Packet Analysis** - Parse and extract network packet data using PyShark
- ⚠️ **Threat Detection** - Automated detection of:
  - Port scanning attempts
  - Traffic spikes and anomalies
  - Suspicious port usage
  - Excessive requests (potential DDoS)
- 📊 **Analytics** - Protocol distribution, top talkers, traffic over time
- 🗄️ **Database** - SQLite (development) with PostgreSQL migration path
- 📝 **API Documentation** - Auto-generated OpenAPI/Swagger docs

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── models/          # Database models
│   ├── schemas/         # Pydantic validation schemas
│   ├── services/        # Business logic
│   ├── detectors/       # Threat detection engines
│   ├── database/        # Database configuration
│   ├── utils/           # Utilities (PCAP parser)
│   ├── config.py        # Configuration
│   └── main.py          # FastAPI app
├── data/
│   ├── uploads/         # Uploaded PCAP files
│   ├── database/        # SQLite database
│   └── reports/         # Generated reports
├── tests/               # Unit and integration tests
├── requirements.txt     # Python dependencies
└── run.py              # Development server
```

## Installation

### Prerequisites

- Python 3.11 or higher
- pip
- Wireshark/tshark (for PyShark)

### Install Wireshark/tshark

**Windows:**
```bash
# Download and install Wireshark from https://www.wireshark.org/download.html
# Make sure to check "Install TShark" during installation
```

**macOS:**
```bash
brew install wireshark
```

**Linux:**
```bash
sudo apt-get install tshark
```

### Setup

1. **Create virtual environment:**
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment:**
```bash
cp .env.example .env
# Edit .env if needed
```

4. **Initialize database:**
```bash
python -c "from app.database.session import engine, Base; from app.models import *; Base.metadata.create_all(bind=engine)"
```

## Usage

### Start Development Server

```bash
python run.py
```

Server will start at: `http://localhost:8000`

### API Documentation

- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

### API Endpoints

#### Sessions
- `POST /api/v1/sessions/upload` - Upload PCAP file
- `GET /api/v1/sessions` - List all sessions
- `GET /api/v1/sessions/{id}` - Get session details
- `DELETE /api/v1/sessions/{id}` - Delete session

#### Packets
- `GET /api/v1/packets` - Query packets with filters

#### Alerts
- `GET /api/v1/alerts` - List alerts with filters
- `GET /api/v1/alerts/{id}` - Get alert details
- `PATCH /api/v1/alerts/{id}` - Update alert status

#### Analytics
- `GET /api/v1/analytics/overview` - Dashboard overview
- `GET /api/v1/analytics/protocol-distribution` - Protocol stats
- `GET /api/v1/analytics/traffic-over-time` - Traffic timeline

## Threat Detection

### Port Scan Detection
Detects when a source IP attempts connections to many ports within 60 seconds.
- **Thresholds:** 20+ ports (medium), 50+ ports (high)

### Traffic Spike Detection
Identifies unusual increases in packet volume.
- **Algorithm:** Traffic > 3x baseline average

### Suspicious Port Detection
Monitors connections to commonly abused ports:
- Telnet (23), FTP (21), SMB (445), RDP (3389), etc.

### Excessive Requests
Detects IPs generating high packet volumes.
- **Thresholds:** 100+ packets/min (medium), 500+ packets/min (high)

## Configuration

Edit `.env` to customize:

```env
# Database
DATABASE_URL=sqlite:///./data/database/threathunter.db

# Upload limits
MAX_UPLOAD_SIZE=104857600  # 100MB

# Detection thresholds
PORT_SCAN_THRESHOLD_MEDIUM=20
PORT_SCAN_THRESHOLD_HIGH=50
EXCESSIVE_REQUESTS_MEDIUM=100
```

## Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# With coverage
pytest --cov=app tests/
```

## Example Usage

### Upload PCAP File

```bash
curl -X POST "http://localhost:8000/api/v1/sessions/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@capture.pcap"
```

### Get Analytics

```bash
curl "http://localhost:8000/api/v1/analytics/overview?session_id=1"
```

### List Alerts

```bash
curl "http://localhost:8000/api/v1/alerts?session_id=1&severity=high"
```

## Development

### Code Style

```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

### Database Migrations

Using Alembic (future enhancement):
```bash
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Troubleshooting

### PyShark Issues

If PyShark can't find tshark:
```python
# Add to your code or environment
import os
os.environ['TSHARK_PATH'] = '/path/to/tshark'
```

### Database Locked

SQLite may lock with concurrent access. Use PostgreSQL for production:
```env
DATABASE_URL=postgresql://user:password@localhost/threathunter
```

## Performance Tips

1. **Large PCAP files:** Adjust `MAX_PACKETS_PER_SESSION` in config
2. **Processing speed:** Increase `PACKET_PROCESSING_BATCH_SIZE`
3. **Memory:** Set `keep_packets=False` in PyShark (already configured)

## Security Considerations

- File upload size limits enforced
- File type validation (.pcap only)
- SQL injection prevented (SQLAlchemy ORM)
- CORS configured for frontend origins

## License

MIT

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Submit pull request

## Roadmap

- [ ] User authentication
- [ ] Real-time packet capture with Scapy
- [ ] WebSocket support for live updates
- [ ] Machine learning anomaly detection
- [ ] GeoIP location mapping
- [ ] Custom detection rules
- [ ] Email/Slack notifications

## Support

For issues and questions, please open a GitHub issue.
