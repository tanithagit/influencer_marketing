import { useState, useEffect } from 'react'
import InfluencerLayout from '../../components/influencer/InfluencerLayout'
import { deliverableAPI, applicationAPI } from '../../services/api'
import Spinner from '../../components/common/Spinner'
import toast from 'react-hot-toast'
import { Upload } from 'lucide-react'

function StatusBadge({ status }) {
  if (status === 'approved') {
    return (
      <span className="text-xs font-medium px-3 py-1 rounded-full bg-green-100 text-green-700">
        Approved
      </span>
    )
  }
  if (status === 'rejected') {
    return (
      <span className="text-xs font-medium px-3 py-1 rounded-full bg-red-100 text-red-700">
        Rejected
      </span>
    )
  }
  return (
    <span className="text-xs font-medium px-3 py-1 rounded-full bg-yellow-100 text-yellow-700">
      Pending Review
    </span>
  )
}

function MyDeliverables() {
  const [deliverables, setDeliverables] = useState([])
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [uploading, setUploading] = useState(false)
  const [selectedCamp, setSelectedCamp] = useState('')
  const [file, setFile] = useState(null)
  const [description, setDescription] = useState('')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const delRes = await deliverableAPI.getMine()
      const appRes = await applicationAPI.getMine()
      setDeliverables(delRes.data)
      const approved = appRes.data.filter(function(a) {
        return a.status === 'approved'
      })
      setApplications(approved)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleFileChange = function(e) {
    setFile(e.target.files[0])
  }

  const handleSubmit = async function(e) {
    e.preventDefault()
    if (!file || !selectedCamp) {
      toast.error('Please select a campaign and file')
      return
    }
    setUploading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('description', description)
      await deliverableAPI.submit(selectedCamp, formData)
      toast.success('Deliverable submitted!')
      setFile(null)
      setDescription('')
      setSelectedCamp('')
      fetchData()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

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

        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">Deliverables</h1>
          <p className="text-gray-500 mt-1">Submit content for approved campaigns</p>
        </div>

        {applications.length > 0 && (
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm mb-8">
            <h2 className="font-semibold text-gray-800 mb-4">
              Submit New Deliverable
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Select Campaign
                </label>
                <select
                  value={selectedCamp}
                  onChange={function(e) { setSelectedCamp(e.target.value) }}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
                  required
                >
                  <option value="">Choose approved campaign...</option>
                  {applications.map(function(app) {
                    return (
                      <option key={app.id} value={app.campaign_id}>
                        Campaign number {app.campaign_id}
                      </option>
                    )
                  })}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Upload File
                </label>
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                  <input
                    type="file"
                    onChange={handleFileChange}
                    accept="image/*,video/mp4,application/pdf"
                    className="hidden"
                    id="file-upload"
                  />
                  <label htmlFor="file-upload" className="cursor-pointer block">
                    <Upload size={24} className="text-gray-400 mx-auto mb-2" />
                    {file ? (
                      <p className="text-pink-600 font-medium">{file.name}</p>
                    ) : (
                      <p className="text-gray-500 text-sm">Click to upload JPG, PNG, MP4 or PDF</p>
                    )}
                  </label>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Description
                </label>
                <textarea
                  value={description}
                  onChange={function(e) { setDescription(e.target.value) }}
                  placeholder="Describe your deliverable..."
                  rows={2}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400 resize-none text-sm"
                />
              </div>

              <button
                type="submit"
                disabled={uploading}
                className="w-full bg-pink-500 hover:bg-pink-600 text-white py-3 rounded-lg font-medium transition disabled:opacity-50"
              >
                {uploading ? 'Uploading...' : 'Submit Deliverable'}
              </button>

            </form>
          </div>
        )}

        <h2 className="font-semibold text-gray-800 mb-4">My Submissions</h2>

        {deliverables.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-xl border border-gray-100">
            <Upload size={48} className="text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No deliverables submitted yet</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {deliverables.map(function(del) {
              return (
                <div key={del.id} className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="font-semibold text-gray-800 mb-2">
                        Campaign number {del.campaign_id}
                      </p>
                      <StatusBadge status={del.status} />
                      {del.description && (
                        <p className="text-gray-500 text-sm mt-2">{del.description}</p>
                      )}
                      <p className="text-xs text-gray-400 mt-2">
                        Submitted: {new Date(del.submitted_at).toLocaleDateString()}
                      </p>
                    </div>

                    <a
                      href={'http://localhost:8000' + del.content_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-sm text-pink-600 hover:underline"
                    >
                      View File
                    </a>
                  </div>
                </div>
              )
            })}
          </div>
        )}

      </div>
    </InfluencerLayout>
  )
}

export default MyDeliverables