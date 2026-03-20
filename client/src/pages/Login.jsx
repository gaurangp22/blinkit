import React, { useState } from 'react'
import { FaRegEyeSlash, FaRegEye } from "react-icons/fa6";
import { BsCart4 } from "react-icons/bs";
import toast from 'react-hot-toast';
import Axios from '../utils/Axios';
import SummaryApi from '../common/SummaryApi';
import AxiosToastError from '../utils/AxiosToastError';
import { Link, useNavigate } from 'react-router-dom';
import fetchUserDetails from '../utils/fetchUserDetails';
import { useDispatch } from 'react-redux';
import { setUserDetails } from '../store/userSlice';

const Login = () => {
    const [data, setData] = useState({ email: "", password: "" })
    const [showPassword, setShowPassword] = useState(false)
    const [errors, setErrors] = useState({})
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()
    const dispatch = useDispatch()

    const handleChange = (e) => {
        const { name, value } = e.target
        setData(prev => ({ ...prev, [name]: value }))
        if (errors[name]) setErrors(prev => ({ ...prev, [name]: "" }))
    }

    const validate = () => {
        const err = {}
        if (!data.email.trim()) err.email = "Email is required"
        else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) err.email = "Enter a valid email"
        if (!data.password) err.password = "Password is required"
        setErrors(err)
        return Object.keys(err).length === 0
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        if (!validate()) return
        try {
            setLoading(true)
            const response = await Axios({ ...SummaryApi.login, data: data })
            if (response.data.error) toast.error(response.data.message)
            if (response.data.success) {
                toast.success(response.data.message)
                localStorage.setItem('accesstoken', response.data.data.accesstoken)
                localStorage.setItem('refreshToken', response.data.data.refreshToken)
                const userDetails = await fetchUserDetails()
                dispatch(setUserDetails(userDetails.data))
                setData({ email: "", password: "" })
                navigate("/")
            }
        } catch (error) {
            AxiosToastError(error)
        } finally {
            setLoading(false)
        }
    }

    return (
        <section className='min-h-[80vh] flex items-center justify-center bg-slate-50 relative overflow-hidden px-4'>
            {/* Soft decorative background blurs */}
            <div className='absolute top-1/4 left-1/4 w-96 h-96 bg-emerald-400 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 pointer-events-none'></div>
            <div className='absolute bottom-1/4 right-1/4 w-96 h-96 bg-teal-300 rounded-full mix-blend-multiply filter blur-[128px] opacity-20 pointer-events-none'></div>

            <div className='bg-white/90 backdrop-blur-xl w-full max-w-md rounded-[2rem] shadow-premium border border-white p-8 relative z-10'>
                <div className='text-center mb-10'>
                    <div className='flex justify-center mb-4'>
                        <div className='w-14 h-14 rounded-2xl bg-slate-900 flex items-center justify-center shadow-lg transform -rotate-3 hover:rotate-0 transition-transform'>
                            <BsCart4 size={28} className='text-emerald-400' />
                        </div>
                    </div>
                    <h1 className='text-2xl lg:text-3xl font-extrabold text-slate-900 tracking-tight'>Welcome back</h1>
                    <p className='text-slate-500 font-medium text-sm mt-2'>Enter your credentials to access your account.</p>
                </div>

                <form className='grid gap-6' onSubmit={handleSubmit}>
                    <div className='grid gap-2'>
                        <label htmlFor='email' className='text-sm font-semibold text-slate-700 ml-1'>Email Address</label>
                        <input
                            type='email' id='email' name='email'
                            className={`w-full px-5 py-3.5 bg-slate-50 border rounded-xl outline-none transition-all text-sm font-medium ${errors.email ? 'border-red-400 ring-2 ring-red-100 bg-red-50/50' : 'border-slate-200 focus:border-emerald-500 focus:ring-4 focus:ring-emerald-500/10 focus:bg-white'}`}
                            value={data.email} onChange={handleChange}
                            placeholder='name@company.com'
                        />
                        {errors.email && <p className='text-xs font-semibold text-red-500 ml-1'>{errors.email}</p>}
                    </div>
                    
                    <div className='grid gap-2'>
                        <div className='flex items-center justify-between ml-1'>
                            <label htmlFor='password' className='text-sm font-semibold text-slate-700'>Password</label>
                            <Link to="/forgot-password" className='text-xs font-semibold text-emerald-600 hover:text-emerald-700'>Forgot password?</Link>
                        </div>
                        <div className={`bg-slate-50 border rounded-xl flex items-center transition-all ${errors.password ? 'border-red-400 ring-2 ring-red-100 bg-red-50/50' : 'border-slate-200 focus-within:border-emerald-500 focus-within:ring-4 focus-within:ring-emerald-500/10 focus-within:bg-white'}`}>
                            <input
                                type={showPassword ? "text" : "password"}
                                id='password' name='password'
                                className='w-full px-5 py-3.5 bg-transparent outline-none rounded-xl text-sm font-medium'
                                value={data.password} onChange={handleChange}
                                placeholder='••••••••'
                            />
                            <button type='button' onClick={() => setShowPassword(prev => !prev)} className='px-4 text-slate-400 hover:text-slate-600 transition-colors'>
                                {showPassword ? <FaRegEye size={18} /> : <FaRegEyeSlash size={18} />}
                            </button>
                        </div>
                        {errors.password && <p className='text-xs font-semibold text-red-500 ml-1'>{errors.password}</p>}
                    </div>

                    <button
                        disabled={loading}
                        className='btn-premium w-full mt-2 py-4 rounded-xl font-bold text-base transition-all bg-emerald-600 text-white shadow-lg shadow-emerald-600/20 hover:bg-emerald-500 hover:shadow-xl hover:-translate-y-0.5 active:translate-y-0 disabled:opacity-70 disabled:pointer-events-none'
                    >
                        {loading ? 'Authenticating...' : 'Sign In'}
                    </button>
                </form>

                <p className='text-center mt-8 text-sm font-medium text-slate-500'>
                    Don't have an account?{' '}
                    <Link to="/register" className='font-bold text-slate-900 hover:text-emerald-600 transition-colors'>Create one now</Link>
                </p>
            </div>
        </section>
    )
}

export default Login
