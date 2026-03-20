import React, { useState } from 'react'
import { DisplayPriceInRupees } from '../utils/DisplayPriceInRupees'
import { Link } from 'react-router-dom'
import { valideURLConvert } from '../utils/valideURLConvert'
import { pricewithDiscount } from '../utils/PriceWithDiscount'
import AddToCartButton from './AddToCartButton'
import { getImagePlaceholder } from '../utils/getImagePlaceholder'

const CardProduct = ({ data }) => {
    const url = `/product/${valideURLConvert(data.name)}-${data._id}`
    const fallbackImage = getImagePlaceholder(data.name)

    return (
        <Link to={url} className='group bg-white rounded-2xl overflow-hidden min-w-[140px] md:min-w-[180px] lg:min-w-[220px] card-hover border border-slate-100/60 shadow-[0_2px_10px_-4px_rgba(0,0,0,0.05)] flex flex-col'>
            {/* Image Container */}
            <div className='h-32 md:h-40 lg:h-48 w-full bg-slate-50/50 p-4 relative overflow-hidden flex items-center justify-center border-b border-slate-50'>
                <img
                    src={data.image[0] || fallbackImage}
                    className='w-full h-full object-contain group-hover:scale-110 transition-transform duration-500 ease-out drop-shadow-sm'
                    alt={data.name}
                    onError={(e) => { e.target.src = fallbackImage }}
                />
                {Boolean(data.discount) && (
                    <span className='absolute top-3 left-3 bg-gradient-to-r from-emerald-500 to-teal-500 text-white text-[10px] font-bold px-2.5 py-1 rounded-full shadow-sm tracking-wide z-10'>
                        {data.discount}% OFF
                    </span>
                )}
            </div>

            {/* Product Details */}
            <div className='p-4 md:p-5 flex flex-col flex-1 gap-2 bg-white'>
                <p className='font-semibold text-sm lg:text-[15px] text-slate-800 line-clamp-2 leading-snug min-h-[2.5rem] tracking-tight'>
                    {data.name}
                </p>

                {data.unit && (
                    <p className='text-[11px] lg:text-xs font-medium text-slate-500 bg-slate-100/80 self-start px-2 py-0.5 rounded-md'>
                        {data.unit}
                    </p>
                )}

                <div className='flex items-center justify-between gap-2 mt-auto pt-2'>
                    <div className='flex flex-col gap-0.5'>
                        <span className='font-bold text-slate-900 text-base md:text-lg tracking-tight leading-none'>
                            {DisplayPriceInRupees(pricewithDiscount(data.price, data.discount))}
                        </span>
                        {Boolean(data.discount) && (
                            <span className='text-[11px] font-medium text-slate-400 line-through leading-none'>
                                {DisplayPriceInRupees(data.price)}
                            </span>
                        )}
                    </div>
                    
                    <div className='shrink-0' onClick={(e) => e.preventDefault()}>
                        {data.stock === 0 ? (
                            <p className='text-rose-500 text-xs font-bold bg-rose-50 px-2 py-1 pb-1.5 rounded-lg'>Out of stock</p>
                        ) : (
                            <AddToCartButton data={data} />
                        )}
                    </div>
                </div>
            </div>
        </Link>
    )
}

export default CardProduct
