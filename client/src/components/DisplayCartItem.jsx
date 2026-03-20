import React from 'react'
import { IoClose } from 'react-icons/io5'
import { BsCart4 } from "react-icons/bs"
import { Link, useNavigate } from 'react-router-dom'
import { useGlobalContext } from '../provider/GlobalProvider'
import { DisplayPriceInRupees } from '../utils/DisplayPriceInRupees'
import { FaCaretRight } from "react-icons/fa";
import { useSelector } from 'react-redux'
import AddToCartButton from './AddToCartButton'
import { pricewithDiscount } from '../utils/PriceWithDiscount'
import imageEmpty from '../assets/empty_cart.webp'
import toast from 'react-hot-toast'

const DisplayCartItem = ({ close }) => {
    const { notDiscountTotalPrice, totalPrice, totalQty } = useGlobalContext()
    const cartItem = useSelector(state => state.cartItem.cart)
    const user = useSelector(state => state.user)
    const navigate = useNavigate()

    const redirectToCheckoutPage = () => {
        if (user?._id) {
            navigate("/checkout", { state: { step: 2 } })
            if (close) close()
            return
        }
        toast("Please Login")
    }

    return (
        <section className='bg-slate-900/40 backdrop-blur-md fixed top-0 bottom-0 right-0 left-0 z-50 transition-all'>
            <div className='bg-white w-full max-w-md min-h-screen max-h-screen ml-auto shadow-[np-20px_0_40px_rgba(0,0,0,0.1)] flex flex-col'>
                {/* Header */}
                <div className='flex items-center p-5 border-b border-slate-100 justify-between bg-white/80 backdrop-blur-xl sticky top-0 z-10'>
                    <h2 className='font-extrabold text-xl text-slate-900 tracking-tight'>Your Cart</h2>
                    <Link to={"/"} className='lg:hidden'>
                        <IoClose size={26} className='text-slate-400 hover:text-slate-700 transition-colors' />
                    </Link>
                    <button onClick={close} className='hidden lg:flex items-center justify-center w-8 h-8 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-500 transition-colors'>
                        <IoClose size={20} />
                    </button>
                </div>

                <div className='flex-1 bg-slate-50/50 p-4 flex flex-col gap-4 overflow-y-auto'>
                    {cartItem[0] ? (
                        <>
                            {/* Savings banner */}
                            <div className='flex items-center justify-between px-5 py-3.5 bg-emerald-50 text-emerald-700 rounded-2xl border border-emerald-100/50 shadow-sm text-sm font-semibold'>
                                <p>Total savings on this order</p>
                                <p className='font-bold bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-md'>{DisplayPriceInRupees(notDiscountTotalPrice - totalPrice)}</p>
                            </div>

                            {/* Cart items */}
                            <div className='bg-white rounded-xl p-3 grid gap-4'>
                                {cartItem.map((item) => (
                                    <div key={item?._id + "cartdisp"} className='flex w-full gap-4 items-center group'>
                                        <div className='w-16 h-16 min-w-16 bg-slate-50 border border-slate-100 rounded-xl overflow-hidden flex items-center justify-center p-1 transition-transform group-hover:scale-105'>
                                            <img
                                                src={item?.productId?.image[0]}
                                                className='w-full h-full object-scale-down'
                                                onError={(e) => { e.target.src = `/api/placeholder/${encodeURIComponent(item?.productId?.name || 'Item')}` }}
                                            />
                                        </div>
                                        <div className='flex-1 text-xs'>
                                            <p className='text-sm text-slate-700 line-clamp-2 font-medium'>{item?.productId?.name}</p>
                                            <p className='text-slate-400 mt-0.5'>{item?.productId?.unit}</p>
                                            <p className='font-bold text-slate-800 mt-0.5'>{DisplayPriceInRupees(pricewithDiscount(item?.productId?.price, item?.productId?.discount))}</p>
                                        </div>
                                        <div>
                                            <AddToCartButton data={item?.productId} />
                                        </div>
                                    </div>
                                ))}
                            </div>

                            {/* Bill */}
                            <div className='bg-white rounded-xl p-4 text-sm'>
                                <h3 className='font-bold text-slate-800 mb-2'>Bill Details</h3>
                                <div className='flex justify-between text-slate-500'>
                                    <p>Items total</p>
                                    <p className='flex items-center gap-2'>
                                        <span className='line-through text-slate-300'>{DisplayPriceInRupees(notDiscountTotalPrice)}</span>
                                        <span className='text-slate-700 font-medium'>{DisplayPriceInRupees(totalPrice)}</span>
                                    </p>
                                </div>
                                <div className='flex justify-between text-slate-500 mt-1'>
                                    <p>Quantity</p>
                                    <p>{totalQty} items</p>
                                </div>
                                <div className='flex justify-between text-slate-500 mt-1'>
                                    <p>Delivery</p>
                                    <p className='text-emerald-600 font-medium'>Free</p>
                                </div>
                            <div className='border-t border-slate-100 mt-3 pt-3 font-extrabold flex justify-between text-slate-900 text-base'>
                                    <p>Grand Total</p>
                                    <p>{DisplayPriceInRupees(totalPrice)}</p>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className='bg-white rounded-2xl border border-slate-100 flex flex-col justify-center items-center p-10 h-full text-center'>
                            <div className='w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mb-6'>
                                <BsCart4 size={40} className='text-slate-300' />
                            </div>
                            <h3 className='font-bold text-lg text-slate-800 mb-2'>Your cart is empty</h3>
                            <p className='text-slate-500 text-sm mb-6 max-w-[200px]'>Add items to your cart to see them here.</p>
                            <Link onClick={close} to={"/"} className='btn-premium bg-emerald-600 hover:bg-emerald-500 px-8 py-3.5 text-white rounded-xl font-bold transition-all shadow-lg shadow-emerald-500/20'>
                                Browse Products
                            </Link>
                        </div>
                    )}
                </div>

                {cartItem[0] && (
                    <div className='p-4 bg-white border-t border-slate-100'>
                        <button onClick={redirectToCheckoutPage} className='btn-premium w-full bg-emerald-600 hover:bg-emerald-500 text-white px-5 font-bold text-base py-4 rounded-xl flex items-center justify-between transition-all shadow-lg shadow-emerald-600/20'>
                            <div className='flex flex-col items-start'>
                                <span className='text-xs font-semibold text-emerald-100'>Total Payment</span>
                                <span className='text-lg'>{DisplayPriceInRupees(totalPrice)}</span>
                            </div>
                            <span className='flex items-center gap-2 bg-white/20 px-4 py-2 rounded-lg backdrop-blur-sm'>
                                Checkout <FaCaretRight />
                            </span>
                        </button>
                    </div>
                )}
            </div>
        </section>
    )
}

export default DisplayCartItem
