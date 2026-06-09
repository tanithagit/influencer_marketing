import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import ProtectedRoute from './components/common/ProtectedRoute'
import Spinner from './components/common/Spinner'

// Auth Pages
import Login    from './pages/auth/Login'
import Register from './pages/auth/Register'

// Brand Pages
import BrandDashboard   from './pages/brand/BrandDashboard'
import BrandCampaigns   from './pages/brand/BrandCampaigns'
import CreateCampaign   from './pages/brand/CreateCampaign'
import BrandApplications from './pages/brand/BrandApplications'

function App() {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Spinner size="lg" />
      </div>
    )
  }

  return (
    <Routes>
      {/* Public Routes */}
      <Route path="/login"    element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Brand Routes */}
      <Route path="/brand/dashboard" element={
        <ProtectedRoute allowedRoles={['brand']}>
          <BrandDashboard />
        </ProtectedRoute>
      } />
      <Route path="/brand/campaigns" element={
        <ProtectedRoute allowedRoles={['brand']}>
          <BrandCampaigns />
        </ProtectedRoute>
      } />
      <Route path="/brand/campaigns/create" element={
        <ProtectedRoute allowedRoles={['brand']}>
          <CreateCampaign />
        </ProtectedRoute>
      } />
      <Route path="/brand/applications" element={
        <ProtectedRoute allowedRoles={['brand']}>
          <BrandApplications />
        </ProtectedRoute>
      } />

      {/* Default redirect */}
      <Route path="/" element={
        user ? (
          <Navigate to={
            user.role === 'brand'      ? '/brand/dashboard' :
            user.role === 'influencer' ? '/influencer/dashboard' :
            '/admin/dashboard'
          } />
        ) : (
          <Navigate to="/login" />
        )
      } />

      {/* 404 */}
      <Route path="*" element={
        <div className="flex items-center justify-center min-h-screen">
          <div className="text-center">
            <h1 className="text-6xl font-bold text-purple-600">404</h1>
            <p className="text-gray-500 mt-2">Page not found</p>
          </div>
        </div>
      } />
    </Routes>
  )
}

export default App