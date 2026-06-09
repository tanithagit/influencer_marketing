import { useState, useEffect } from 'react'
import AdminLayout from '../../components/admin/AdminLayout'
import api from '../../services/api'
import Spinner from '../../components/common/Spinner'
import { DollarSign } from 'lucide-react'

function AdminPayments() {
  const [payments, setPayments] = useState([])
  const [loading,  setLoading]  = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await api.get('/api/payments/campaign/1')
        setPayments(res.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  const statusStyles = {
    pending:  'bg-yellow-100 text-yellow-700',
    escrowed: 'bg-blue-100 text-blue-700',
    released: 'bg-green-100 text-green-700',
    failed:   'bg-red-100 text-red-700',
  }

  const totalAmount = payments.reduce((sum, p) => sum + p.amount, 0)

  return (
    <AdminLayout>
      <div className="p-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">Payment Monitor</h1>
          <p className="text-gray-500 mt-1">Monitor all platform transactions</p>
        </div>

        {/* Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500 mb-2">Total Transactions</p>
            <p className="text-3xl font-bold text-gray-800">{payments.length}</p>
          </div>
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500 mb-2">Total Amount</p>
            <p className="text-3xl font-bold text-green-600">
              ${totalAmount.toFixed(2)}
            </p>
          </div>
          <div className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
            <p className="text-sm text-gray-500 mb-2">Released Payments</p>
            <p className="text-3xl font-bold text-blue-600">
              {payments.filter((p) => p.payment_status === 'released').length}
            </p>
          </div>
        </div>

        {/* Payments List */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Spinner size="lg" />
          </div>
        ) : payments.length === 0 ? (
          <div className="text-center py-20 bg-white rounded-xl border border-gray-100">
            <DollarSign size={48} className="text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500">No payments found</p>
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-100">
                <tr>
                  <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                    Payment ID
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                    Campaign
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                    Influencer
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                    Amount
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                    Status
                  </th>
                  <th className="text-left px-6 py-4 text-sm font-medium text-gray-600">
                    Date
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {payments.map((payment) => (
                  <tr key={payment.id} className="hover:bg-gray-50 transition">
                    <td className="px-6 py-4 text-sm text-gray-500">
                      #{payment.id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-800">
                      Campaign #{payment.campaign_id}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-800">
                      User #{payment.influencer_id}
                    </td>
                    <td className="px-6 py-4 text-sm font-semibold text-gray-800">
                      ${payment.amount.toFixed(2)}
                    </td>
                    <td className="px-6 py-4">
                      <span className={`text-xs font-medium px-2 py-1 rounded-full capitalize ${statusStyles[payment.payment_status] || 'bg-gray-100 text-gray-700'}`}>
                        {payment.payment_status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-500">
                      {new Date(payment.created_at).toLocaleDateString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </AdminLayout>
  )
}

export default AdminPayments