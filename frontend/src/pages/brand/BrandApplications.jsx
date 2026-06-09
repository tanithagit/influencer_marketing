import { useState, useEffect } from 'react'
import BrandLayout from '../../components/brand/BrandLayout'
import { applicationAPI, campaignAPI, paymentAPI } from '../../services/api'
import Spinner from '../../components/common/Spinner'
import toast from 'react-hot-toast'
import { CheckCircle, XCircle, DollarSign, User } from 'lucide-react'

function StatusBadge({ status }) {
  const styles = {
    pending:  'bg-yellow-100 text-yellow-700',
    approved: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
  }
  return (
    <span className={`text-xs font-medium px-2 py-1 rounded-full capitalize ${styles[status]}`}>
      {status}
    </span>
  )
}

function BrandApplications() {
  const [campaigns,    setCampaigns]    = useState([])
  const [applications, setApplications] = useState([])
  const [selectedCamp, setSelectedCamp] = useState(null)
  const [loading,      setLoading]      = useState(true)

  useEffect(() => {
    fetchCampaigns()
  }, [])

  const fetchCampaigns = async () => {
    try {
      const res = await campaignAPI.getMine()
      setCampaigns(res.data)
      if (res.data.length > 0) {
        setSelectedCamp(res.data[0].id)
        fetchApplications(res.data[0].id)
      }
    } catch (err) {
      toast.error('Failed to load campaigns')
    } finally {
      setLoading(false)
    }
  }

  const fetchApplications = async (campaignId) => {
    try {
      const res = await applicationAPI.getCampaignApps(campaignId)
      setApplications(res.data)
    } catch (err) {
      setApplications([])
    }
  }

  const handleCampaignChange = (id) => {
    setSelectedCamp(id)
    fetchApplications(id)
  }

  const handleApprove = async (id) => {
    try {
      await applicationAPI.approve(id)
      toast.success('Application approved!')
      fetchApplications(selectedCamp)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to approve')
    }
  }

  const handleReject = async (id) => {
    try {
      await applicationAPI.reject(id)
      toast.success('Application rejected')
      fetchApplications(selectedCamp)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to reject')
    }
  }

  const handleCreatePayment = async (influencerId, amount) => {
    try {
      await paymentAPI.createIntent({
        campaign_id:   selectedCamp,
        influencer_id: influencerId,
        amount:        amount
      })
      toast.success('Payment escrowed successfully!')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Payment failed')
    }
  }

  return (
    <BrandLayout>
      <div className="p-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">Applications</h1>
          <p className="text-gray-500 mt-1">Review influencer applications</p>
        </div>

        {/* Campaign Selector */}
        {campaigns.length > 0 && (
          <div className="mb-6">
            <select
              value={selectedCamp || ''}
              onChange={(e) => handleCampaignChange(Number(e.target.value))}
              className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              {campaigns.map((c) => (
                <option key={c.id} value={c.id}>{c.title}</option>
              ))}
            </select>
          </div>
        )}

        {/* Applications List */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        ) : applications.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-xl border border-gray-100">
            <p className="text-gray-500">No applications yet for this campaign</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {applications.map((app) => (
              <div
                key={app.id}
                className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <div className="w-9 h-9 bg-purple-100 rounded-full flex items-center justify-center">
                        <User size={16} className="text-purple-600" />
                      </div>
                      <div>
                        <p className="font-semibold text-gray-800">
                          Influencer #{app.influencer_id}
                        </p>
                        <p className="text-xs text-gray-500">
                          Applied {new Date(app.applied_at).toLocaleDateString()}
                        </p>
                      </div>
                      <StatusBadge status={app.status} />
                    </div>

                    {app.proposal_message && (
                      <p className="text-gray-600 text-sm mt-2 bg-gray-50 p-3 rounded-lg">
                        "{app.proposal_message}"
                      </p>
                    )}

                    {app.proposed_rate && (
                      <p className="text-sm text-green-600 mt-2 font-medium">
                        Proposed Rate: ${app.proposed_rate}
                      </p>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2 ml-4">
                    {app.status === 'pending' && (
                      <>
                        <button
                          onClick={() => handleApprove(app.id)}
                          className="flex items-center gap-1 bg-green-50 text-green-700 hover:bg-green-100 px-3 py-1.5 rounded-lg text-sm font-medium transition"
                        >
                          <CheckCircle size={14} />
                          Approve
                        </button>
                        <button
                          onClick={() => handleReject(app.id)}
                          className="flex items-center gap-1 bg-red-50 text-red-700 hover:bg-red-100 px-3 py-1.5 rounded-lg text-sm font-medium transition"
                        >
                          <XCircle size={14} />
                          Reject
                        </button>
                      </>
                    )}
                    {app.status === 'approved' && (
                      <button
                        onClick={() => handleCreatePayment(
                          app.influencer_id,
                          app.proposed_rate || 100
                        )}
                        className="flex items-center gap-1 bg-purple-50 text-purple-700 hover:bg-purple-100 px-3 py-1.5 rounded-lg text-sm font-medium transition"
                      >
                        <DollarSign size={14} />
                        Escrow Payment
                      </button>
                    )}
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

export default BrandApplications