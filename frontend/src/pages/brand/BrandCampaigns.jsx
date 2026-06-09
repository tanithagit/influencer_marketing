import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import BrandLayout from '../../components/brand/BrandLayout'
import { campaignAPI } from '../../services/api'
import Spinner from '../../components/common/Spinner'
import toast from 'react-hot-toast'
import { Plus, Calendar, DollarSign, Users, Trash2 } from 'lucide-react'

function StatusBadge({ status }) {
  const styles = {
    active:    'bg-green-100 text-green-700',
    paused:    'bg-yellow-100 text-yellow-700',
    completed: 'bg-blue-100 text-blue-700',
    cancelled: 'bg-red-100 text-red-700',
    draft:     'bg-gray-100 text-gray-700',
  }
  return (
    <span className={`text-xs font-medium px-2 py-1 rounded-full capitalize ${styles[status] || styles.draft}`}>
      {status}
    </span>
  )
}

function BrandCampaigns() {
  const [campaigns, setCampaigns] = useState([])
  const [loading,   setLoading]   = useState(true)

  useEffect(() => {
    fetchCampaigns()
  }, [])

  const fetchCampaigns = async () => {
    try {
      const res = await campaignAPI.getMine()
      setCampaigns(res.data)
    } catch (err) {
      toast.error('Failed to load campaigns')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Cancel this campaign?')) return
    try {
      await campaignAPI.delete(id)
      toast.success('Campaign cancelled')
      fetchCampaigns()
    } catch (err) {
      toast.error('Failed to cancel campaign')
    }
  }

  return (
    <BrandLayout>
      <div className="p-8">

        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">My Campaigns</h1>
            <p className="text-gray-500 mt-1">Manage your marketing campaigns</p>
          </div>
          <Link
            to="/brand/campaigns/create"
            className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg transition text-sm font-medium"
          >
            <Plus size={16} />
            New Campaign
          </Link>
        </div>

        {/* Campaigns List */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        ) : campaigns.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-xl border border-gray-100">
            <Megaphone size={48} className="text-gray-300 mx-auto mb-4" />
            <h3 className="text-gray-500 font-medium">No campaigns yet</h3>
            <p className="text-gray-400 text-sm mt-1">
              Create your first campaign to get started
            </p>
            <Link
              to="/brand/campaigns/create"
              className="inline-flex items-center gap-2 mt-4 bg-purple-600 text-white px-4 py-2 rounded-lg text-sm"
            >
              <Plus size={16} />
              Create Campaign
            </Link>
          </div>
        ) : (
          <div className="grid gap-4">
            {campaigns.map((campaign) => (
              <div
                key={campaign.id}
                className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm hover:border-purple-200 transition"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-gray-800 text-lg">
                        {campaign.title}
                      </h3>
                      <StatusBadge status={campaign.status} />
                    </div>
                    <p className="text-gray-500 text-sm mb-4 line-clamp-2">
                      {campaign.description}
                    </p>
                    <div className="flex items-center gap-6 text-sm text-gray-500">
                      <span className="flex items-center gap-1">
                        <DollarSign size={14} />
                        Budget: ${campaign.budget}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar size={14} />
                        {new Date(campaign.end_date).toLocaleDateString()}
                      </span>
                      {campaign.niche && (
                        <span className="bg-purple-50 text-purple-700 px-2 py-0.5 rounded-full text-xs">
                          {campaign.niche}
                        </span>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-2 ml-4">
                    <Link
                      to={`/brand/campaigns/${campaign.id}/applications`}
                      className="flex items-center gap-1 text-sm text-blue-600 hover:text-blue-800 bg-blue-50 px-3 py-1.5 rounded-lg transition"
                    >
                      <Users size={14} />
                      Applications
                    </Link>
                    <button
                      onClick={() => handleDelete(campaign.id)}
                      className="p-2 text-red-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </BrandLayout>
  )
}

export default BrandCampaigns