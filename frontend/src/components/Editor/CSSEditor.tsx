import React, { useEffect, useRef, useState } from 'react';
import * as monaco from 'monaco-editor';
import { useTheme } from '@/hooks/useTheme';

interface CSSEditorProps {
  initialValue?: string;
  onChange?: (value: string) => void;
  onSave?: (value: string) => void;
}

const CSSEditor: React.FC<CSSEditorProps> = ({
  initialValue = '',
  onChange,
  onSave,
}) => {
  const editorRef = useRef<HTMLDivElement>(null);
  const [editor, setEditor] = useState<monaco.editor.IStandaloneCodeEditor | null>(null);
  const { isDarkMode } = useTheme();

  useEffect(() => {
    if (editorRef.current) {
      const newEditor = monaco.editor.create(editorRef.current, {
        value: initialValue,
        language: 'css',
        theme: isDarkMode ? 'vs-dark' : 'vs-light',
        automaticLayout: true,
        minimap: {
          enabled: true,
        },
        fontSize: 14,
        lineNumbers: 'on',
        roundedSelection: false,
        scrollBeyondLastLine: false,
        readOnly: false,
        cursorStyle: 'line',
        wordWrap: 'on',
        folding: true,
        lineDecorationsWidth: 0,
        contextmenu: true,
        scrollbar: {
          verticalScrollbarSize: 10,
          horizontalScrollbarSize: 10,
        },
      });

      setEditor(newEditor);

      // 监听内容变化
      newEditor.onDidChangeModelContent(() => {
        const value = newEditor.getValue();
        onChange?.(value);
      });

      // 监听保存快捷键
      newEditor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.KeyS, () => {
        const value = newEditor.getValue();
        onSave?.(value);
      });

      return () => {
        newEditor.dispose();
      };
    }
  }, [initialValue]);

  // 主题变化时更新编辑器主题
  useEffect(() => {
    if (editor) {
      monaco.editor.setTheme(isDarkMode ? 'vs-dark' : 'vs-light');
    }
  }, [isDarkMode, editor]);

  return (
    <div className="w-full h-full min-h-[500px] border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
      <div ref={editorRef} className="w-full h-full" />
    </div>
  );
};

export default CSSEditor; 