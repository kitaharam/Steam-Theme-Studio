import React from 'react';
import { Button } from '@/components/ui/button';

interface PreviewControlProps {
  isPreviewActive: boolean;
  onStartPreview: () => void;
  onStopPreview: () => void;
  onSave: () => void;
  onRefresh: () => void;
  disabled?: boolean;
}

const PreviewControl: React.FC<PreviewControlProps> = ({
  isPreviewActive,
  onStartPreview,
  onStopPreview,
  onSave,
  onRefresh,
  disabled,
}) => {
  return (
    <div className="flex items-center space-x-2 p-4 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
      <Button
        variant="primary"
        onClick={isPreviewActive ? onStopPreview : onStartPreview}
        disabled={disabled}
      >
        {isPreviewActive ? '停止预览' : '开始预览'}
      </Button>
      
      <Button
        variant="secondary"
        onClick={onRefresh}
        disabled={!isPreviewActive || disabled}
      >
        刷新预览
      </Button>

      <div className="flex-1" />

      <Button
        variant="outline"
        onClick={onSave}
        disabled={disabled}
      >
        保存
      </Button>
    </div>
  );
};

export default PreviewControl; 