/**
 * Threat Center Page - View and manage security alerts
 */
import { useState, useEffect } from 'react';
import { AlertTriangle, Filter, ShieldAlert } from 'lucide-react';
import Card from '../components/common/Card';
import Badge from '../components/common/Badge';
import Loader from '../components/common/Loader';
import { alertService } from '../services/alertService';
import { sessionService } from '../services/sessionService';
import { formatDate } from '../utils/formatters';
import { ALERT_TYPES } from '../utils/constants';

export default function ThreatCenter() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [filteredAlerts, setFilteredAlerts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    severity: 'all',
    status: 'all',
    alertType: 'all',
  });

  useEffect(() => {
    loadSessions();
  }, []);

  useEffect(() => {
    if (selectedSession) {
      loadAlerts(selectedSession.id);
    }
  }, [selectedSession]);

  useEffect(() => {
    applyFilters();
  }, [alerts, filters]);

  const loadSessions = async () => {
    try {
      const data = await sessionService.listSessions();
      setSessions(data.sessions.filter(s => s.status === 'completed'));

      if (data.sessions.length > 0) {
        setSelectedSession(data.sessions[0]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadAlerts = async (sessionId) => {
    try {
      setLoading(true);
      const data = await alertService.listAlerts({ session_id: sessionId });
      setAlerts(data.alerts);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...alerts];

    if (filters.severity !== 'all') {
      filtered = filtered.filter(a => a.severity === filters.severity);
    }

    if (filters.status !== 'all') {
      filtered = filtered.filter(a => a.status === filters.status);
    }

    if (filters.alertType !== 'all') {
      filtered = filtered.filter(a => a.alert_type === filters.alertType);
    }

    setFilteredAlerts(filtered);
  };

  const handleStatusChange = async (alertId, newStatus) => {
    try {
      await alertService.updateAlertStatus(alertId, newStatus);

      // Refresh alerts
      if (selectedSession) {
        loadAlerts(selectedSession.id);
      }
    } catch (err) {
      console.error(err);
    }
  };

  if (loading && alerts.length === 0) {
    return <Loader text="Loading alerts..." />;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Threat Center</h1>
        <p className="text-gray-600 mt-1">Monitor and manage security alerts</p>
      </div>

      {/* Session Selector */}
      {sessions.length > 0 && (
        <Card>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select Session
          </label>
          <select
            value={selectedSession?.id || ''}
            onChange={(e) => {
              const session = sessions.find(s => s.id === parseInt(e.target.value));
              setSelectedSession(session);
            }}
            className="input"
          >
            {sessions.map((session) => (
              <option key={session.id} value={session.id}>
                {session.filename} - {session.packet_count} packets
              </option>
            ))}
          </select>
        </Card>
      )}

      {/* Filters */}
      <Card title={
        <div className="flex items-center space-x-2">
          <Filter className="w-5 h-5" />
          <span>Filters</span>
        </div>
      }>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Severity Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Severity
            </label>
            <select
              value={filters.severity}
              onChange={(e) => setFilters({ ...filters, severity: e.target.value })}
              className="input"
            >
              <option value="all">All</option>
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>

          {/* Status Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              value={filters.status}
              onChange={(e) => setFilters({ ...filters, status: e.target.value })}
              className="input"
            >
              <option value="all">All</option>
              <option value="active">Active</option>
              <option value="acknowledged">Acknowledged</option>
              <option value="resolved">Resolved</option>
            </select>
          </div>

          {/* Alert Type Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Alert Type
            </label>
            <select
              value={filters.alertType}
              onChange={(e) => setFilters({ ...filters, alertType: e.target.value })}
              className="input"
            >
              <option value="all">All</option>
              {Object.keys(ALERT_TYPES).map((type) => (
                <option key={type} value={type}>
                  {ALERT_TYPES[type]}
                </option>
              ))}
            </select>
          </div>
        </div>
      </Card>

      {/* Alerts List */}
      <Card title={`Alerts (${filteredAlerts.length})`}>
        {filteredAlerts.length === 0 ? (
          <div className="text-center py-12">
            <ShieldAlert className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <p className="text-gray-600">No alerts found</p>
          </div>
        ) : (
          <div className="space-y-4">
            {filteredAlerts.map((alert) => (
              <div
                key={alert.id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <AlertTriangle className={`w-5 h-5 ${
                        alert.severity === 'high' || alert.severity === 'critical'
                          ? 'text-danger-500'
                          : 'text-warning-500'
                      }`} />
                      <h3 className="font-semibold text-gray-900">{alert.title}</h3>
                      <Badge severity={alert.severity}>{alert.severity}</Badge>
                      <span className="text-xs text-gray-500">
                        {ALERT_TYPES[alert.alert_type] || alert.alert_type}
                      </span>
                    </div>

                    <p className="text-sm text-gray-700 mb-3">{alert.description}</p>

                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      {alert.src_ip && (
                        <span className="font-mono">Source: {alert.src_ip}</span>
                      )}
                      {alert.dst_ip && (
                        <span className="font-mono">Dest: {alert.dst_ip}</span>
                      )}
                      <span>{formatDate(alert.timestamp)}</span>
                    </div>
                  </div>

                  <div className="ml-4">
                    <select
                      value={alert.status}
                      onChange={(e) => handleStatusChange(alert.id, e.target.value)}
                      className="input text-sm"
                    >
                      <option value="active">Active</option>
                      <option value="acknowledged">Acknowledged</option>
                      <option value="resolved">Resolved</option>
                    </select>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </Card>
    </div>
  );
}
