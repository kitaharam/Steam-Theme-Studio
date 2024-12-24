import { Link } from 'react-router-dom'
import { Cog6ToothIcon } from '@heroicons/react/24/outline'

export default function Navbar() {
  return (
    <nav className="bg-secondary h-14 px-4 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <h1 className="text-xl font-semibold text-text-primary">Steam Theme Studio</h1>
      </div>
      <div className="flex items-center space-x-4">
        <Link
          to="/settings"
          className="p-2 hover:bg-primary rounded-lg transition-colors"
          title="设置"
        >
          <Cog6ToothIcon className="w-6 h-6 text-text-secondary" />
        </Link>
      </div>
    </nav>
  )
} 