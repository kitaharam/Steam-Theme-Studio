import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from './App'

test('renders main navigation', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  )
  
  // 验证导航链接是否存在
  expect(screen.getByTitle('主页')).toBeInTheDocument()
  expect(screen.getByTitle('编辑器')).toBeInTheDocument()
  expect(screen.getByTitle('主题')).toBeInTheDocument()
  expect(screen.getByTitle('资源')).toBeInTheDocument()
}) 