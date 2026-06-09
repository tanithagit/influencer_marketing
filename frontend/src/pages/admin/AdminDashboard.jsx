import { useState, useEffect } from 'react'
import AdminLayout from '../../components/admin/AdminLayout'
import api from '../../services/api'
import Spinner from '../../components/common/Spinner'
import {
  Users,
  Megaphone,
  DollarSign,
  TrendingUp,
  Building2,
  UserCheck
} from 'lucide-react'

function StatCard({ title, value, icon: Icon, color, bg }) {
  return (
    <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm font-medium text-gray-500">{title}</p>
        <div className={`w-10 h-10 ${bg} rounded-lg flex items-center justify-center`}>
          <Icon size={20} className={color} />
        </div>
      </div>
      <p className="text-3xl font-bold text-gray-800">{value}</p>
    </div>
  )
}

function AdminDashboard() {
  const [overview, setOverview] = useState(null)
  const [loading,  setLoading]  = useState(true)

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        const res = await api.get('/api/analytics/admin/overview')
        setOverview(res.data)
      } catch (err) {
        console.error('Failed to fetch overview', err)
      } finally {
        setLoading(false)
      }
    }
    fetchOverview()
  }, [])

  if (loading) {
    return (
      <AdminLayout>
        <div className="flex items-center justify-center h-96">
          <Spinner size="lg" />
        </div>
      </AdminLayout>
    )
  }

  return (
    <AdminLayout>
      <div className="p-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">Admin Dashboard</h1>
          <p className="text-gray-500 mt-1">Platform overview and management</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <StatCard
            title="Total Users"
            value={overview?.total_users || 0}
            icon={Users}
            color="text-blue-600"
            bg="bg-blue-50"
          />
          <StatCard
            title="Total Brands"
            value={overview?.total_brands || 0}
            icon={Building2}
            color="text-purple-600"
            bg="bg-purple-50"
          />
          <StatCard
            title="Total Influencers"
            value={overview?.total_influencers || 0}
            icon={UserCheck}
            color="text-pink-600"
            bg="bg-pink-50"
          />
          <StatCard
            title="Total Campaigns"
            value={overview?.total_campaigns || 0}
            icon={Megaphone}
            color="text-orange-600"
            bg="bg-orange-50"
          />
          <StatCard
            title="Total Payments"
            value={overview?.total_payments || 0}
            icon={DollarSign}
            color="text-green-600"
            bg="bg-green-50"
          />
          <StatCard
            title="Total Revenue"
            value={`$${overview?.total_revenue?.toFixed(2) || '0.00'}`}
            icon={TrendingUp}
            color="text-red-600"
            bg="bg-red-50"
          />
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-800 mb-2">
              Platform Summary
            </h3>
            <div className="space-y-3 mt-4">
              <div className="flex justify-between items-center py-2 border-b border-gray-100">
                <span className="text-sm text-gray-500">Total Users</span>
                <span className="font-semibold text-gray-800">
                  {overview?.total_users || 0}
                </span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-gray-100">
                <span className="text-sm text-gray-500">Active Campaigns</span>
                <span className="font-semibold text-gray-800">
                  {overview?.total_campaigns || 0}
                </span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-gray-100">
                <span className="text-sm text-gray-500">Payments Processed</span>
                <span className="font-semibold text-gray-800">
                  {overview?.total_payments || 0}
                </span>
              </div>
              <div className="flex justify-between items-center py-2">
                <span className="text-sm text-gray-500">Revenue Generated</span>
                <span className="font-semibold text-green-600">
                  ${overview?.total_revenue?.toFixed(2) || '0.00'}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-800 mb-4">Quick Actions</h3>
            <div className="space-y-3">
                <a
                href="/admin/users"
                className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg hover:bg-blue-100 transition"
              >
                <Users size={18} className="text-blue-600" />
                <span className="text-sm font-medium text-blue-700">
                  Manage Users
                </span>
              </a>
                <a
                href="/admin/campaigns"
                className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg hover:bg-purple-100 transition"
              >
                <Megaphone size={18} className="text-purple-600" />
                <span className="text-sm font-medium text-purple-700">
                  View All Campaigns
                </span>
              </a>
                <a
                href="/admin/payments"
                className="flex items-center gap-3 p-3 bg-green-50 rounded-lg hover:bg-green-100 transition"
              >
                <DollarSign size={18} className="text-green-600" />
                <span className="text-sm font-medium text-green-700">
                  Monitor Payments
                </span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </AdminLayout>
  )
}

export default AdminDashboard