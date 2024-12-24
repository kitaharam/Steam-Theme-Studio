import { Link } from 'react-router-dom'
import { HomeIcon } from '@heroicons/react/24/outline'

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <h1 className="text-4xl font-bold mb-4">404</h1>
      <p className="text-text-secondary mb-8">页面未找到</p>
      <Link
        to="/"
        className="flex items-center space-x-2 px-4 py-2 bg-accent rounded-lg hover:bg-opacity-80 transition-colors"
      >
        <HomeIcon className="w-5 h-5" />
        <span>返回首页</span>
      </Link>
    </div>
  )
} 