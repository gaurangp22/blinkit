import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { BsCart4 } from "react-icons/bs"

const Success = () => {
  const location = useLocation()
  const isOrder = location?.state?.text === "Order"

  return (
    <div className='min-h-[70vh] flex items-center justify-center bg-slate-50 px-4'>
      <div className='bg-white w-full max-w-md rounded-2xl shadow-xl border border-slate-100 p-8 text-center'>
        {/* Animated checkmark */}
        <div className='w-20 h-20 mx-auto rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center mb-6 shadow-lg shadow-emerald-200'>
          <svg className='w-10 h-10 text-white' fill='none' viewBox='0 0 24 24' stroke='currentColor' strokeWidth={3}>
            <path strokeLinecap='round' strokeLinejoin='round' d='M5 13l4 4L19 7' />
          </svg>
        </div>

        <h1 className='text-2xl font-bold text-slate-800 mb-2'>
          {isOrder ? 'Order Placed!' : 'Payment Successful!'}
        </h1>
        <p className='text-slate-500 mb-1'>
          {isOrder
            ? 'Your order has been placed successfully. You will receive it soon!'
            : 'Your payment was processed successfully.'
          }
        </p>
        <p className='text-sm text-slate-400 mb-8'>Thank you for shopping with Cartify</p>

        <div className='grid gap-3'>
          <Link to="/dashboard/myorders"
            className='w-full py-3 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl hover:from-indigo-700 hover:to-purple-700 transition-all shadow-lg shadow-indigo-200 block'>
            View My Orders
          </Link>
          <Link to="/"
            className='w-full py-3 border-2 border-slate-200 text-slate-600 font-semibold rounded-xl hover:bg-slate-50 transition-colors flex items-center justify-center gap-2 block'>
            <BsCart4 size={18} />
            Continue Shopping
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Success
