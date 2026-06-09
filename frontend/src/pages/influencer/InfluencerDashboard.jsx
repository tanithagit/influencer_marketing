import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import InfluencerLayout from '../../components/influencer/InfluencerLayout'
import { analyticsAPI } from '../../services/api'
import Spinner from '../../components/common/Spinner'
import {
  FileText,
  CheckCircle,
  DollarSign,
  Upload,
  ArrowRight,
  TrendingUp
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

function InfluencerDashboard() {
  const [analytics, setAnalytics] = useState(null)
  const [loading,   setLoading]   = useState(true)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const res = await analyticsAPI.influencerDashboard()
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
      <InfluencerLayout>
        <div className="flex items-center justify-center h-96">
          <Spinner size="lg" />
        </div>
      </InfluencerLayout>
    )
  }

  return (
    <InfluencerLayout>
      <div className="p-8">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
            <p className="text-gray-500 mt-1">Track your campaigns and earnings</p>
          </div>
          <Link
            to="/influencer/campaigns"
            className="flex items-center gap-2 bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-lg transition text-sm font-medium"
          >
            Browse Campaigns
          </Link>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Applications"
            value={analytics?.total_applications || 0}
            icon={FileText}
            color="text-blue-600"
            bg="bg-blue-50"
          />
          <StatCard
            title="Approved"
            value={analytics?.approved_applications || 0}
            icon={CheckCircle}
            color="text-green-600"
            bg="bg-green-50"
          />
          <StatCard
            title="Total Earnings"
            value={`$${analytics?.total_earnings?.toFixed(2) || '0.00'}`}
            icon={DollarSign}
            color="text-pink-600"
            bg="bg-pink-50"
          />
          <StatCard
            title="Success Rate"
            value={`${analytics?.deliverable_success_rate || 0}%`}
            icon={TrendingUp}
            color="text-orange-600"
            bg="bg-orange-50"
          />
        </div>

        {/* Secondary Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

          {/* Application Stats */}
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <FileText size={18} className="text-blue-600" />
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

          {/* Earnings Stats */}
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <DollarSign size={18} className="text-pink-600" />
              Earnings
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Released</span>
                <span className="text-sm font-semibold text-green-600">
                  ${analytics?.released_earnings?.toFixed(2) || '0.00'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Pending</span>
                <span className="text-sm font-semibold text-yellow-600">
                  ${analytics?.pending_earnings?.toFixed(2) || '0.00'}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Total</span>
                <span className="text-sm font-semibold text-blue-600">
                  ${analytics?.total_earnings?.toFixed(2) || '0.00'}
                </span>
              </div>
            </div>
          </div>

          {/* Deliverable Stats */}
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-700 mb-4 flex items-center gap-2">
              <Upload size={18} className="text-orange-600" />
              Deliverables
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Total</span>
                <span className="text-sm font-semibold text-gray-700">
                  {analytics?.total_deliverables || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Approved</span>
                <span className="text-sm font-semibold text-green-600">
                  {analytics?.approved_deliverables || 0}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-500">Rejected</span>
                <span className="text-sm font-semibold text-red-500">
                  {analytics?.rejected_deliverables || 0}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Links */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link
            to="/influencer/campaigns"
            className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm hover:border-pink-300 transition group"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-800">Browse Campaigns</h3>
                <p className="text-sm text-gray-500 mt-1">
                  Find new campaigns to apply
                </p>
              </div>
              <ArrowRight
                size={20}
                className="text-gray-400 group-hover:text-pink-500 transition"
              />
            </div>
          </Link>

          <Link
            to="/influencer/deliverables"
            className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm hover:border-pink-300 transition group"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-gray-800">Submit Deliverables</h3>
                <p className="text-sm text-gray-500 mt-1">
                  Upload content for approved campaigns
                </p>
              </div>
              <ArrowRight
                size={20}
                className="text-gray-400 group-hover:text-pink-500 transition"
              />
            </div>
          </Link>
        </div>
      </div>
    </InfluencerLayout>
  )
}

export default InfluencerDashboard