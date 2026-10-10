/**
 * Analytics Page - Detailed traffic analysis and visualizations
 */
import { useState, useEffect } from 'react';
import { BarChart3, PieChart, TrendingUp } from 'lucide-react';
import { PieChart as RechartsPie, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { LineChart, Line, XAxis, YAxis, CartesianGrid } from 'recharts';
import Card from '../components/common/Card';
import Loader from '../components/common/Loader';
import { sessionService } from '../services/sessionService';
import { analyticsService } from '../services/analyticsService';
import { formatNumber, formatBytes } from '../utils/formatters';

const COLORS = ['#0ea5e9', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

export default function Analytics() {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [protocolData, setProtocolData] = useState(null);
  const [trafficData, setTrafficData] = useState(null);
  const [loading, setLoading] = useState(true);

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
      const data = await sessionService.listSessions();
      const completedSessions = data.sessions.filter(s => s.status === 'completed');
      setSessions(completedSessions);

      if (completedSessions.length > 0) {
        setSelectedSession(completedSessions[0]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const loadAnalytics = async (sessionId) => {
    try {
      setLoading(true);

      const [protocols, traffic] = await Promise.all([
        analyticsService.getProtocolDistribution(sessionId),
        analyticsService.getTrafficOverTime(sessionId),
      ]);

      setProtocolData(protocols);
      setTrafficData(traffic);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !protocolData) {
    return <Loader text="Loading analytics..." />;
  }

  if (sessions.length === 0) {
    return (
      <div className="text-center py-12">
        <BarChart3 className="w-16 h-16 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">No completed sessions available for analysis</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Traffic Analytics</h1>
        <p className="text-gray-600 mt-1">Detailed network traffic analysis and visualizations</p>
      </div>

      {/* Session Selector */}
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
              {session.filename} - {formatNumber(session.packet_count)} packets
            </option>
          ))}
        </select>
      </Card>

      {/* Protocol Distribution */}
      {protocolData && (
        <Card title={
          <div className="flex items-center space-x-2">
            <PieChart className="w-5 h-5" />
            <span>Protocol Distribution</span>
          </div>
        }>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Pie Chart */}
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <RechartsPie>
                  <Pie
                    data={protocolData.protocols}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ protocol, percentage }) => `${protocol} (${percentage}%)`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="count"
                  >
                    {protocolData.protocols.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </RechartsPie>
              </ResponsiveContainer>
            </div>

            {/* Stats Table */}
            <div>
              <div className="space-y-3">
                {protocolData.protocols.map((proto, index) => (
                  <div
                    key={proto.protocol}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex items-center space-x-3">
                      <div
                        className="w-4 h-4 rounded"
                        style={{ backgroundColor: COLORS[index % COLORS.length] }}
                      />
                      <span className="font-medium text-gray-900">{proto.protocol}</span>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-gray-900">{formatNumber(proto.count)}</p>
                      <p className="text-sm text-gray-600">{proto.percentage}%</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </Card>
      )}

      {/* Traffic Over Time */}
      {trafficData && trafficData.timeseries.length > 0 && (
        <Card title={
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5" />
            <span>Traffic Over Time</span>
          </div>
        }>
          <div className="h-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={trafficData.timeseries}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="timestamp"
                  tickFormatter={(value) => new Date(value).toLocaleTimeString()}
                />
                <YAxis />
                <Tooltip
                  labelFormatter={(value) => new Date(value).toLocaleString()}
                  formatter={(value, name) => {
                    if (name === 'bytes') return [formatBytes(value), 'Bytes'];
                    return [formatNumber(value), 'Packets'];
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="packet_count"
                  stroke="#0ea5e9"
                  name="Packets"
                  strokeWidth={2}
                />
                <Line
                  type="monotone"
                  dataKey="bytes"
                  stroke="#22c55e"
                  name="Bytes"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>
      )}

      {/* Session Statistics */}
      {selectedSession && (
        <Card title="Session Statistics">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div>
              <p className="text-sm text-gray-600">Total Packets</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formatNumber(selectedSession.packet_count)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Unique Source IPs</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formatNumber(selectedSession.unique_src_ips)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Unique Dest IPs</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {formatNumber(selectedSession.unique_dst_ips)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Capture Duration</p>
              <p className="text-2xl font-bold text-gray-900 mt-1">
                {selectedSession.duration ? `${selectedSession.duration.toFixed(1)}s` : 'N/A'}
              </p>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
