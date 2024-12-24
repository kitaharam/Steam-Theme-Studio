interface WebSocketOptions {
  onMessage?: (data: any) => void;
  onOpen?: () => void;
  onClose?: () => void;
  onError?: (error: Event) => void;
}

export class WebSocketService {
  private ws: WebSocket | null = null;
  private options: WebSocketOptions;

  constructor(options: WebSocketOptions = {}) {
    this.options = options;
  }

  connect(url: string) {
    try {
      console.log('正在连接WebSocket:', url);
      
      if (this.ws) {
        console.log('关闭现有连接');
        this.ws.close();
      }

      this.ws = new WebSocket(url.startsWith('ws') ? url : `ws://${window.location.host}${url}`);

      this.ws.onopen = () => {
        console.log('WebSocket连接已建立');
        this.options.onOpen?.();
      };

      this.ws.onmessage = (event) => {
        console.log('收到WebSocket消息:', event.data);
        try {
          const data = JSON.parse(event.data);
          this.options.onMessage?.(data);
        } catch (error) {
          console.error('WebSocket消息解析错误:', error);
        }
      };

      this.ws.onclose = (event) => {
        console.log('WebSocket连接已关闭:', event.code, event.reason);
        this.ws = null;
        this.options.onClose?.();
      };

      this.ws.onerror = (error) => {
        console.error('WebSocket错误:', error);
        this.options.onError?.(error);
      };
    } catch (error) {
      console.error('WebSocket连接创建失败:', error);
      this.options.onError?.(error as Event);
    }
  }

  disconnect() {
    if (this.ws) {
      console.log('主动断开WebSocket连接');
      this.ws.close();
      this.ws = null;
    }
  }

  send(data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      const message = JSON.stringify(data);
      console.log('发送WebSocket消息:', message);
      this.ws.send(message);
    } else {
      console.error('WebSocket未连接，无法发送消息');
    }
  }

  isConnected() {
    return this.ws?.readyState === WebSocket.OPEN;
  }
} 