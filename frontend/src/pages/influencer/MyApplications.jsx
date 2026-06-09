import { useState, useEffect } from 'react'
import InfluencerLayout from '../../components/influencer/InfluencerLayout'
import { applicationAPI } from '../../services/api'
import Spinner from '../../components/common/Spinner'
import { FileText } from 'lucide-react'

function StatusBadge({ status }) {
  const styles = {
    pending:  'bg-yellow-100 text-yellow-700',
    approved: 'bg-green-100 text-green-700',
    rejected: 'bg-red-100 text-red-700',
  }
  return (
    <span className={`text-xs font-medium px-3 py-1 rounded-full capitalize ${styles[status]}`}>
      {status}
    </span>
  )
}

function MyApplications() {
  const [applications, setApplications] = useState([])
  const [loading,      setLoading]      = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await applicationAPI.getMine()
        setApplications(res.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  return (
    <InfluencerLayout>
      <div className="p-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">My Applications</h1>
          <p className="text-gray-500 mt-1">Track all your campaign applications</p>
        </div>

        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        ) : applications.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-xl border border-gray-100">
            <FileText size={48} className="text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 font-medium">No applications yet</p>
            <p className="text-gray-400 text-sm mt-1">
              Browse campaigns and start applying!
            </p>
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
                      <p className="font-semibold text-gray-800">
                        Campaign #{app.campaign_id}
                      </p>
                      <StatusBadge status={app.status} />
                    </div>
                    {app.proposal_message && (
                      <p className="text-gray-500 text-sm bg-gray-50 p-3 rounded-lg mt-2">
                        "{app.proposal_message}"
                      </p>
                    )}
                    <div className="flex items-center gap-4 mt-3 text-xs text-gray-400">
                      <span>
                        Applied: {new Date(app.applied_at).toLocaleDateString()}
                      </span>
                      {app.proposed_rate && (
                        <span className="text-green-600 font-medium">
                          Rate: ${app.proposed_rate}
                        </span>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </InfluencerLayout>
  )
}

export default MyApplications