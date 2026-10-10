/**
 * Analytics API service
 */
import api from './api';

export const analyticsService = {
  /**
   * Get overview analytics
   */
  getOverview: async (sessionId) => {
    const response = await api.get('/analytics/overview', {
      params: { session_id: sessionId },
    });
    return response.data;
  },

  /**
   * Get protocol distribution
   */
  getProtocolDistribution: async (sessionId) => {
    const response = await api.get('/analytics/protocol-distribution', {
      params: { session_id: sessionId },
    });
    return response.data;
  },

  /**
   * Get traffic over time
   */
  getTrafficOverTime: async (sessionId, intervalSeconds = 60) => {
    const response = await api.get('/analytics/traffic-over-time', {
      params: { session_id: sessionId, interval_seconds: intervalSeconds },
    });
    return response.data;
  },
};
