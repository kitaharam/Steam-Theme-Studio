import { Link, useLocation } from 'react-router-dom'
import {
  HomeIcon,
  PencilSquareIcon,
  SwatchIcon,
  FolderIcon,
} from '@heroicons/react/24/outline'

const navigation = [
  { name: '主页', href: '/', icon: HomeIcon },
  { name: '编辑器', href: '/editor', icon: PencilSquareIcon },
  { name: '主题', href: '/themes', icon: SwatchIcon },
  { name: '资源', href: '/resources', icon: FolderIcon },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <div className="w-16 bg-secondary flex flex-col items-center py-4 space-y-4">
      {navigation.map((item) => {
        const isActive = location.pathname === item.href
        const Icon = item.icon
        return (
          <Link
            key={item.name}
            to={item.href}
            className={`p-2 rounded-lg transition-colors ${
              isActive
                ? 'bg-accent text-white'
                : 'text-text-secondary hover:bg-primary'
            }`}
            title={item.name}
          >
            <Icon className="w-6 h-6" />
          </Link>
        )
      })}
    </div>
  )
} 