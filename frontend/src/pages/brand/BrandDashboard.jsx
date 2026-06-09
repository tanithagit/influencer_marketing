import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import BrandLayout from '../../components/brand/BrandLayout'
import { analyticsAPI } from '../../services/api'
import Spinner from '../../components/common/Spinner'
import {
  Megaphone,
  Users,
  DollarSign,
  FileCheck,
  TrendingUp,
  Plus,
  ArrowRight
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

function BrandDashboard() {
  const [analytics, setAnalytics] = useState(null)
  const [loading,   setLoading]   = useState(true)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await analyticsAPI.brandDashboard()
        setAnalytics(res.data)
      } catch (err) {
        console.error('Failed to fetch analytics', err)
      } finally {
        setLoading(false)
      }
    }
    fetchAnalytics()
  }, [])

  if (loading) {
    return (
      <BrandLayout>
        <div className="flex items-center justify-center h-96">
          <Spinner size="lg" />
        </div>
      </BrandLayout>
    )
  }

  return (
    <BrandLayout>
      <div className="p-8">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
            <p className="text-gray-500 mt-1">Overview of your campaigns</p>
          </div>
          <Link
            to="/brand/campaigns/create"
            className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition text-sm font-medium"
          >
            <Plus size={16} />
            New Campaign
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Campaigns"
            value={analytics?.total_campaigns || 0}
            icon={Megaphone}
            color="text-purple-600"
            bg="bg-purple-50"
          />
          <StatCard
            title="Total Applications"
            value={analytics?.total_applications || 0}
            icon={Users}
            color="text-blue-600"
            bg="bg-blue-50"
          />
          <StatCard
            title="Budget Spent"
            value={`$${analytics?.total_budget_spent?.toFixed(2) || '0.00'}`}
            icon={DollarSign}
            color="text-green-600"
            bg="bg-green-50"
          />
          <StatCard
            title="Approved Deliverables"
            value={analytics?.approved_deliverables || 0}
            icon={FileCheck}
            color="text-orange-600"
            bg="bg-orange-50"
          />
        </div>

        {/* Secondary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <Megaphone size={18} className="text-purple-600" />
              Campaign Status
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Active</span>
                <span className="text-sm font-semibold text-green-600">
                  {analytics?.active_campaigns || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Completed</span>
                <span className="text-sm font-semibold text-blue-600">
                  {analytics?.completed_campaigns || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Cancelled</span>
                <span className="text-sm font-semibold text-red-500">
                  {analytics?.cancelled_campaigns || 0}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <Users size={18} className="text-blue-600" />
              Application Status
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Pending</span>
                <span className="text-sm font-semibold text-yellow-600">
                  {analytics?.pending_applications || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Approved</span>
                <span className="text-sm font-semibold text-green-600">
                  {analytics?.approved_applications || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Rejected</span>
                <span className="text-sm font-semibold text-red-500">
                  {analytics?.rejected_applications || 0}
                </span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <DollarSign size={18} className="text-green-600" />
              Payment Summary
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Released</span>
                <span className="text-sm font-semibold text-green-600">
                  ${analytics?.total_budget_spent?.toFixed(2) || '0.00'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">In Escrow</span>
                <span className="text-sm font-semibold text-yellow-600">
                  ${analytics?.escrowed_amount?.toFixed(2) || '0.00'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Total Paid</span>
                <span className="text-sm font-semibold text-blue-600">
                  {analytics?.total_payments_made || 0} payments
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link
            to="/brand/campaigns"
            className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm hover:border-purple-300 transition group"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-800">Manage Campaigns</h3>
                <p className="text-sm text-gray-500 mt-1">
                  View and manage all your campaigns
                </p>
              </div>
              <ArrowRight
                size={20}
                className="text-gray-400 group-hover:text-purple-600 transition"
              />
            </div>
          </Link>

          <Link
            to="/brand/applications"
            className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm hover:border-purple-300 transition group"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-800">Review Applications</h3>
                <p className="text-sm text-gray-500 mt-1">
                  {analytics?.pending_applications || 0} pending applications
                </p>
              </div>
              <ArrowRight
                size={20}
                className="text-gray-400 group-hover:text-purple-600 transition"
              />
            </div>
          </Link>
        </div>
      </div>
    </BrandLayout>
  )
}

export default BrandDashboard