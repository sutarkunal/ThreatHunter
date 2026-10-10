/**
 * Alert API service
 */
import api from './api';

export const alertService = {
  /**
   * Get alerts with filters
   */
  listAlerts: async (params = {}) => {
    const response = await api.get('/alerts', { params });
    return response.data;
  },

  /**
   * Get alert by ID
   */
  getAlert: async (alertId) => {
    const response = await api.get(`/alerts/${alertId}`);
    return response.data;
  },

  /**
   * Update alert status
   */
  updateAlertStatus: async (alertId, status) => {
    const response = await api.patch(`/alerts/${alertId}`, { status });
    return response.data;
  },
};
