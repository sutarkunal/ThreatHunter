/**
 * Utility constants
 */

export const SEVERITY_COLORS = {
  low: 'bg-gray-100 text-gray-800',
  medium: 'bg-warning-100 text-warning-800',
  high: 'bg-danger-100 text-danger-800',
  critical: 'bg-danger-600 text-white',
};

export const ALERT_TYPES = {
  port_scan: 'Port Scan',
  traffic_spike: 'Traffic Spike',
  suspicious_port: 'Suspicious Port',
  excessive_requests: 'Excessive Requests',
};

export const STATUS_COLORS = {
  processing: 'bg-blue-100 text-blue-800',
  completed: 'bg-success-100 text-success-800',
  failed: 'bg-danger-100 text-danger-800',
};
