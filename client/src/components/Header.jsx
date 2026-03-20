import React, { useState } from 'react'
import Search from './Search'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { FaRegCircleUser } from "react-icons/fa6";
import useMobile from '../hooks/useMobile';
import { BsCart4 } from "react-icons/bs";
import { useSelector } from 'react-redux';
import { GoTriangleDown, GoTriangleUp } from "react-icons/go";
import UserMenu from './UserMenu';
import { DisplayPriceInRupees } from '../utils/DisplayPriceInRupees';
import { useGlobalContext } from '../provider/GlobalProvider';
import DisplayCartItem from './DisplayCartItem';

const Header = () => {
    const [isMobile] = useMobile()
    const location = useLocation()
    const isSearchPage = location.pathname === "/search"
    const navigate = useNavigate()
    const user = useSelector((state) => state?.user)
    const [openUserMenu, setOpenUserMenu] = useState(false)
    const cartItem = useSelector(state => state.cartItem.cart)
    const { totalPrice, totalQty } = useGlobalContext()
    const [openCartSection, setOpenCartSection] = useState(false)

    const redirectToLoginPage = () => navigate("/login")
    const handleCloseUserMenu = () => setOpenUserMenu(false)

    const handleMobileUser = () => {
        if (!user._id) {
            navigate("/login")
            return
        }
        navigate("/user")
    }

    return (
        <header className='h-24 lg:h-20 sticky top-0 z-40 flex flex-col justify-center gap-1 bg-white/80 backdrop-blur-xl border-b border-slate-200/50 shadow-soft transition-all duration-300'>
            {
                !(isSearchPage && isMobile) && (
                    <div className='container mx-auto flex items-center px-4 justify-between h-full'>
                        {/* Logo */}
                        <Link to={"/"} className='flex items-center gap-3 group'>
                            <div className='w-10 h-10 rounded-xl bg-slate-900 group-hover:bg-emerald-600 transition-colors flex items-center justify-center shadow-md'>
                                <BsCart4 size={20} className='text-white' />
                            </div>
                            <span className='text-2xl font-extrabold tracking-tight text-slate-900 hidden sm:block'>
                                Cartify<span className='text-emerald-500'>.</span>
                            </span>
                        </Link>

                        {/* Search */}
                        <div className='hidden lg:block flex-1 max-w-2xl mx-8'>
                            <Search />
                        </div>

                        {/* Right section */}
                        <div className='flex items-center gap-4'>
                            {/* Mobile user icon */}
                            <button className='text-slate-600 hover:text-slate-900 lg:hidden transition-colors bg-slate-100 p-2 rounded-full' onClick={handleMobileUser}>
                                <FaRegCircleUser size={22} />
                            </button>

                            {/* Desktop */}
                            <div className='hidden lg:flex items-center gap-5'>
                                {
                                    user?._id ? (
                                        <div className='relative'>
                                            <div onClick={() => setOpenUserMenu(prev => !prev)} className='flex select-none items-center gap-2 cursor-pointer text-slate-700 hover:text-slate-950 transition-colors px-4 py-2 rounded-xl hover:bg-slate-100/80 font-medium'>
                                                <FaRegCircleUser size={20} />
                                                <p className='text-sm'>Account</p>
                                                {openUserMenu ? <GoTriangleUp size={18} /> : <GoTriangleDown size={18} />}
                                            </div>
                                            {
                                                openUserMenu && (
                                                    <div className='absolute right-0 top-14 z-50'>
                                                        <div className='bg-white rounded-2xl p-3 min-w-[240px] shadow-premium border border-slate-100'>
                                                            <UserMenu close={handleCloseUserMenu} />
                                                        </div>
                                                    </div>
                                                )
                                            }
                                        </div>
                                    ) : (
                                        <button onClick={redirectToLoginPage} className='text-sm font-semibold px-6 py-2.5 rounded-xl border-2 border-slate-200 text-slate-700 hover:border-slate-900 hover:bg-slate-900 hover:text-white transition-all duration-300'>
                                            Sign In
                                        </button>
                                    )
                                }
                                <button onClick={() => setOpenCartSection(true)} className='flex items-center gap-3 bg-emerald-600 hover:bg-emerald-700 px-5 py-2.5 rounded-xl text-white transition-all shadow-md hover:shadow-lg hover:-translate-y-0.5 active:translate-y-0'>
                                    <BsCart4 size={22} className='opacity-90' />
                                    <div className='font-semibold text-sm'>
                                        {
                                            cartItem[0] ? (
                                                <div className='flex items-center gap-2.5'>
                                                    <span className='bg-white/25 px-2.5 py-0.5 rounded-md text-sm'>{totalQty}</span>
                                                    <span>{DisplayPriceInRupees(totalPrice)}</span>
                                                </div>
                                            ) : (
                                                <span className='tracking-wide'>Bag</span>
                                            )
                                        }
                                    </div>
                                </button>
                            </div>
                        </div>
                    </div>
                )
            }

            <div className='container mx-auto px-4 lg:hidden pb-2'>
                <Search />
            </div>

            {
                openCartSection && (
                    <DisplayCartItem close={() => setOpenCartSection(false)} />
                )
            }
        </header>
    )
}

export default Header
