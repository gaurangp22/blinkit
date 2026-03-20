import React, { useEffect, useRef, useState } from 'react'
import { useParams } from 'react-router-dom'
import SummaryApi from '../common/SummaryApi'
import Axios from '../utils/Axios'
import AxiosToastError from '../utils/AxiosToastError'
import { FaAngleRight, FaAngleLeft } from "react-icons/fa6";
import { DisplayPriceInRupees } from '../utils/DisplayPriceInRupees'
import Divider from '../components/Divider'
import { pricewithDiscount } from '../utils/PriceWithDiscount'
import AddToCartButton from '../components/AddToCartButton'

const ProductDisplayPage = () => {
  const params = useParams()
  let productId = params?.product?.split("-")?.slice(-1)[0]
  const [data, setData] = useState({ name: "", image: [] })
  const [image, setImage] = useState(0)
  const [loading, setLoading] = useState(false)
  const imageContainer = useRef()

  const fetchProductDetails = async () => {
    try {
      const response = await Axios({ ...SummaryApi.getProductDetails, data: { productId } })
      const { data: responseData } = response
      if (responseData.success) setData(responseData.data)
    } catch (error) {
      AxiosToastError(error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchProductDetails() }, [params])

  const handleScrollRight = () => { imageContainer.current.scrollLeft += 100 }
  const handleScrollLeft = () => { imageContainer.current.scrollLeft -= 100 }

  return (
    <section className='container mx-auto p-4 grid lg:grid-cols-2 gap-8 bg-slate-50 min-h-[80vh]'>
      {/* Images */}
      <div className='bg-white rounded-2xl p-6 border border-slate-100'>
        <div className='lg:min-h-[50vh] lg:max-h-[50vh] rounded-xl min-h-56 max-h-56 h-full w-full bg-slate-50 flex items-center justify-center'>
          <img
            src={data.image[image]}
            className='w-full h-full object-scale-down'
            onError={(e) => { e.target.src = `/api/placeholder/${encodeURIComponent(data.name || 'Product')}` }}
          />
        </div>
        <div className='flex items-center justify-center gap-2 my-3'>
          {data.image.map((_, index) => (
            <div key={index + "dot"} className={`w-2.5 h-2.5 rounded-full transition-colors ${index === image ? 'bg-indigo-600' : 'bg-slate-200'}`}></div>
          ))}
        </div>
        <div className='grid relative'>
          <div ref={imageContainer} className='flex gap-3 z-10 relative w-full overflow-x-auto scrollbar-none'>
            {data.image.map((img, index) => (
              <div className='w-16 h-16 min-h-16 min-w-16 cursor-pointer rounded-lg border-2 border-transparent hover:border-indigo-300 transition-colors overflow-hidden bg-slate-50' key={img + index}>
                <img src={img} alt='thumb' onClick={() => setImage(index)} className='w-full h-full object-scale-down'
                  onError={(e) => { e.target.src = `/api/placeholder/Image+${index+1}` }} />
              </div>
            ))}
          </div>
          {data.image.length > 4 && (
            <div className='w-full h-full hidden lg:flex justify-between absolute items-center'>
              <button onClick={handleScrollLeft} className='z-10 bg-white p-1.5 rounded-full shadow-md text-slate-600 hover:text-indigo-600 transition-colors'><FaAngleLeft /></button>
              <button onClick={handleScrollRight} className='z-10 bg-white p-1.5 rounded-full shadow-md text-slate-600 hover:text-indigo-600 transition-colors'><FaAngleRight /></button>
            </div>
          )}
        </div>

        {/* Description - desktop */}
        <div className='my-4 hidden lg:grid gap-3'>
          {data.description && (
            <div>
              <p className='font-semibold text-slate-800'>Description</p>
              <p className='text-sm text-slate-600'>{data.description}</p>
            </div>
          )}
          {data.unit && (
            <div>
              <p className='font-semibold text-slate-800'>Unit</p>
              <p className='text-sm text-slate-600'>{data.unit}</p>
            </div>
          )}
          {data?.more_details && Object.keys(data?.more_details).map((element, index) => (
            <div key={element + index}>
              <p className='font-semibold text-slate-800'>{element}</p>
              <p className='text-sm text-slate-600'>{data?.more_details[element]}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Product Info */}
      <div className='bg-white rounded-2xl p-6 border border-slate-100 h-fit'>
        <div className='flex items-center gap-2 mb-3'>
          <span className='bg-emerald-50 text-emerald-700 text-xs font-semibold px-3 py-1 rounded-full'>In Stock</span>
          {Boolean(data.discount) && (
            <span className='bg-gradient-to-r from-orange-500 to-pink-500 text-white text-xs font-bold px-3 py-1 rounded-full'>{data.discount}% OFF</span>
          )}
        </div>

        <h2 className='text-xl font-bold text-slate-800 lg:text-3xl leading-tight'>{data.name}</h2>
        {data.unit && <p className='text-slate-500 mt-1'>{data.unit}</p>}

        <Divider />

        <div className='my-4'>
          <p className='text-sm text-slate-500 mb-2'>Price</p>
          <div className='flex items-center gap-3'>
            <div className='border-2 border-indigo-100 px-5 py-2.5 rounded-xl bg-indigo-50'>
              <p className='font-bold text-xl lg:text-2xl text-indigo-700'>{DisplayPriceInRupees(pricewithDiscount(data.price, data.discount))}</p>
            </div>
            {Boolean(data.discount) && (
              <p className='line-through text-slate-400 text-lg'>{DisplayPriceInRupees(data.price)}</p>
            )}
          </div>
        </div>

        {data.stock === 0 ? (
          <p className='text-lg text-red-500 my-4 font-medium'>Out of Stock</p>
        ) : (
          <div className='my-4'>
            <AddToCartButton data={data} />
          </div>
        )}

        <Divider />

        <h2 className='font-bold text-slate-800 mt-4 mb-3'>Why shop from Cartify?</h2>
        <div className='grid gap-4'>
          <div className='flex items-start gap-3'>
            <div className='w-10 h-10 min-w-10 rounded-xl bg-indigo-50 flex items-center justify-center text-xl'>🚀</div>
            <div>
              <p className='font-semibold text-sm text-slate-800'>Fast Delivery</p>
              <p className='text-xs text-slate-500'>Get your order delivered quickly to your doorstep.</p>
            </div>
          </div>
          <div className='flex items-start gap-3'>
            <div className='w-10 h-10 min-w-10 rounded-xl bg-emerald-50 flex items-center justify-center text-xl'>💰</div>
            <div>
              <p className='font-semibold text-sm text-slate-800'>Best Prices</p>
              <p className='text-xs text-slate-500'>Best price destination with great offers.</p>
            </div>
          </div>
          <div className='flex items-start gap-3'>
            <div className='w-10 h-10 min-w-10 rounded-xl bg-purple-50 flex items-center justify-center text-xl'>📦</div>
            <div>
              <p className='font-semibold text-sm text-slate-800'>Wide Selection</p>
              <p className='text-xs text-slate-500'>Choose from thousands of products across categories.</p>
            </div>
          </div>
        </div>

        {/* Description - mobile */}
        <div className='my-4 lg:hidden grid gap-3'>
          <Divider />
          {data.description && (
            <div>
              <p className='font-semibold text-slate-800'>Description</p>
              <p className='text-sm text-slate-600'>{data.description}</p>
            </div>
          )}
          {data.unit && (
            <div>
              <p className='font-semibold text-slate-800'>Unit</p>
              <p className='text-sm text-slate-600'>{data.unit}</p>
            </div>
          )}
        </div>
      </div>
    </section>
  )
}

export default ProductDisplayPage
