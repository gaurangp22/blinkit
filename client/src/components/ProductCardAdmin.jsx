import React, { useState } from 'react'
import EditProductAdmin from './EditProductAdmin'
import { IoClose } from 'react-icons/io5'
import SummaryApi from '../common/SummaryApi'
import Axios from '../utils/Axios'
import AxiosToastError from '../utils/AxiosToastError'
import toast from 'react-hot-toast'

const ProductCardAdmin = ({ data, fetchProductData }) => {
  const [editOpen, setEditOpen] = useState(false)
  const [openDelete, setOpenDelete] = useState(false)

  const handleDeleteCancel = () => setOpenDelete(false)

  const handleDelete = async () => {
    try {
      const response = await Axios({
        ...SummaryApi.deleteProduct,
        data: { _id: data._id }
      })
      const { data: responseData } = response
      if (responseData.success) {
        toast.success(responseData.message)
        if (fetchProductData) fetchProductData()
        setOpenDelete(false)
      }
    } catch (error) {
      AxiosToastError(error)
    }
  }

  return (
    <div className='w-36 p-4 bg-white rounded-xl border border-slate-100 shadow-sm'>
      <div className='h-24 flex items-center justify-center bg-slate-50 rounded-lg mb-2'>
        <img
          src={data?.image[0]}
          alt={data?.name}
          className='w-full h-full object-scale-down'
          onError={(e) => { e.target.src = `/api/placeholder/${encodeURIComponent(data?.name || 'Product')}` }}
        />
      </div>
      <p className='text-ellipsis line-clamp-2 font-medium text-sm text-slate-800'>{data?.name}</p>
      <p className='text-slate-400 text-xs'>{data?.unit}</p>
      <div className='grid grid-cols-2 gap-2 py-2'>
        <button onClick={() => setEditOpen(true)} className='px-1 py-1 text-xs font-medium border border-indigo-200 bg-indigo-50 text-indigo-600 hover:bg-indigo-100 rounded-lg transition-colors'>Edit</button>
        <button onClick={() => setOpenDelete(true)} className='px-1 py-1 text-xs font-medium border border-red-200 bg-red-50 text-red-600 hover:bg-red-100 rounded-lg transition-colors'>Delete</button>
      </div>

      {editOpen && (
        <EditProductAdmin fetchProductData={fetchProductData} data={data} close={() => setEditOpen(false)} />
      )}

      {openDelete && (
        <section className='fixed top-0 left-0 right-0 bottom-0 bg-black/60 backdrop-blur-sm z-50 p-4 flex justify-center items-center'>
          <div className='bg-white p-6 w-full max-w-md rounded-2xl shadow-xl'>
            <div className='flex items-center justify-between gap-4'>
              <h3 className='font-bold text-slate-800'>Delete Product</h3>
              <button onClick={() => setOpenDelete(false)} className='text-slate-400 hover:text-slate-600'>
                <IoClose size={22} />
              </button>
            </div>
            <p className='my-3 text-slate-600 text-sm'>Are you sure you want to permanently delete this product?</p>
            <div className='flex justify-end gap-3 pt-2'>
              <button onClick={handleDeleteCancel} className='px-4 py-2 rounded-xl border border-slate-200 text-slate-600 hover:bg-slate-50 text-sm font-medium transition-colors'>Cancel</button>
              <button onClick={handleDelete} className='px-4 py-2 rounded-xl bg-red-600 text-white hover:bg-red-700 text-sm font-medium transition-colors'>Delete</button>
            </div>
          </div>
        </section>
      )}
    </div>
  )
}

export default ProductCardAdmin
