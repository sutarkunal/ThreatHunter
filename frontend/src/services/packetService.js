/**
 * Packet API service
 */
import api from './api';

export const packetService = {
  /**
   * Get packets with filters
   */
  listPackets: async (sessionId, params = {}) => {
    const response = await api.get('/packets', {
      params: { session_id: sessionId, ...params },
    });
    return response.data;
  },
};
