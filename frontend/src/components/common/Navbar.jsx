import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { LogOut, User, LayoutDashboard } from 'lucide-react'

function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const getDashboardLink = () => {
    if (user?.role === 'brand')      return '/brand/dashboard'
    if (user?.role === 'influencer') return '/influencer/dashboard'
    if (user?.role === 'admin')      return '/admin/dashboard'
    return '/'
  }

  return (
    <nav className="bg-white border-b border-gray-200 px-6 py-4">
      <div className="max-w-7xl mx-auto flex items-center justify-between">

        {/* Logo */}
        <Link to="/" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">IM</span>
          </div>
          <span className="font-bold text-gray-800 text-lg">
            InfluencerHub
          </span>
        </Link>

        {/* Right side */}
        {user && (
          <div className="flex items-center gap-4">
            <Link
              to={getDashboardLink()}
              className="flex items-center gap-2 text-gray-600 hover:text-purple-600 transition"
            >
              <LayoutDashboard size={18} />
              <span className="text-sm font-medium">Dashboard</span>
            </Link>

            <div className="flex items-center gap-2 text-gray-600">
              <User size={18} />
              <span className="text-sm font-medium">{user.full_name}</span>
              <span className="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full capitalize">
                {user.role}
              </span>
            </div>

            <button
              onClick={handleLogout}
              className="flex items-center gap-2 text-red-500 hover:text-red-700 transition text-sm"
            >
              <LogOut size={18} />
              Logout
            </button>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navbar