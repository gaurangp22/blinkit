import React, { useEffect, useState } from 'react'
import UploadSubCategoryModel from '../components/UploadSubCategoryModel'
import AxiosToastError from '../utils/AxiosToastError'
import Axios from '../utils/Axios'
import SummaryApi from '../common/SummaryApi'
import DisplayTable from '../components/DisplayTable'
import { createColumnHelper } from '@tanstack/react-table'
import ViewImage from '../components/ViewImage'
import { LuPencil } from "react-icons/lu";
import { MdDelete  } from "react-icons/md";
import { HiPencil } from "react-icons/hi";
import EditSubCategory from '../components/EditSubCategory'
import CofirmBox from '../components/CofirmBox'
import toast from 'react-hot-toast'

const SubCategoryPage = () => {
  const [openAddSubCategory,setOpenAddSubCategory] = useState(false)
  const [data,setData] = useState([])
  const [loading,setLoading] = useState(false)
  const columnHelper = createColumnHelper()
  const [ImageURL,setImageURL] = useState("")
  const [openEdit,setOpenEdit] = useState(false)
  const [editData,setEditData] = useState({
    _id : ""
  })
  const [deleteSubCategory,setDeleteSubCategory] = useState({
      _id : ""
  })
  const [openDeleteConfirmBox,setOpenDeleteConfirmBox] = useState(false)


  const fetchSubCategory = async()=>{
    try {
        setLoading(true)
        const response = await Axios({
          ...SummaryApi.getSubCategory
        })
        const { data : responseData } = response

        if(responseData.success){
          setData(responseData.data)
        }
    } catch (error) {
       AxiosToastError(error)
    } finally{
      setLoading(false)
    }
  }

  useEffect(()=>{
    fetchSubCategory()
  },[])

  const column = [
    columnHelper.accessor('name',{
      header : "Name"
    }),
    columnHelper.accessor('image',{
      header : "Image",
      cell : ({row})=>{
        console.log("row",)
        return <div className='flex justify-center items-center'>
            <img 
                src={row.original.image}
                alt={row.original.name}
                className='w-8 h-8 cursor-pointer'
                onClick={()=>{
                  setImageURL(row.original.image)
                }}      
            />
        </div>
      }
    }),
    columnHelper.accessor("category",{
       header : "Category",
       cell : ({row})=>{
        return(
          <>
            {
              row.original.category.map((c,index)=>{
                return(
                  <p key={c._id+"table"} className='shadow-md px-1 inline-block'>{c.name}</p>
                )
              })
            }
          </>
        )
       }
    }),
    columnHelper.accessor("_id",{
      header : "Action",
      cell : ({row})=>{
        return(
          <div className='flex items-center justify-center gap-3'>
              <button onClick={()=>{
                  setOpenEdit(true)
                  setEditData(row.original)
              }} className='p-2 bg-green-100 rounded-full hover:text-green-600'>
                  <HiPencil size={20}/>
              </button>
              <button onClick={()=>{
                setOpenDeleteConfirmBox(true)
                setDeleteSubCategory(row.original)
              }} className='p-2 bg-red-100 rounded-full text-red-500 hover:text-red-600'>
                  <MdDelete  size={20}/>
              </button>
          </div>
        )
      }
    })
  ]

  const handleDeleteSubCategory = async()=>{
      try {
          const response = await Axios({
              ...SummaryApi.deleteSubCategory,
              data : deleteSubCategory
          })

          const { data : responseData } = response

          if(responseData.success){
             toast.success(responseData.message)
             fetchSubCategory()
             setOpenDeleteConfirmBox(false)
             setDeleteSubCategory({_id : ""})
          }
      } catch (error) {
        AxiosToastError(error)
      }
  }
  return (
    <section className='bg-slate-50 min-h-[calc(100vh-80px)] p-4 sm:p-6'>
        <div className='p-4 bg-white shadow-sm rounded-xl flex items-center justify-between border border-slate-100 mb-6'>
            <h2 className='font-bold text-xl text-slate-800 tracking-tight'>Sub Categories</h2>
            <button onClick={()=>setOpenAddSubCategory(true)} className='text-sm bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-lg font-medium transition-colors shadow-sm'>
                + Add Sub Category
            </button>
        </div>

        <div className='bg-white rounded-xl shadow-[0_2px_10px_-3px_rgba(6,81,237,0.1)] border border-slate-100 overflow-x-auto w-full'>
            <DisplayTable
                data={data}
                column={column}
            />
        </div>


        {
          openAddSubCategory && (
            <UploadSubCategoryModel 
              close={()=>setOpenAddSubCategory(false)}
              fetchData={fetchSubCategory}
            />
          )
        }

        {
          ImageURL &&
          <ViewImage url={ImageURL} close={()=>setImageURL("")}/>
        }

        {
          openEdit && 
          <EditSubCategory 
            data={editData} 
            close={()=>setOpenEdit(false)}
            fetchData={fetchSubCategory}
          />
        }

        {
          openDeleteConfirmBox && (
            <CofirmBox 
              cancel={()=>setOpenDeleteConfirmBox(false)}
              close={()=>setOpenDeleteConfirmBox(false)}
              confirm={handleDeleteSubCategory}
            />
          )
        }
    </section>
  )
}

export default SubCategoryPage
