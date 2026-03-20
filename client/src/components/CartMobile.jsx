import React from 'react'
import { useGlobalContext } from '../provider/GlobalProvider'
import { FaCartShopping } from 'react-icons/fa6'
import { DisplayPriceInRupees } from '../utils/DisplayPriceInRupees'
import { Link } from 'react-router-dom'
import { FaCaretRight } from "react-icons/fa";
import { useSelector } from 'react-redux'

const CartMobileLink = () => {
    const { totalPrice, totalQty } = useGlobalContext()
    const cartItem = useSelector(state => state.cartItem.cart)

    return (
        <>
            {cartItem[0] && (
                <div className='sticky bottom-4 p-2 lg:hidden'>
                    <div className='bg-gradient-to-r from-indigo-600 to-purple-600 px-4 py-3 rounded-2xl text-white flex items-center justify-between gap-3 shadow-xl shadow-indigo-300/30'>
                        <div className='flex items-center gap-3'>
                            <div className='p-2 bg-white/20 rounded-xl'>
                                <FaCartShopping size={16} />
                            </div>
                            <div className='text-sm'>
                                <p className='font-bold'>{totalQty} items</p>
                                <p className='text-white/80 text-xs'>{DisplayPriceInRupees(totalPrice)}</p>
                            </div>
                        </div>
                        <Link to={"/cart"} className='flex items-center gap-1 bg-white/20 px-4 py-1.5 rounded-xl text-sm font-medium hover:bg-white/30 transition-colors'>
                            <span>View Cart</span>
                            <FaCaretRight />
                        </Link>
                    </div>
                </div>
            )}
        </>
    )
}

export default CartMobileLink
