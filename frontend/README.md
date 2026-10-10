# ThreatHunter Frontend

Modern React-based dashboard for network monitoring and threat detection.

## Features

- 📊 **Interactive Dashboard** - Real-time overview of network activity
- 📈 **Analytics Visualizations** - Protocol distribution, traffic timelines with Recharts
- ⚠️ **Threat Center** - Alert management with filtering and status updates
- 📤 **PCAP Upload** - Drag-and-drop file upload with validation
- 🎨 **Modern UI** - Built with Tailwind CSS and Lucide icons
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **React Router** - Client-side routing
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Axios** - HTTP client
- **Lucide React** - Icon library

## Installation

### Prerequisites

- Node.js 18+ and npm

### Setup

```bash
cd frontend
npm install
```

### Configuration

Create `.env` file:

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## Development

### Start Dev Server

```bash
npm run dev
```

Server runs at: `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Output in `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
src/
├── components/
│   ├── common/         # Reusable components (Card, Badge, Navbar, etc.)
│   ├── dashboard/      # Dashboard-specific components
│   ├── analytics/      # Analytics components
│   └── alerts/         # Alert components
├── pages/              # Route pages
│   ├── Dashboard.jsx
│   ├── Analytics.jsx
│   ├── ThreatCenter.jsx
│   ├── Reports.jsx
│   └── Upload.jsx
├── services/           # API service layer
├── utils/              # Utility functions
├── styles/             # Global styles
├── App.jsx             # Main app component
└── main.jsx            # Entry point
```

## Pages

### Dashboard (`/`)
- Overview statistics
- Session selector
- Top source/destination IPs
- Protocol distribution
- Quick stats cards

### Analytics (`/analytics`)
- Protocol distribution pie chart
- Traffic over time line chart
- Session statistics
- Detailed metrics

### Threat Center (`/threats`)
- Alert listing with filters
- Severity-based filtering
- Alert status management
- Alert details

### Upload (`/upload`)
- Drag-and-drop file upload
- File validation
- Upload progress
- Success feedback

### Reports (`/reports`)
- Coming in Phase 4
- Report generation placeholder

## API Integration

All API calls go through service layer:

```javascript
// Example: Upload PCAP
import { sessionService } from './services/sessionService';

const file = // ... get file
await sessionService.uploadPCAP(file);
```

Services available:
- `sessionService` - Session management
- `alertService` - Alert operations
- `analyticsService` - Analytics data
- `packetService` - Packet queries

## Styling

### Tailwind Classes

Custom classes defined in `src/styles/index.css`:

```css
.card         /* White card with shadow */
.btn          /* Base button */
.btn-primary  /* Primary button (blue) */
.btn-secondary /* Secondary button (gray) */
.btn-danger   /* Danger button (red) */
.badge        /* Status badge */
.input        /* Form input */
```

### Color Palette

- **Primary**: Blue (`primary-*`)
- **Danger**: Red (`danger-*`)
- **Warning**: Yellow (`warning-*`)
- **Success**: Green (`success-*`)

## Components

### Common Components

**Card**
```jsx
<Card title="Title" action={<button>Action</button>}>
  Content
</Card>
```

**Badge**
```jsx
<Badge severity="high">High</Badge>
```

**Loader**
```jsx
<Loader size="md" text="Loading..." />
```

## Development Tips

### Hot Module Replacement

Vite provides instant HMR. Changes appear immediately without full reload.

### Proxy Configuration

Vite proxies `/api` requests to backend:

```javascript
// vite.config.js
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  }
}
```

### ESLint

```bash
npm run lint
```

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Troubleshooting

### Port Already in Use

Change port in `vite.config.js`:

```javascript
server: {
  port: 3000,  // Change from 5173
}
```

### CORS Issues

Ensure backend allows frontend origin in CORS settings.

### API Connection Failed

Check:
1. Backend is running on `http://localhost:8000`
2. `.env` has correct `VITE_API_BASE_URL`
3. Network tab in browser DevTools for errors

## Roadmap

- [ ] Real-time updates with WebSockets
- [ ] Dark mode toggle
- [ ] Advanced filtering
- [ ] Chart export
- [ ] User authentication
- [ ] Custom dashboards
- [ ] Alert notifications

## License

MIT

## Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request
