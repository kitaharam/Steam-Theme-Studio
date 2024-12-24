import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import CSSEditor from '@/components/Editor/CSSEditor';
import PreviewControl from '@/components/Editor/PreviewControl';
import useWebSocket from '@/hooks/useWebSocket';
import { API_BASE_URL } from '@/config';

interface Theme {
  name: string;
  config: {
    name: string;
    author: string;
    version: string;
    description: string;
  };
  path: string;
}

const Editor: React.FC = () => {
  const { themeName } = useParams<{ themeName: string }>();
  const navigate = useNavigate();
  const [theme, setTheme] = useState<Theme | null>(null);
  const [cssContent, setCssContent] = useState('');
  const [isPreviewActive, setIsPreviewActive] = useState(false);
  const [isSaving, setIsSaving] = useState(false);

  const {
    sendMessage,
    connected,
    connecting,
    connect,
    disconnect,
  } = useWebSocket({
    url: `ws://${API_BASE_URL}/api/millennium/themes/${themeName}/preview/ws`,
    autoConnect: false,
    onMessage: (data) => {
      if (data.status === 'error') {
        toast.error(data.message);
      }
    },
    onClose: () => {
      setIsPreviewActive(false);
    },
    onError: () => {
      toast.error('预览连接失败');
      setIsPreviewActive(false);
    },
  });

  useEffect(() => {
    const fetchTheme = async () => {
      try {
        const response = await fetch(`http://${API_BASE_URL}/api/millennium/themes/${themeName}`);
        if (!response.ok) {
          throw new Error('主题不存在');
        }
        const data = await response.json();
        setTheme(data);

        // 读取CSS文件内容
        const cssResponse = await fetch(`http://${API_BASE_URL}/api/millennium/themes/${themeName}/css`);
        if (cssResponse.ok) {
          const css = await cssResponse.text();
          setCssContent(css);
        }
      } catch (error) {
        toast.error('加载主题失败');
        navigate('/');
      }
    };

    if (themeName) {
      fetchTheme();
    }
  }, [themeName, navigate]);

  const handleStartPreview = async () => {
    try {
      const response = await fetch(
        `http://${API_BASE_URL}/api/millennium/themes/${themeName}/preview`,
        { method: 'POST' }
      );
      
      if (!response.ok) {
        throw new Error('启动预览失败');
      }

      setIsPreviewActive(true);
      connect();
      toast.success('预览已启动');
    } catch (error) {
      toast.error('启动预览失败');
    }
  };

  const handleStopPreview = async () => {
    try {
      await fetch(
        `http://${API_BASE_URL}/api/millennium/themes/${themeName}/preview`,
        { method: 'DELETE' }
      );
      disconnect();
      setIsPreviewActive(false);
      toast.success('预览已停止');
    } catch (error) {
      toast.error('停止预览失败');
    }
  };

  const handleSave = async () => {
    if (isSaving) return;

    setIsSaving(true);
    try {
      const response = await fetch(
        `http://${API_BASE_URL}/api/millennium/themes/${themeName}/css`,
        {
          method: 'PUT',
          headers: {
            'Content-Type': 'text/plain',
          },
          body: cssContent,
        }
      );

      if (!response.ok) {
        throw new Error('保存失败');
      }

      toast.success('保存成功');
    } catch (error) {
      toast.error('保存失败');
    } finally {
      setIsSaving(false);
    }
  };

  const handleRefresh = () => {
    if (connected) {
      sendMessage(cssContent);
    }
  };

  const handleCSSChange = (value: string) => {
    setCssContent(value);
    if (connected) {
      sendMessage(value);
    }
  };

  if (!theme) {
    return <div className="p-4">加载中...</div>;
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between p-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div>
          <h1 className="text-2xl font-bold">{theme.config.name}</h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            作者: {theme.config.author} | 版本: {theme.config.version}
          </p>
        </div>
      </div>

      <PreviewControl
        isPreviewActive={isPreviewActive}
        onStartPreview={handleStartPreview}
        onStopPreview={handleStopPreview}
        onSave={handleSave}
        onRefresh={handleRefresh}
        disabled={connecting}
      />

      <div className="flex-1 p-4">
        <CSSEditor
          initialValue={cssContent}
          onChange={handleCSSChange}
          onSave={handleSave}
        />
      </div>
    </div>
  );
};

export default Editor; 