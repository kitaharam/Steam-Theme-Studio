import React from 'react';
import { Link } from 'react-router-dom';

interface Theme {
  id: string;
  name: string;
  description: string;
  author: string;
  createdAt: string;
  updatedAt: string;
}

interface ThemeListProps {
  themes: Theme[];
  onDelete?: (id: string) => void;
}

const ThemeList: React.FC<ThemeListProps> = ({ themes, onDelete }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {themes.map((theme) => (
        <div
          key={theme.id}
          className="bg-secondary rounded-lg p-4 hover:bg-opacity-80 transition-colors"
        >
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-lg font-semibold">
              <Link to={`/editor/${theme.id}`} className="hover:text-primary">
                {theme.name}
              </Link>
            </h3>
            <div className="flex space-x-2">
              <button
                onClick={() => onDelete?.(theme.id)}
                className="text-red-500 hover:text-red-600"
              >
                删除
              </button>
            </div>
          </div>
          <p className="text-sm text-text-secondary mb-4">{theme.description}</p>
          <div className="flex justify-between text-xs text-text-secondary">
            <span>作者: {theme.author}</span>
            <span>更新于: {new Date(theme.updatedAt).toLocaleDateString()}</span>
          </div>
        </div>
      ))}
      
      <Link
        to="/editor/new"
        className="flex items-center justify-center bg-secondary rounded-lg p-4 hover:bg-opacity-80 transition-colors border-2 border-dashed border-gray-600"
      >
        <div className="text-center">
          <div className="text-4xl mb-2">+</div>
          <div>创建新主题</div>
        </div>
      </Link>
    </div>
  );
};

export default ThemeList; 