import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '@/services/api';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Button } from '@/components/ui/button';

interface ApiStatus {
  status: string;
  app_name: string;
  version: string;
  environment: string;
}

const Home: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<ApiStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [wsMessage, setWsMessage] = useState<string>('');

  const {
    connected: wsConnected,
    connecting: wsConnecting,
    connect: wsConnect,
    disconnect: wsDisconnect,
    send: wsSend,
  } = useWebSocket({
    url: '/ws/test',
    autoConnect: false,
    onMessage: (data) => {
      setWsMessage(JSON.stringify(data));
    },
    onError: () => {
      setWsMessage('WebSocket连接失败');
    },
  });

  useEffect(() => {
    const checkApi = async () => {
      try {
        const status = await api.healthCheck();
        setApiStatus(status);
        setError(null);
      } catch (err) {
        setError('API连接失败');
        console.error(err);
      }
    };

    checkApi();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-8">Steam主题设计器</h1>
      
      {/* API状态显示 */}
      <div className="mb-8 p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">API状态</h2>
        {error ? (
          <div className="text-red-500">{error}</div>
        ) : apiStatus ? (
          <div className="space-y-2">
            <p>状态: <span className="text-green-500">{apiStatus.status}</span></p>
            <p>应用: {apiStatus.app_name}</p>
            <p>版本: {apiStatus.version}</p>
            <p>环境: {apiStatus.environment}</p>
          </div>
        ) : (
          <div>正在检查API状态...</div>
        )}
      </div>

      {/* WebSocket测试 */}
      <div className="mb-8 p-4 bg-white dark:bg-gray-800 rounded-lg shadow-md">
        <h2 className="text-xl font-semibold mb-4">WebSocket测试</h2>
        <div className="space-y-4">
          <div className="flex items-center space-x-4">
            <Button
              variant={wsConnected ? 'outline' : 'primary'}
              onClick={wsConnected ? wsDisconnect : wsConnect}
              disabled={wsConnecting}
            >
              {wsConnecting ? '连接中...' : wsConnected ? '断开连接' : '连接WebSocket'}
            </Button>
            {wsConnected && (
              <Button
                variant="secondary"
                onClick={() => wsSend({ type: 'ping' })}
              >
                发送测试消息
              </Button>
            )}
          </div>
          {wsMessage && (
            <div className="mt-2">
              <p>最新消息:</p>
              <pre className="bg-gray-100 dark:bg-gray-700 p-2 rounded mt-1">
                {wsMessage}
              </pre>
            </div>
          )}
        </div>
      </div>

      {/* 功能卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
          <h2 className="text-2xl font-semibold mb-4">开始设计</h2>
          <p className="text-gray-600 dark:text-gray-300 mb-4">
            创建新的Steam主题或编辑现有主题
          </p>
          <Link
            to="/editor"
            className="inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
          >
            进入编辑器
          </Link>
        </div>
      </div>
    </div>
  );
};

export default Home; 