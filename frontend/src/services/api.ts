interface HealthCheckResponse {
  status: string;
  app_name: string;
  version: string;
  environment: string;
}

interface PingResponse {
  ping: string;
}

export const api = {
  /**
   * 健康检查
   */
  async healthCheck(): Promise<HealthCheckResponse> {
    const response = await fetch('/api/health');
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  },

  /**
   * Ping测试
   */
  async ping(): Promise<PingResponse> {
    const response = await fetch('/api/health/ping');
    if (!response.ok) {
      throw new Error('Ping failed');
    }
    return response.json();
  },
}; 