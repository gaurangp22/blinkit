import React, { useState, useEffect } from 'react'
import { useSelector, useDispatch } from 'react-redux'
import NoData from '../components/NoData'
import { DisplayPriceInRupees } from '../utils/DisplayPriceInRupees'
import Axios from '../utils/Axios'
import SummaryApi from '../common/SummaryApi'
import toast from 'react-hot-toast'
import { setOrder } from '../store/orderSlice'
import { IoClose, IoSearchOutline } from 'react-icons/io5'
import { BsBoxSeam, BsTruck, BsCheckCircleFill, BsXCircleFill, BsArrowRepeat, BsReceipt, BsGeoAlt, BsClockHistory, BsFilter } from 'react-icons/bs'
import { FiPackage, FiShoppingCart } from 'react-icons/fi'

const ORDER_STATUSES = ['All', 'Confirmed', 'Processing', 'Packed', 'Shipped', 'Out for Delivery', 'Delivered', 'Cancelled']

const statusConfig = {
  'Confirmed': { color: 'bg-blue-50 text-blue-700 border-blue-200', icon: <BsCheckCircleFill className="text-blue-500" /> },
  'Processing': { color: 'bg-amber-50 text-amber-700 border-amber-200', icon: <BsClockHistory className="text-amber-500" /> },
  'Packed': { color: 'bg-purple-50 text-purple-700 border-purple-200', icon: <FiPackage className="text-purple-500" /> },
  'Shipped': { color: 'bg-indigo-50 text-indigo-700 border-indigo-200', icon: <BsTruck className="text-indigo-500" /> },
  'Out for Delivery': { color: 'bg-orange-50 text-orange-700 border-orange-200', icon: <BsTruck className="text-orange-500" /> },
  'Delivered': { color: 'bg-emerald-50 text-emerald-700 border-emerald-200', icon: <BsCheckCircleFill className="text-emerald-500" /> },
  'Cancelled': { color: 'bg-red-50 text-red-700 border-red-200', icon: <BsXCircleFill className="text-red-500" /> },
  'CASH ON DELIVERY': { color: 'bg-emerald-50 text-emerald-700 border-emerald-200', icon: <BsCheckCircleFill className="text-emerald-500" /> },
}

