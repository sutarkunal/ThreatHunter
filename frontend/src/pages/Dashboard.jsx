/**
 * Dashboard Page - Overview of network monitoring
 */
import { useState, useEffect } from 'react';
import { Activity, AlertTriangle, Shield, TrendingUp } from 'lucide-react';
import Card from '../components/common/Card';
import Loader from '../components/common/Loader';
import Badge from '../components/common/Badge';
import { sessionService } from '../services/sessionService';
import { analyticsService } from '../services/analyticsService';
import { formatNumber, formatRelativeTime } from '../utils/formatters';
import { STATUS_COLORS } from '../utils/constants';

export default function Dashboard() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (selectedSession) {
      loadAnalytics(selectedSession.id);
    }
  }, [selectedSession]);

  const loadSessions = async () => {
    try {
      setLoading(true);
      const data = await sessionService.listSessions();
      setSessions(data.sessions);

      // Auto-select first completed session
      const completedSession = data.sessions.find(s => s.status === 'completed');
      if (completedSession) {
        setSelectedSession(completedSession);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const loadAnalytics = async (sessionId) => {
    try {
      const data = await analyticsService.getOverview(sessionId);
      setAnalytics(data);
    } catch (err) {
      setError(err.message);
    }
  };

  if (loading) {
    return <Loader text="Loading dashboard..." />;
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <AlertTriangle className="w-12 h-12 text-danger-500 mx-auto mb-4" />
        <p className="text-danger-600">Error: {error}</p>
      </div>
    );
  }

  if (sessions.length === 0) {
    return (
      <div className="text-center py-12">
        <Shield className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-gray-700 mb-2">No PCAP Sessions</h2>
        <p className="text-gray-600 mb-4">Upload a PCAP file to start analyzing network traffic</p>
        <a href="/upload" className="btn btn-primary">
          Upload PCAP File
        </a>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Network Monitoring Dashboard</h1>
          <p className="text-gray-600 mt-1">Real-time threat detection and analysis</p>
        </div>
      </div>

      {/* Session Selector */}
      <Card title="Select Session">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sessions.map((session) => (
            <button
              key={session.id}
              onClick={() => setSelectedSession(session)}
              className={`text-left p-4 border-2 rounded-lg transition-colors ${
                selectedSession?.id === session.id
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-gray-900 truncate">{session.filename}</h3>
                <span className={`badge ${STATUS_COLORS[session.status]}`}>
                  {session.status}
                </span>
              </div>
              <p className="text-sm text-gray-600">{formatNumber(session.packet_count)} packets</p>
              <p className="text-xs text-gray-500 mt-1">{formatRelativeTime(session.upload_timestamp)}</p>
            </button>
          ))}
        </div>
      </Card>

      {/* Stats Cards */}
      {analytics && (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {/* Total Packets */}
            <Card>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Packets</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">
                    {formatNumber(analytics.total_packets)}
                  </p>
                </div>
                <Activity className="w-12 h-12 text-primary-500" />
              </div>
            </Card>

            {/* Total Alerts */}
            <Card>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Total Alerts</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">
                    {formatNumber(analytics.total_alerts)}
                  </p>
                </div>
                <AlertTriangle className="w-12 h-12 text-warning-500" />
              </div>
            </Card>

            {/* Active Threats */}
            <Card>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Active Threats</p>
                  <p className="text-3xl font-bold text-danger-600 mt-1">
                    {formatNumber(analytics.active_threats)}
                  </p>
                </div>
                <Shield className="w-12 h-12 text-danger-500" />
              </div>
            </Card>

            {/* Protocols */}
            <Card>
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600">Protocols Detected</p>
                  <p className="text-3xl font-bold text-gray-900 mt-1">
                    {Object.keys(analytics.protocols).length}
                  </p>
                </div>
                <TrendingUp className="w-12 h-12 text-success-500" />
              </div>
            </Card>
          </div>

          {/* Top IPs */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top Source IPs */}
            <Card title="Top Source IPs">
              <div className="space-y-2">
                {analytics.top_src_ips.slice(0, 5).map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-mono text-sm">{item.ip}</span>
                    <Badge severity="low">{formatNumber(item.count)} packets</Badge>
                  </div>
                ))}
              </div>
            </Card>

            {/* Top Destination IPs */}
            <Card title="Top Destination IPs">
              <div className="space-y-2">
                {analytics.top_dst_ips.slice(0, 5).map((item, index) => (
                  <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <span className="font-mono text-sm">{item.ip}</span>
                    <Badge severity="low">{formatNumber(item.count)} packets</Badge>
                  </div>
                ))}
              </div>
            </Card>
          </div>

          {/* Protocol Distribution */}
          <Card title="Protocol Distribution">
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {Object.entries(analytics.protocols).map(([protocol, count]) => (
                <div key={protocol} className="text-center p-4 bg-gray-50 rounded-lg">
                  <p className="text-2xl font-bold text-primary-600">{formatNumber(count)}</p>
                  <p className="text-sm text-gray-600 mt-1">{protocol}</p>
                </div>
              ))}
            </div>
          </Card>
        </>
      )}
    </div>
  );
}
