import React from 'react'
import { useSelector } from 'react-redux'
import NoData from '../components/NoData'
import { DisplayPriceInRupees } from '../utils/DisplayPriceInRupees'

const MyOrders = () => {
  const orders = useSelector(state => state.orders.order)

  return (
    <div className='p-4'>
      <div className='bg-white rounded-xl shadow-sm border border-slate-100 p-4 mb-4'>
        <h1 className='font-bold text-lg text-slate-800'>My Orders</h1>
        <p className='text-sm text-slate-500'>{orders.length} orders placed</p>
      </div>

      {!orders[0] && <NoData />}

      <div className='grid gap-3'>
        {orders.map((order, index) => (
          <div key={order._id + index + "order"} className='bg-white rounded-xl border border-slate-100 shadow-sm p-4'>
            <div className='flex items-center justify-between mb-3'>
              <div>
                <p className='text-xs text-slate-400 font-medium'>Order #{order?.orderId}</p>
                <p className='text-xs text-slate-400 mt-0.5'>
                  {order?.createdAt ? new Date(order.createdAt).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' }) : ''}
                </p>
              </div>
              <span className='text-xs font-semibold px-3 py-1 rounded-full bg-emerald-50 text-emerald-700'>
                {order?.payment_status || 'Placed'}
              </span>
            </div>
            <div className='flex gap-3 items-center'>
              <div className='w-14 h-14 min-w-14 bg-slate-50 rounded-lg overflow-hidden flex items-center justify-center border border-slate-100'>
                <img
                  src={order.product_details?.image?.[0]}
                  className='w-full h-full object-scale-down'
                  onError={(e) => { e.target.src = `/api/placeholder/${encodeURIComponent(order.product_details?.name || 'Product')}` }}
                />
              </div>
              <div className='flex-1'>
                <p className='font-medium text-slate-800 text-sm line-clamp-1'>{order.product_details?.name}</p>
                <p className='text-sm font-bold text-indigo-600 mt-0.5'>{DisplayPriceInRupees(order.totalAmt)}</p>
              </div>
            </div>
            {order.delivery_address && order.delivery_address.name && (
              <div className='mt-3 pt-3 border-t border-slate-50 text-xs text-slate-500'>
                <p className='font-medium text-slate-600'>Deliver to: {order.delivery_address.name}</p>
                <p>{order.delivery_address.address_line}, {order.delivery_address.city}, {order.delivery_address.state} - {order.delivery_address.pincode}</p>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default MyOrders
