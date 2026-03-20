import React, { useEffect, useState } from 'react'
import SummaryApi from '../common/SummaryApi'
import AxiosToastError from '../utils/AxiosToastError'
import Axios from '../utils/Axios'
import Loading from '../components/Loading'
import ProductCardAdmin from '../components/ProductCardAdmin'
import { IoSearchOutline } from "react-icons/io5";
import EditProductAdmin from '../components/EditProductAdmin'

const ProductAdmin = () => {
  const [productData,setProductData] = useState([])
  const [page,setPage] = useState(1)
  const [loading,setLoading] = useState(false)
  const [totalPageCount,setTotalPageCount] = useState(1)
  const [search,setSearch] = useState("")
  
  const fetchProductData = async()=>{
    try {
        setLoading(true)
        const response = await Axios({
           ...SummaryApi.getProduct,
           data : {
              page : page,
              limit : 12,
              search : search 
           }
        })

        const { data : responseData } = response 

        if(responseData.success){
          setTotalPageCount(responseData.totalNoPage)
          setProductData(responseData.data)
        }

    } catch (error) {
      AxiosToastError(error)
    }finally{
      setLoading(false)
    }
  }
  
  useEffect(()=>{
    fetchProductData()
  },[page])

  const handleNext = ()=>{
    if(page !== totalPageCount){
      setPage(preve => preve + 1)
    }
  }
  const handlePrevious = ()=>{
    if(page > 1){
      setPage(preve => preve - 1)
    }
  }

  const handleOnChange = (e)=>{
    const { value } = e.target
    setSearch(value)
    setPage(1)
  }

  useEffect(()=>{
    let flag = true 

    const interval = setTimeout(() => {
      if(flag){
        fetchProductData()
        flag = false
      }
    }, 300);

    return ()=>{
      clearTimeout(interval)
    }
  },[search])
  
  return (
    <section className='bg-slate-50 min-h-[calc(100vh-80px)] p-4 sm:p-6'>
        <div className='p-4 bg-white shadow-sm rounded-xl flex flex-col sm:flex-row items-start sm:items-center justify-between border border-slate-100 mb-6 gap-4'>
            <h2 className='font-bold text-xl text-slate-800 tracking-tight'>Manage Products</h2>
            <div className='h-10 min-w-[200px] sm:max-w-xs w-full bg-slate-50 px-4 flex items-center gap-3 py-2 rounded-lg border border-slate-200 focus-within:border-emerald-500 focus-within:ring-2 focus-within:ring-emerald-500/20 transition-all'>
                <IoSearchOutline size={20} className="text-slate-400"/>
                <input
                    type='text'
                    placeholder='Search products...' 
                    className='h-full w-full outline-none bg-transparent text-sm text-slate-700 placeholder:text-slate-400'
                    value={search}
                    onChange={handleOnChange}
                />
            </div>
        </div>
        {
          loading && (
            <Loading/>
          )
        }


        <div className='bg-transparent'>

            <div className='min-h-[55vh]'>
              <div className='grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4'>
                {
                  productData.map((p,index)=>{
                    return(
                      <ProductCardAdmin data={p} fetchProductData={fetchProductData}  />
                    )
                  })
                }
              </div>
            </div>
            
            <div className='flex justify-between items-center my-6 bg-white p-4 rounded-xl border border-slate-100 shadow-sm'>
              <button onClick={handlePrevious} className="border border-slate-200 px-4 py-2 hover:bg-slate-50 rounded-lg text-sm font-medium transition-colors disabled:opacity-50">Previous</button>
              <div className='w-full text-center text-sm font-semibold text-slate-600'>Page {page} of {totalPageCount}</div>
              <button onClick={handleNext} className="border border-slate-200 px-4 py-2 hover:bg-slate-50 rounded-lg text-sm font-medium transition-colors disabled:opacity-50">Next</button>
            </div>

        </div>
          

      
    </section>
  )
}

export default ProductAdmin
