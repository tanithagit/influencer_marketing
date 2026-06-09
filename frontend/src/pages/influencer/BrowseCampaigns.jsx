import { useState, useEffect } from 'react'
import InfluencerLayout from '../../components/influencer/InfluencerLayout'
import { campaignAPI, applicationAPI } from '../../services/api'
import Spinner from '../../components/common/Spinner'
import toast from 'react-hot-toast'
import { DollarSign, Calendar, Search, Send } from 'lucide-react'

function BrowseCampaigns() {
  const [campaigns,  setCampaigns]  = useState([])
  const [loading,    setLoading]    = useState(true)
  const [applying,   setApplying]   = useState(null)
  const [search,     setSearch]     = useState('')
  const [proposal,   setProposal]   = useState({})
  const [showModal,  setShowModal]  = useState(null)

  useEffect(() => {
    fetchCampaigns()
  }, [])

  const fetchCampaigns = async (niche = '') => {
    try {
      const res = await campaignAPI.list({ niche })
      setCampaigns(res.data)
    } catch (err) {
      toast.error('Failed to load campaigns')
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    fetchCampaigns(search)
  }

  const handleApply = async (campaignId) => {
    setApplying(campaignId)
    try {
      await applicationAPI.apply(campaignId, {
        proposal_message: proposal[campaignId] || '',
        proposed_rate:    null
      })
      toast.success('Application submitted!')
      setShowModal(null)
      setProposal({})
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to apply')
    } finally {
      setApplying(null)
    }
  }

  return (
    <InfluencerLayout>
      <div className="p-8">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">Browse Campaigns</h1>
          <p className="text-gray-500 mt-1">Find campaigns that match your niche</p>
        </div>

        {/* Search */}
        <form onSubmit={handleSearch} className="flex gap-3 mb-8">
          <div className="flex-1 relative">
            <Search
              size={18}
              className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"
            />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search by niche (Technology, Fashion...)"
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 transition"
            />
          </div>
          <button
            type="submit"
            className="bg-pink-500 hover:bg-pink-600 text-white px-6 py-3 rounded-lg transition font-medium"
          >
            Search
          </button>
        </form>

        {/* Campaigns Grid */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        ) : campaigns.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-xl border border-gray-100">
            <p className="text-gray-500">No campaigns found</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {campaigns.map((campaign) => (
              <div
                key={campaign.id}
                className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm hover:border-pink-200 transition"
              >
                {/* Campaign Header */}
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h3 className="font-semibold text-gray-800 text-lg">
                      {campaign.title}
                    </h3>
                    {campaign.niche && (
                      <span className="text-xs bg-pink-50 text-pink-600 px-2 py-0.5 rounded-full mt-1 inline-block">
                        {campaign.niche}
                      </span>
                    )}
                  </div>
                  <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full font-medium">
                    Active
                  </span>
                </div>

                {/* Description */}
                <p className="text-gray-500 text-sm mb-4 line-clamp-2">
                  {campaign.description}
                </p>

                {/* Requirements */}
                {campaign.requirements && (
                  <div className="bg-gray-50 rounded-lg p-3 mb-4">
                    <p className="text-xs font-medium text-gray-600 mb-1">
                      Requirements:
                    </p>
                    <p className="text-xs text-gray-500">{campaign.requirements}</p>
                  </div>
                )}

                {/* Stats */}
                <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                  <span className="flex items-center gap-1">
                    <DollarSign size={14} className="text-green-500" />
                    Budget: ${campaign.budget}
                  </span>
                  <span className="flex items-center gap-1">
                    <Calendar size={14} className="text-blue-500" />
                    {new Date(campaign.end_date).toLocaleDateString()}
                  </span>
                </div>

                {/* Apply Button */}
                {showModal === campaign.id ? (
                  <div className="space-y-3">
                    <textarea
                      value={proposal[campaign.id] || ''}
                      onChange={(e) => setProposal({
                        ...proposal,
                        [campaign.id]: e.target.value
                      })}
                      placeholder="Write your proposal message..."
                      rows={3}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-pink-400 resize-none"
                    />
                    <div className="flex gap-2">
                      <button
                        onClick={() => setShowModal(null)}
                        className="flex-1 px-3 py-2 border border-gray-300 text-gray-600 rounded-lg text-sm hover:bg-gray-50 transition"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={() => handleApply(campaign.id)}
                        disabled={applying === campaign.id}
                        className="flex-1 bg-pink-500 hover:bg-pink-600 text-white px-3 py-2 rounded-lg text-sm font-medium transition disabled:opacity-50 flex items-center justify-center gap-1"
                      >
                        {applying === campaign.id ? (
                          <Spinner size="sm" />
                        ) : (
                          <>
                            <Send size={14} />
                            Submit
                          </>
                        )}
                      </button>
                    </div>
                  </div>
                ) : (
                  <button
                    onClick={() => setShowModal(campaign.id)}
                    className="w-full bg-pink-500 hover:bg-pink-600 text-white py-2 rounded-lg text-sm font-medium transition"
                  >
                    Apply Now
                  </button>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </InfluencerLayout>
  )
}

export default BrowseCampaigns