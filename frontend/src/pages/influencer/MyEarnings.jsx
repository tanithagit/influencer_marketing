import { useState, useEffect } from 'react'
import InfluencerLayout from '../../components/influencer/InfluencerLayout'
import { paymentAPI } from '../../services/api'
import Spinner from '../../components/common/Spinner'
import { DollarSign } from 'lucide-react'

function StatusBadge({ status }) {
  const styles = {
    pending:  'bg-yellow-100 text-yellow-700',
    escrowed: 'bg-blue-100 text-blue-700',
    released: 'bg-green-100 text-green-700',
    failed:   'bg-red-100 text-red-700',
  }
  return (
    <span className={`text-xs font-medium px-3 py-1 rounded-full capitalize ${styles[status] || 'bg-gray-100 text-gray-700'}`}>
      {status}
    </span>
  )
}

function MyEarnings() {
  const [payments, setPayments] = useState([])
  const [loading,  setLoading]  = useState(true)

  useEffect(() => {
    const fetch = async () => {
      try {
        const res = await paymentAPI.getMine()
        setPayments(res.data)
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetch()
  }, [])

  const totalReleased = payments
    .filter((p) => p.payment_status === 'released')
    .reduce((sum, p) => sum + p.amount, 0)

  const totalPending = payments
    .filter((p) => p.payment_status === 'escrowed')
    .reduce((sum, p) => sum + p.amount, 0)

  return (
    <InfluencerLayout>
      <div className="p-8">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-800">My Earnings</h1>
          <p className="text-gray-500 mt-1">Track all your payments</p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-green-50 rounded-xl p-6 border border-green-100">
            <p className="text-sm text-green-600 font-medium mb-2">
              Total Released
            </p>
            <p className="text-3xl font-bold text-green-700">
              ${totalReleased.toFixed(2)}
            </p>
          </div>
          <div className="bg-yellow-50 rounded-xl p-6 border border-yellow-100">
            <p className="text-sm text-yellow-600 font-medium mb-2">
              In Escrow
            </p>
            <p className="text-3xl font-bold text-yellow-700">
              ${totalPending.toFixed(2)}
            </p>
          </div>
          <div className="bg-blue-50 rounded-xl p-6 border border-blue-100">
            <p className="text-sm text-blue-600 font-medium mb-2">
              Total Payments
            </p>
            <p className="text-3xl font-bold text-blue-700">
              {payments.length}
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
            <p className="text-gray-500">No payments yet</p>
          </div>
        ) : (
          <div className="grid gap-4">
            {payments.map((payment) => (
              <div
                key={payment.id}
                className="bg-white rounded-xl p-6 border border-gray-100 shadow-sm"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-semibold text-gray-800">
                      Campaign #{payment.campaign_id}
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(payment.created_at).toLocaleDateString()}
                    </p>
                    {payment.released_at && (
                      <p className="text-xs text-green-500 mt-1">
                        Released: {new Date(payment.released_at).toLocaleDateString()}
                      </p>
                    )}
                  </div>
                  <div className="text-right">
                    <p className="text-2xl font-bold text-gray-800">
                      ${payment.amount.toFixed(2)}
                    </p>
                    <StatusBadge status={payment.payment_status} />
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

export default MyEarnings