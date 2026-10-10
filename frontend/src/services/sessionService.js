/**
 * Session API service
 */
import api from './api';

export const sessionService = {
  /**
   * Upload a PCAP file
   */
  uploadPCAP: async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/sessions/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  /**
   * Get all sessions
   */
  listSessions: async () => {
    const response = await api.get('/sessions');
    return response.data;
  },

  /**
   * Get session by ID
   */
  getSession: async (sessionId) => {
    const response = await api.get(`/sessions/${sessionId}`);
    return response.data;
  },

  /**
   * Delete session
   */
  deleteSession: async (sessionId) => {
    await api.delete(`/sessions/${sessionId}`);
  },
};
