// API配置
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'localhost:8000';

// WebSocket配置
export const WS_RECONNECT_ATTEMPTS = 3;
export const WS_RECONNECT_INTERVAL = 3000;

// 主题配置
export const DEFAULT_THEME = {
  name: '新主题',
  author: '未知',
  version: '1.0.0',
  description: '这是一个新的Steam主题',
};

// 编辑器配置
export const EDITOR_CONFIG = {
  fontSize: 14,
  tabSize: 2,
  insertSpaces: true,
  minimap: true,
  wordWrap: 'on',
  lineNumbers: 'on',
  folding: true,
  autoClosingBrackets: 'always',
  autoClosingQuotes: 'always',
  formatOnPaste: true,
  formatOnType: true,
}; 