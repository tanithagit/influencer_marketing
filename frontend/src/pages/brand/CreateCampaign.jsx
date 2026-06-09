import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import BrandLayout from '../../components/brand/BrandLayout'
import { campaignAPI } from '../../services/api'
import toast from 'react-hot-toast'
import Spinner from '../../components/common/Spinner'

function CreateCampaign() {
  const [formData, setFormData] = useState({
    title:        '',
    description:  '',
    requirements: '',
    budget:       '',
    niche:        '',
    start_date:   '',
    end_date:     ''
  })
  const [loading,  setLoading]  = useState(false)
  const navigate                = useNavigate()

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const payload = {
        ...formData,
        budget:     parseFloat(formData.budget),
        start_date: new Date(formData.start_date).toISOString(),
        end_date:   new Date(formData.end_date).toISOString(),
      }
      await campaignAPI.create(payload)
      toast.success('Campaign created successfully!')
      navigate('/brand/campaigns')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to create campaign')
    } finally {
      setLoading(false)
    }
  }

  const niches = [
    'Technology', 'Fashion', 'Food', 'Travel',
    'Fitness', 'Beauty', 'Gaming', 'Education',
    'Finance', 'Lifestyle'
  ]

  return (
    <BrandLayout>
      <div className="p-8 max-w-2xl">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">Create Campaign</h1>
          <p className="text-gray-500 mt-1">Fill in the details for your new campaign</p>
        </div>

        <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
          <form onSubmit={handleSubmit} className="space-y-5">

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Campaign Title *
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="e.g. Summer Product Launch"
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Describe your campaign..."
                rows={3}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition resize-none"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Requirements
              </label>
              <textarea
                name="requirements"
                value={formData.requirements}
                onChange={handleChange}
                placeholder="e.g. Minimum 10k followers, tech niche..."
                rows={3}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition resize-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Budget ($) *
                </label>
                <input
                  type="number"
                  name="budget"
                  value={formData.budget}
                  onChange={handleChange}
                  placeholder="5000"
                  required
                  min="1"
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Niche
                </label>
                <select
                  name="niche"
                  value={formData.niche}
                  onChange={handleChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                >
                  <option value="">Select niche</option>
                  {niches.map(n => (
                    <option key={n} value={n}>{n}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Start Date *
                </label>
                <input
                  type="date"
                  name="start_date"
                  value={formData.start_date}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  End Date *
                </label>
                <input
                  type="date"
                  name="end_date"
                  value={formData.end_date}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 transition"
                />
              </div>
            </div>

            <div className="flex gap-3 pt-2">
              <button
                type="button"
                onClick={() => navigate('/brand/campaigns')}
                className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition font-medium"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 rounded-lg transition disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {loading ? <Spinner size="sm" /> : 'Create Campaign'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </BrandLayout>
  )
}

export default CreateCampaign