const MyOrders = () => {
  const orders = useSelector(state => state.orders.order)
  const dispatch = useDispatch()
  const [activeFilter, setActiveFilter] = useState('All')
  const [searchQuery, setSearchQuery] = useState('')
  const [trackingModal, setTrackingModal] = useState(null)
  const [trackingData, setTrackingData] = useState(null)
  const [trackingLoading, setTrackingLoading] = useState(false)
  const [expandedOrder, setExpandedOrder] = useState(null)

  const filteredOrders = orders.filter(order => {
    const matchesFilter = activeFilter === 'All' || order.order_status === activeFilter
    const matchesSearch = !searchQuery || 
      order.product_details?.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      order.orderId?.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesFilter && matchesSearch
  })

  // Group orders by date
  const groupedOrders = filteredOrders.reduce((groups, order) => {
    const date = order.createdAt ? new Date(order.createdAt).toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' }) : 'Unknown Date'
    if (!groups[date]) groups[date] = []
    groups[date].push(order)
    return groups
  }, {})

  const refreshOrders = async () => {
    try {
      const response = await Axios({ ...SummaryApi.getOrderItems })
      if (response.data.success) {
        dispatch(setOrder(response.data.data))
      }
    } catch (error) {
      console.error("Failed to refresh orders", error)
    }
  }

  const handleCancelOrder = async (orderId) => {
    if (!window.confirm("Are you sure you want to cancel this order?")) return
    try {
      const response = await Axios({ ...SummaryApi.cancelOrder, data: { orderId } })
      if (response.data.success) {
        toast.success("Order cancelled successfully")
        refreshOrders()
      }
    } catch (error) {
      toast.error(error?.response?.data?.message || "Failed to cancel order")
    }
  }

  const handleReorder = async (orderId) => {
    try {
      const response = await Axios({ ...SummaryApi.reorderItem, data: { orderId } })
      if (response.data.success) {
        toast.success("Item added to your cart!")
      }
    } catch (error) {
      toast.error(error?.response?.data?.message || "Failed to reorder")
    }
  }

  const handleTrackOrder = async (orderId) => {
    setTrackingModal(orderId)
    setTrackingLoading(true)
    try {
      const response = await Axios({ ...SummaryApi.trackOrder, data: { orderId } })
      if (response.data.success) {
        setTrackingData(response.data.data)
      }
    } catch (error) {
      toast.error("Failed to load tracking details")
      setTrackingModal(null)
    } finally {
      setTrackingLoading(false)
    }
  }

  const getStatusStats = () => {
    const stats = {}
    orders.forEach(o => {
      const status = o.order_status || 'Processing'
      stats[status] = (stats[status] || 0) + 1
    })
    return stats
  }

  const stats = getStatusStats()

  return (
    <div className='p-4 max-w-5xl mx-auto'>
      {/* Header */}
      <div className='bg-white rounded-2xl shadow-sm border border-slate-100 p-6 mb-6'>
        <div className='flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4'>
          <div>
            <h1 className='text-2xl font-bold text-slate-800 flex items-center gap-3'>
              <BsBoxSeam className='text-indigo-500' />
              My Orders
            </h1>
            <p className='text-sm text-slate-500 mt-1'>{orders.length} total orders</p>
          </div>
          
          {/* Quick Stats */}
          <div className='flex gap-3 flex-wrap'>
            {stats['Confirmed'] && (
              <div className='px-3 py-1.5 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold'>
                {stats['Confirmed']} Confirmed
              </div>
            )}
            {stats['Delivered'] && (
              <div className='px-3 py-1.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-semibold'>
                {stats['Delivered']} Delivered
              </div>
            )}
            {stats['Cancelled'] && (
              <div className='px-3 py-1.5 rounded-full bg-red-50 text-red-700 text-xs font-semibold'>
                {stats['Cancelled']} Cancelled
              </div>
            )}
          </div>
        </div>
        
        {/* Search Bar */}
        <div className='mt-4 relative'>
          <IoSearchOutline className='absolute left-3 top-1/2 -translate-y-1/2 text-slate-400' size={18} />
          <input 
            type="text" 
            placeholder="Search by product name or order ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className='w-full pl-10 pr-4 py-2.5 border border-slate-200 rounded-xl text-sm outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-50 transition-all'
          />
        </div>

        {/* Filter Tabs */}
        <div className='mt-4 flex gap-2 overflow-x-auto pb-1 scrollbar-hide'>
          {ORDER_STATUSES.map(status => (
            <button 
              key={status}
              onClick={() => setActiveFilter(status)}
              className={`px-4 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-all border ${
                activeFilter === status 
                  ? 'bg-indigo-600 text-white border-indigo-600 shadow-sm' 
                  : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
              }`}
            >
              {status}
              {status !== 'All' && stats[status] ? ` (${stats[status]})` : ''}
              {status === 'All' ? ` (${orders.length})` : ''}
            </button>
          ))}
        </div>
      </div>

      {/* No orders */}
      {!filteredOrders.length && (
        <div className='text-center py-16'>
          <FiPackage className='mx-auto text-slate-300 mb-4' size={48} />
          <h3 className='text-lg font-semibold text-slate-600'>
            {searchQuery || activeFilter !== 'All' ? 'No matching orders found' : 'No orders yet'}
          </h3>
          <p className='text-sm text-slate-400 mt-1'>
            {searchQuery ? 'Try a different search term' : 'Start shopping to place your first order!'}
          </p>
        </div>
      )}

      {/* Orders grouped by date */}
      {Object.entries(groupedOrders).map(([date, dateOrders]) => (
        <div key={date} className='mb-6'>
          <h3 className='text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3 px-1'>{date}</h3>
          <div className='grid gap-3'>
            {dateOrders.map((order, index) => {
              const statusInfo = statusConfig[order.order_status] || statusConfig['Processing']
              const isCancellable = ['Confirmed', 'Processing'].includes(order.order_status)
              const isExpanded = expandedOrder === order._id

              return (
                <div key={order._id + index + "order"} className='bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden transition-all hover:shadow-md'>
                  {/* Main Order Row */}
                  <div className='p-4'>
                    <div className='flex items-start gap-4'>
                      {/* Product Image */}
                      <div className='w-16 h-16 min-w-16 bg-slate-50 rounded-xl overflow-hidden flex items-center justify-center border border-slate-100'>
                        <img
                          src={order.product_details?.image?.[0]}
                          className='w-full h-full object-scale-down p-1'
                          alt={order.product_details?.name}
                          onError={(e) => { e.target.src = `/api/placeholder/${encodeURIComponent(order.product_details?.name || 'Product')}` }}
                        />
                      </div>

                      {/* Product Info */}
                      <div className='flex-1 min-w-0'>
                        <div className='flex items-start justify-between gap-2'>
                          <div>
                            <p className='font-semibold text-slate-800 text-sm line-clamp-1'>{order.product_details?.name}</p>
                            <p className='text-xs text-slate-400 mt-0.5'>Order #{order?.orderId}</p>
                          </div>
                          <span className={`shrink-0 inline-flex items-center gap-1.5 text-xs font-semibold px-3 py-1 rounded-full border ${statusInfo.color}`}>
                            {statusInfo.icon}
                            {order.order_status || 'Processing'}
                          </span>
                        </div>

                        <div className='flex items-center gap-4 mt-2'>
                          <p className='text-sm font-bold text-indigo-600'>{DisplayPriceInRupees(order.totalAmt)}</p>
                          {order.quantity > 1 && (
                            <p className='text-xs text-slate-400'>Qty: {order.quantity}</p>
                          )}
                          <p className='text-xs text-slate-400'>
                            {order.payment_status}
                          </p>
                        </div>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className='flex items-center gap-2 mt-3 pt-3 border-t border-slate-50 flex-wrap'>
                      {/* Track Order */}
                      {order.order_status !== 'Cancelled' && (
                        <button 
                          onClick={() => handleTrackOrder(order._id)}
                          className='flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-indigo-50 text-indigo-600 hover:bg-indigo-100 transition-colors'
                        >
                          <BsGeoAlt size={12} />
                          Track Order
                        </button>
                      )}

                      {/* Reorder */}
                      <button 
                        onClick={() => handleReorder(order._id)}
                        className='flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-50 text-emerald-600 hover:bg-emerald-100 transition-colors'
                      >
                        <BsArrowRepeat size={12} />
                        Reorder
                      </button>

                      {/* Cancel Order */}
                      {isCancellable && (
                        <button 
                          onClick={() => handleCancelOrder(order._id)}
                          className='flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-red-50 text-red-600 hover:bg-red-100 transition-colors'
                        >
                          <BsXCircleFill size={12} />
                          Cancel
                        </button>
                      )}

                      {/* Expand Details */}
                      <button 
                        onClick={() => setExpandedOrder(isExpanded ? null : order._id)}
                        className='flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-50 text-slate-600 hover:bg-slate-100 transition-colors ml-auto'
                      >
                        <BsReceipt size={12} />
                        {isExpanded ? 'Hide Details' : 'View Details'}
                      </button>
                    </div>
                  </div>

                  {/* Expanded Details */}
                  {isExpanded && (
                    <div className='bg-slate-50 border-t border-slate-100 p-4 space-y-3 animate-fadeIn'>
                      {/* Invoice */}
                      {order.invoice_number && (
                        <div className='flex items-center justify-between'>
                          <span className='text-xs text-slate-500'>Invoice</span>
                          <span className='text-xs font-medium text-slate-700'>{order.invoice_number}</span>
                        </div>
                      )}
                      <div className='flex items-center justify-between'>
                        <span className='text-xs text-slate-500'>Order Date</span>
                        <span className='text-xs font-medium text-slate-700'>
                          {order.createdAt ? new Date(order.createdAt).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : ''}
                        </span>
                      </div>
                      <div className='flex items-center justify-between'>
                        <span className='text-xs text-slate-500'>Payment Method</span>
                        <span className='text-xs font-medium text-slate-700'>{order.payment_status}</span>
                      </div>
                      {order.product_details?.unit && (
                        <div className='flex items-center justify-between'>
                          <span className='text-xs text-slate-500'>Product Unit</span>
                          <span className='text-xs font-medium text-slate-700'>{order.product_details.unit}</span>
                        </div>
                      )}

                      {/* Delivery Address */}
                      {order.delivery_address && order.delivery_address.name && (
                        <div className='bg-white rounded-xl p-3 border border-slate-100'>
                          <p className='text-xs font-semibold text-slate-600 mb-1 flex items-center gap-1.5'>
                            <BsGeoAlt className='text-indigo-500' />
                            Delivery Address
                          </p>
                          <p className='text-xs text-slate-600 font-medium'>{order.delivery_address.name}</p>
                          <p className='text-xs text-slate-500'>
                            {order.delivery_address.address_line}, {order.delivery_address.city}, {order.delivery_address.state} - {order.delivery_address.pincode}
                          </p>
                          {order.delivery_address.mobile && (
                            <p className='text-xs text-slate-500 mt-0.5'>📞 {order.delivery_address.mobile}</p>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>
      ))}

      {/* Tracking Modal */}
      {trackingModal && (
        <div className='fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4'>
          <div className='bg-white rounded-2xl w-full max-w-md max-h-[85vh] overflow-auto shadow-2xl'>
            {/* Modal Header */}
            <div className='sticky top-0 bg-white border-b border-slate-100 p-4 flex items-center justify-between rounded-t-2xl'>
              <h2 className='font-bold text-lg text-slate-800 flex items-center gap-2'>
                <BsTruck className='text-indigo-500' />
                Order Tracking
              </h2>
              <button 
                onClick={() => { setTrackingModal(null); setTrackingData(null) }}
                className='p-1.5 hover:bg-slate-100 rounded-lg transition-colors'
              >
                <IoClose size={20} />
              </button>
            </div>

            {trackingLoading ? (
              <div className='p-8 text-center'>
                <div className='w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin mx-auto mb-3'></div>
                <p className='text-sm text-slate-500'>Loading tracking details...</p>
              </div>
            ) : trackingData ? (
              <div className='p-4 space-y-5'>
                {/* Order Summary */}
                <div className='bg-indigo-50 rounded-xl p-4'>
                  <p className='text-xs font-medium text-indigo-600'>Order #{trackingData.order?.orderId}</p>
                  <p className='font-semibold text-slate-800 mt-1'>{trackingData.order?.product_details?.name}</p>
                  <p className='text-xs text-slate-500 mt-1'>
                    Estimated Delivery: {new Date(trackingData.estimatedDelivery).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>

                {/* Timeline */}
                <div className='space-y-0'>
                  {trackingData.timeline?.map((step, idx) => (
                    <div key={idx} className='flex gap-3'>
                      {/* Line + Dot */}
                      <div className='flex flex-col items-center'>
                        <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center shrink-0 ${
                          step.cancelled 
                            ? 'bg-red-500 border-red-500' 
                            : step.completed 
                              ? 'bg-indigo-500 border-indigo-500' 
                              : 'bg-white border-slate-300'
                        }`}>
                          {step.completed && <div className='w-1.5 h-1.5 bg-white rounded-full'></div>}
                        </div>
                        {idx < trackingData.timeline.length - 1 && (
                          <div className={`w-0.5 h-10 ${step.completed ? 'bg-indigo-300' : 'bg-slate-200'}`}></div>
                        )}
                      </div>

                      {/* Content */}
                      <div className='pb-6'>
                        <p className={`text-sm font-semibold ${step.cancelled ? 'text-red-600' : step.completed ? 'text-slate-800' : 'text-slate-400'}`}>
                          {step.status}
                        </p>
                        {step.time && (
                          <p className='text-xs text-slate-400 mt-0.5'>
                            {new Date(step.time).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Delivery Address in Tracking */}
                {trackingData.order?.delivery_address?.name && (
                  <div className='bg-slate-50 rounded-xl p-3 border border-slate-100'>
                    <p className='text-xs font-semibold text-slate-600 mb-1'>📍 Delivering to</p>
                    <p className='text-xs text-slate-700 font-medium'>{trackingData.order.delivery_address.name}</p>
                    <p className='text-xs text-slate-500'>
                      {trackingData.order.delivery_address.address_line}, {trackingData.order.delivery_address.city}
                    </p>
                  </div>
                )}
              </div>
            ) : null}
          </div>
        </div>
      )}
    </div>
  )
}

export default MyOrders
