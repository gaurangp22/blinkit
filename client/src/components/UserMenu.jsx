import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { Link, useNavigate } from 'react-router-dom'
import Divider from './Divider'
import Axios from '../utils/Axios'
import SummaryApi from '../common/SummaryApi'
import { logout } from '../store/userSlice'
import toast from 'react-hot-toast'
import AxiosToastError from '../utils/AxiosToastError'
import { HiOutlineExternalLink } from "react-icons/hi";
import isAdmin from '../utils/isAdmin'

const UserMenu = ({ close }) => {
    const user = useSelector((state) => state.user)
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const handleLogout = async () => {
        try {
            const response = await Axios({ ...SummaryApi.logout })
            if (response.data.success) {
                if (close) close()
                dispatch(logout())
                localStorage.clear()
                toast.success(response.data.message)
                navigate("/")
            }
        } catch (error) {
            AxiosToastError(error)
        }
    }

    const handleClose = () => { if (close) close() }

    return (
        <div>
            <div className='font-bold text-slate-800'>My Account</div>
            <div className='text-sm flex items-center gap-2 mt-1'>
                <span className='max-w-52 text-ellipsis line-clamp-1 text-slate-600'>
                    {user.name || user.mobile}
                    {user.role === "ADMIN" && <span className='text-indigo-600 font-medium ml-1'>(Admin)</span>}
                </span>
                <Link onClick={handleClose} to={"/dashboard/profile"} className='hover:text-indigo-600 transition-colors'>
                    <HiOutlineExternalLink size={15} />
                </Link>
            </div>

            <Divider />

            <div className='text-sm grid gap-0.5'>
                {isAdmin(user.role) && (
                    <>
                        <Link onClick={handleClose} to={"/dashboard/category"} className='px-3 py-1.5 hover:bg-indigo-50 hover:text-indigo-700 rounded-lg transition-colors'>Category</Link>
                        <Link onClick={handleClose} to={"/dashboard/subcategory"} className='px-3 py-1.5 hover:bg-indigo-50 hover:text-indigo-700 rounded-lg transition-colors'>Sub Category</Link>
                        <Link onClick={handleClose} to={"/dashboard/upload-product"} className='px-3 py-1.5 hover:bg-indigo-50 hover:text-indigo-700 rounded-lg transition-colors'>Upload Product</Link>
                        <Link onClick={handleClose} to={"/dashboard/product"} className='px-3 py-1.5 hover:bg-indigo-50 hover:text-indigo-700 rounded-lg transition-colors'>Products</Link>
                    </>
                )}
                <Link onClick={handleClose} to={"/dashboard/myorders"} className='px-3 py-1.5 hover:bg-indigo-50 hover:text-indigo-700 rounded-lg transition-colors'>My Orders</Link>
                <Link onClick={handleClose} to={"/dashboard/address"} className='px-3 py-1.5 hover:bg-indigo-50 hover:text-indigo-700 rounded-lg transition-colors'>Save Address</Link>
                <button onClick={handleLogout} className='text-left px-3 py-1.5 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors'>Log Out</button>
            </div>
        </div>
    )
}

export default UserMenu
