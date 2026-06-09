import { useState, useEffect } from 'react'
import AdminLayout from '../../components/admin/AdminLayout'
import api from '../../services/api'
import Spinner from '../../components/common/Spinner'
import { DollarSign, Calendar } from 'lucide-react'

function AdminCampaigns() {
  const [campaigns, setCampaigns] = useState([])
  const [loading,   setLoading]   = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await api.get('/api/campaigns/admin/all')
        setCampaigns(res.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  const statusStyles = {
    active:    'bg-green-100 text-green-700',
    paused:    'bg-yellow-100 text-yellow-700',
    completed: 'bg-blue-100 text-blue-700',
    cancelled: 'bg-red-100 text-red-700',
    draft:     'bg-gray-100 text-gray-700',
  }

  return (
    <AdminLayout>
      <div className="p-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">All Campaigns</h1>
          <p className="text-gray-500 mt-1">Monitor all platform campaigns</p>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        ) : campaigns.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-xl border border-gray-100">
            <p className="text-gray-500">No campaigns found</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {campaigns.map((campaign) => (
              <div
                key={campaign.id}
                className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="font-semibold text-gray-800">
                        {campaign.title}
                      </h3>
                      <span className={`text-xs font-medium px-2 py-1 rounded-full capitalize ${statusStyles[campaign.status] || statusStyles.draft}`}>
                        {campaign.status}
                      </span>
                    </div>
                    <p className="text-gray-500 text-sm mb-3 line-clamp-1">
                      {campaign.description}
                    </p>
                    <div className="flex items-center gap-6 text-sm text-gray-500">
                      <span className="flex items-center gap-1">
                        <DollarSign size={14} />
                        Budget: ${campaign.budget}
                      </span>
                      <span className="flex items-center gap-1">
                        <Calendar size={14} />
                        Ends: {new Date(campaign.end_date).toLocaleDateString()}
                      </span>
                      {campaign.niche && (
                        <span className="bg-purple-50 text-purple-700 px-2 py-0.5 rounded-full text-xs">
                          {campaign.niche}
                        </span>
                      )}
                      <span className="text-xs text-gray-400">
                        Brand ID: {campaign.brand_id}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </AdminLayout>
  )
}

export default AdminCampaigns