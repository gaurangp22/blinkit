import React, { useEffect, useState } from 'react'
import { IoSearch } from "react-icons/io5";
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { TypeAnimation } from 'react-type-animation';
import { FaArrowLeft } from "react-icons/fa";
import useMobile from '../hooks/useMobile';

const Search = () => {
    const navigate = useNavigate()
    const location = useLocation()
    const [isSearchPage, setIsSearchPage] = useState(false)
    const [isMobile] = useMobile()
    const params = useLocation()
    const searchText = params.search.slice(3)

    useEffect(() => {
        setIsSearchPage(location.pathname === "/search")
    }, [location])

    const redirectToSearchPage = () => navigate("/search")

    const handleOnChange = (e) => {
        navigate(`/search?q=${e.target.value}`)
    }

    return (
        <div className='w-full min-w-[280px] lg:min-w-[400px] h-10 lg:h-11 rounded-xl border border-slate-200 overflow-hidden flex items-center text-slate-400 bg-slate-50 group focus-within:border-indigo-400 focus-within:bg-white focus-within:shadow-md focus-within:shadow-indigo-100 transition-all'>
            <div>
                {
                    (isMobile && isSearchPage) ? (
                        <Link to={"/"} className='flex justify-center items-center h-full p-2 m-1 group-focus-within:text-indigo-600 bg-white rounded-full shadow-sm'>
                            <FaArrowLeft size={16} />
                        </Link>
                    ) : (
                        <button className='flex justify-center items-center h-full px-3 group-focus-within:text-indigo-600 transition-colors'>
                            <IoSearch size={20} />
                        </button>
                    )
                }
            </div>
            <div className='w-full h-full'>
                {
                    !isSearchPage ? (
                        <div onClick={redirectToSearchPage} className='w-full h-full flex items-center text-sm'>
                            <TypeAnimation
                                sequence={[
                                    'Search "milk"', 1000,
                                    'Search "bread"', 1000,
                                    'Search "sugar"', 1000,
                                    'Search "chips"', 1000,
                                    'Search "soap"', 1000,
                                    'Search "juice"', 1000,
                                ]}
                                wrapper="span"
                                speed={50}
                                repeat={Infinity}
                            />
                        </div>
                    ) : (
                        <div className='w-full h-full'>
                            <input
                                type='text'
                                placeholder='Search for products...'
                                autoFocus
                                defaultValue={searchText}
                                className='bg-transparent w-full h-full outline-none text-slate-700 text-sm'
                                onChange={handleOnChange}
                            />
                        </div>
                    )
                }
            </div>
        </div>
    )
}

export default Search
