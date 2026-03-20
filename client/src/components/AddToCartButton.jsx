import React, { useEffect, useState } from 'react'
import { useGlobalContext } from '../provider/GlobalProvider'
import Axios from '../utils/Axios'
import SummaryApi from '../common/SummaryApi'
import toast from 'react-hot-toast'
import AxiosToastError from '../utils/AxiosToastError'
import Loading from './Loading'
import { useSelector } from 'react-redux'
import { FaMinus, FaPlus } from "react-icons/fa6";

const AddToCartButton = ({ data }) => {
    const { fetchCartItem, updateCartItem, deleteCartItem } = useGlobalContext()
    const [loading, setLoading] = useState(false)
    const cartItem = useSelector(state => state.cartItem.cart)
    const [isAvailableCart, setIsAvailableCart] = useState(false)
    const [qty, setQty] = useState(0)
    const [cartItemDetails, setCartItemsDetails] = useState()

    const handleADDTocart = async (e) => {
        e.preventDefault()
        e.stopPropagation()
        try {
            setLoading(true)
            const response = await Axios({ ...SummaryApi.addTocart, data: { productId: data?._id } })
            const { data: responseData } = response
            if (responseData.success) {
                toast.success(responseData.message)
                if (fetchCartItem) fetchCartItem()
            }
        } catch (error) {
            AxiosToastError(error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        const checkingitem = cartItem.some(item => item.productId._id === data._id)
        setIsAvailableCart(checkingitem)
        const product = cartItem.find(item => item.productId._id === data._id)
        setQty(product?.quantity)
        setCartItemsDetails(product)
    }, [data, cartItem])

    const increaseQty = async (e) => {
        e.preventDefault()
        e.stopPropagation()
        const response = await updateCartItem(cartItemDetails?._id, qty + 1)
        if (response.success) toast.success("Item added")
    }

    const decreaseQty = async (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (qty === 1) {
            deleteCartItem(cartItemDetails?._id)
        } else {
            const response = await updateCartItem(cartItemDetails?._id, qty - 1)
            if (response.success) toast.success("Item removed")
        }
    }

    return (
        <div className='w-full max-w-[150px]'>
            {isAvailableCart ? (
                <div className='flex w-full h-10 items-center bg-emerald-50 rounded-full border-2 border-emerald-100 overflow-hidden shadow-sm'>
                    <button onClick={decreaseQty} className='hover:bg-emerald-500 hover:text-white text-emerald-600 w-10 h-full flex items-center justify-center transition-all bg-emerald-100/30'>
                        <FaMinus size={12} />
                    </button>
                    <p className='flex-1 w-full h-full font-extrabold text-sm flex items-center justify-center text-emerald-900 bg-white'>{qty}</p>
                    <button onClick={increaseQty} className='hover:bg-emerald-500 hover:text-white text-emerald-600 w-10 h-full flex items-center justify-center transition-all bg-emerald-100/30'>
                        <FaPlus size={12} />
                    </button>
                </div>
            ) : (
                <button onClick={handleADDTocart} className='w-full bg-emerald-50 hover:bg-emerald-600 text-emerald-700 hover:text-white border-2 border-emerald-100 hover:border-emerald-600 px-4 py-1.5 rounded-full text-sm font-bold transition-all duration-300 shadow-sm'>
                    {loading ? <Loading /> : "Add"}
                </button>
            )}
        </div>
    )
}

export default AddToCartButton
