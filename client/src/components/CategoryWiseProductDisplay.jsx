import React, { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import AxiosToastError from '../utils/AxiosToastError'
import Axios from '../utils/Axios'
import SummaryApi from '../common/SummaryApi'
import CardLoading from './CardLoading'
import CardProduct from './CardProduct'
import { FaAngleLeft, FaAngleRight } from "react-icons/fa6";
import { useSelector } from 'react-redux'
import { valideURLConvert } from '../utils/valideURLConvert'

const CategoryWiseProductDisplay = ({ id, name }) => {
    const [data, setData] = useState([])
    const [loading, setLoading] = useState(false)
    const containerRef = useRef()
    const subCategoryData = useSelector(state => state.product.allSubCategory)
    const loadingCardNumber = new Array(6).fill(null)

    const fetchCategoryWiseProduct = async () => {
        try {
            setLoading(true)
            const response = await Axios({
                ...SummaryApi.getProductByCategory,
                data: { id: id }
            })
            const { data: responseData } = response
            if (responseData.success) {
                setData(responseData.data)
            }
        } catch (error) {
            AxiosToastError(error)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        fetchCategoryWiseProduct()
    }, [])

    const handleScrollRight = () => { containerRef.current.scrollLeft += 200 }
    const handleScrollLeft = () => { containerRef.current.scrollLeft -= 200 }

    const handleRedirectProductListpage = () => {
        const subcategory = subCategoryData.find(sub => {
            return sub.category.some(c => c._id == id)
        })
        return `/${valideURLConvert(name)}-${id}/${valideURLConvert(subcategory?.name)}-${subcategory?._id}`
    }

    const redirectURL = handleRedirectProductListpage()

    if (!loading && data.length === 0) return null

    return (
        <div className='py-4'>
            <div className='container mx-auto px-4 flex items-center justify-between gap-4 mb-3'>
                <h3 className='font-bold text-lg md:text-xl text-slate-800'>{name}</h3>
                <Link to={redirectURL} className='text-indigo-600 hover:text-indigo-800 text-sm font-medium transition-colors'>
                    See All →
                </Link>
            </div>
            <div className='relative flex items-center'>
                <div className='flex gap-3 md:gap-4 lg:gap-5 container mx-auto px-4 overflow-x-scroll scrollbar-none scroll-smooth' ref={containerRef}>
                    {loading && loadingCardNumber.map((_, index) => (
                        <CardLoading key={"catwise" + index} />
                    ))}
                    {data.map((p, index) => (
                        <CardProduct data={p} key={p._id + "catwise" + index} />
                    ))}
                </div>
                <div className='w-full left-0 right-0 container mx-auto px-2 absolute hidden lg:flex justify-between pointer-events-none'>
                    <button onClick={handleScrollLeft} className='pointer-events-auto z-10 bg-white hover:bg-indigo-50 shadow-lg text-indigo-600 p-2.5 rounded-full border border-slate-100 transition-colors'>
                        <FaAngleLeft />
                    </button>
                    <button onClick={handleScrollRight} className='pointer-events-auto z-10 bg-white hover:bg-indigo-50 shadow-lg text-indigo-600 p-2.5 rounded-full border border-slate-100 transition-colors'>
                        <FaAngleRight />
                    </button>
                </div>
            </div>
        </div>
    )
}

export default CategoryWiseProductDisplay
