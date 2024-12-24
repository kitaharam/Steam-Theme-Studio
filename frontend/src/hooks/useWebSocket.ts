import { useEffect, useRef, useState, useCallback } from 'react';
import { WebSocketService } from '@/services/ws';

interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
  autoConnect?: boolean;
}

export function useWebSocket({
  url,
  onMessage,
  onOpen,
  onClose,
  onError,
  autoConnect = true,
}: UseWebSocketOptions) {
  const [connected, setConnected] = useState(false);
  const [connecting, setConnecting] = useState(false);
  const wsRef = useRef<WebSocketService | null>(null);

  const connect = useCallback(() => {
    if (!wsRef.current) {
      setConnecting(true);
      wsRef.current = new WebSocketService({
        onOpen: () => {
          setConnected(true);
          setConnecting(false);
          onOpen?.();
        },
        onClose: () => {
          setConnected(false);
          setConnecting(false);
          onClose?.();
        },
        onError: (error) => {
          setConnecting(false);
          onError?.(error);
        },
        onMessage,
      });
    }
    wsRef.current.connect(url);
  }, [url, onMessage, onOpen, onClose, onError]);

  const disconnect = useCallback(() => {
    if (wsRef.current) {
      wsRef.current.disconnect();
      wsRef.current = null;
    }
  }, []);

  const send = useCallback((data: any) => {
    if (wsRef.current) {
      wsRef.current.send(data);
    }
  }, []);

  useEffect(() => {
    if (autoConnect) {
      connect();
    }

    return () => {
      disconnect();
    };
  }, [autoConnect, connect, disconnect]);

  return {
    connected,
    connecting,
    connect,
    disconnect,
    send,
  };
}

export default useWebSocket; 