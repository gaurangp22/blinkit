import React, { useEffect, useState } from 'react'
import UploadCategoryModel from '../components/UploadCategoryModel'
import Loading from '../components/Loading'
import NoData from '../components/NoData'
import Axios from '../utils/Axios'
import SummaryApi from '../common/SummaryApi'
import EditCategory from '../components/EditCategory'
import CofirmBox from '../components/CofirmBox'
import toast from 'react-hot-toast'
import AxiosToastError from '../utils/AxiosToastError'
import { useSelector } from 'react-redux'
import { HiPencil } from "react-icons/hi"
import { MdDelete  } from "react-icons/md"

const CategoryPage = () => {
    const [openUploadCategory,setOpenUploadCategory] = useState(false)
    const [loading,setLoading] = useState(false)
    const [categoryData,setCategoryData] = useState([])
    const [openEdit,setOpenEdit] = useState(false)
    const [editData,setEditData] = useState({
        name : "",
        image : "",
    })
    const [openConfimBoxDelete,setOpenConfirmBoxDelete] = useState(false)
    const [deleteCategory,setDeleteCategory] = useState({
        _id : ""
    })
    // const allCategory = useSelector(state => state.product.allCategory)


    // useEffect(()=>{
    //     setCategoryData(allCategory)
    // },[allCategory])
    
    const fetchCategory = async()=>{
        try {
            setLoading(true)
            const response = await Axios({
                ...SummaryApi.getCategory
            })
            const { data : responseData } = response

            if(responseData.success){
                setCategoryData(responseData.data)
            }
        } catch (error) {
            
        }finally{
            setLoading(false)
        }
    }

    useEffect(()=>{
        fetchCategory()
    },[])

    const handleDeleteCategory = async()=>{
        try {
            const response = await Axios({
                ...SummaryApi.deleteCategory,
                data : deleteCategory
            })

            const { data : responseData } = response

            if(responseData.success){
                toast.success(responseData.message)
                fetchCategory()
                setOpenConfirmBoxDelete(false)
            }
        } catch (error) {
            AxiosToastError(error)
        }
    }

  return (
    <section className='bg-slate-50 min-h-[calc(100vh-80px)] p-4 sm:p-6'>
        <div className='p-4 bg-white shadow-sm rounded-xl flex items-center justify-between border border-slate-100 mb-6'>
            <h2 className='font-bold text-xl text-slate-800 tracking-tight'>Manage Categories</h2>
            <button onClick={()=>setOpenUploadCategory(true)} className='text-sm bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-lg font-medium transition-colors shadow-sm'>
                + Add Category
            </button>
        </div>
        {
            !categoryData[0] && !loading && (
                <NoData/>
            )
        }

        <div className='grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4'>
            {
                categoryData.map((category,index)=>{
                    return(
                        <div className='w-full aspect-[3/4] bg-white rounded-xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-slate-100 overflow-hidden flex flex-col transition-all hover:-translate-y-1 hover:shadow-md' key={category._id}>
                            <div className="flex-1 w-full bg-slate-50/50 flex items-center justify-center p-4 relative group">
                                <img 
                                    alt={category.name}
                                    src={category.image}
                                    className='w-full h-full object-contain'
                                />
                                <div className='absolute inset-0 bg-slate-900/40 flex items-center justify-center gap-3 opacity-0 group-hover:opacity-100 transition-opacity backdrop-blur-[2px]'>
                                    <button onClick={()=>{
                                        setOpenEdit(true)
                                        setEditData(category)
                                    }} className='bg-white text-emerald-600 p-2.5 rounded-full hover:bg-emerald-50 transition-colors shadow-lg scale-90 group-hover:scale-100 duration-200'>
                                        <HiPencil size={18}/>
                                    </button>
                                    <button onClick={()=>{
                                        setOpenConfirmBoxDelete(true)
                                        setDeleteCategory(category)
                                    }} className='bg-white text-red-500 p-2.5 rounded-full hover:bg-red-50 transition-colors shadow-lg scale-90 group-hover:scale-100 duration-200'>
                                        <MdDelete size={18}/>
                                    </button>
                                </div>
                            </div>
                            <div className='py-3 px-2 border-t border-slate-100 bg-white'>
                                <h3 className="font-semibold text-sm text-slate-800 text-center truncate">{category.name}</h3>
                            </div>
                        </div>
                    )
                })
            }
        </div>

        {
            loading && (
                <Loading/>
            )
        }

        {
            openUploadCategory && (
                <UploadCategoryModel fetchData={fetchCategory} close={()=>setOpenUploadCategory(false)}/>
            )
        }

        {
            openEdit && (
                <EditCategory data={editData} close={()=>setOpenEdit(false)} fetchData={fetchCategory}/>
            )
        }

        {
           openConfimBoxDelete && (
            <CofirmBox close={()=>setOpenConfirmBoxDelete(false)} cancel={()=>setOpenConfirmBoxDelete(false)} confirm={handleDeleteCategory}/>
           ) 
        }
    </section>
  )
}

export default CategoryPage
