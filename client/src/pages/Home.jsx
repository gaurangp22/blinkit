import React from 'react'
import { useSelector } from 'react-redux'
import { valideURLConvert } from '../utils/valideURLConvert'
import { useNavigate } from 'react-router-dom'
import CategoryWiseProductDisplay from '../components/CategoryWiseProductDisplay'
import { BsCart4 } from "react-icons/bs";

const Home = () => {
  const loadingCategory = useSelector(state => state.product.loadingCategory)
  const categoryData = useSelector(state => state.product.allCategory)
  const subCategoryData = useSelector(state => state.product.allSubCategory)
  const navigate = useNavigate()

  const handleRedirectProductListpage = (id, cat) => {
    const subcategory = subCategoryData.find(sub => {
      return sub.category.some(c => c._id == id)
    })
    const url = `/${valideURLConvert(cat)}-${id}/${valideURLConvert(subcategory?.name)}-${subcategory?._id}`
    navigate(url)
  }

  return (
    <section className='bg-slate-50 min-h-screen'>
      {/* Hero Section */}
      <div className='gradient-bg pb-24 lg:pb-32 pt-16 lg:pt-24 min-h-[500px] flex items-center relative'>
        <div className='absolute inset-0 overflow-hidden pointer-events-none opacity-20'>
           {/* Decorative elements behind hero */}
           <div className='absolute -top-20 -right-20 w-96 h-96 bg-emerald-500 rounded-full mix-blend-screen filter blur-[100px] animate-pulse' style={{ animationDuration: '8s' }}></div>
           <div className='absolute -bottom-32 -left-20 w-[30rem] h-[30rem] bg-indigo-500 rounded-full mix-blend-screen filter blur-[120px]'></div>
        </div>
        
        <div className='container mx-auto px-4 relative z-10'>
          <div className='text-center text-white max-w-4xl mx-auto'>
            <div className='inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 mb-8 text-sm font-medium tracking-wide'>
              <span className='w-2 h-2 rounded-full bg-emerald-400 animate-ping'></span>
              Delivery in 10 minutes
            </div>
            <h1 className='text-4xl md:text-5xl lg:text-7xl font-extrabold mb-6 leading-[1.1] tracking-tight'>
              Groceries delivered.<br/>
              <span className='text-transparent bg-clip-text bg-gradient-to-r from-emerald-300 to-emerald-500'>Without the wait.</span>
            </h1>
            <p className='text-lg md:text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed mb-10 font-normal'>
              Your favorite daily essentials and premium products. Handpicked and delivered to your doorstep in minutes.
            </p>
            <button
              onClick={() => navigate('/search')}
              className='btn-premium px-10 py-4 bg-emerald-500 text-white text-lg font-semibold rounded-2xl shadow-float hover:bg-emerald-400 hover:-translate-y-1 transition-all'
            >
              Start Shopping Now
            </button>
          </div>
        </div>
      </div>

      {/* Categories */}
      <div className='container mx-auto px-4 -mt-16 lg:-mt-20 relative z-20 pb-8'>
        <div className='bg-white/90 backdrop-blur-xl rounded-[2rem] shadow-premium p-6 md:p-8 lg:p-10 border border-slate-100'>
          <div className='flex items-center justify-between mb-8'>
            <h2 className='text-2xl font-bold text-slate-900 tracking-tight'>Shop by Category</h2>
          </div>
          
          <div className='grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-8 gap-x-4 gap-y-8'>
            {
              loadingCategory ? (
                new Array(8).fill(null).map((_, index) => (
                  <div key={index + "loadcat"} className='flex flex-col items-center gap-3 animate-pulse'>
                    <div className='w-20 h-20 bg-slate-200 rounded-2xl'></div>
                    <div className='w-16 h-4 bg-slate-200 rounded-md'></div>
                  </div>
                ))
              ) : (
                categoryData.map((cat) => (
                  <div
                    key={cat._id + "cat"}
                    className='group cursor-pointer flex flex-col items-center text-center'
                    onClick={() => handleRedirectProductListpage(cat._id, cat.name)}
                  >
                    <div className='w-20 h-20 md:w-24 md:h-24 bg-slate-50 group-hover:bg-emerald-50 rounded-[1.5rem] mb-3 flex items-center justify-center transition-all duration-300 group-hover:shadow-soft border border-slate-100 group-hover:border-emerald-100 p-4 shrink-0 overflow-hidden relative'>
                      <img
                        src={cat.image}
                        className='w-full h-full object-contain group-hover:scale-110 transition-transform duration-500 ease-out'
                        alt={cat.name}
                        onError={(e) => { e.target.src = `/api/placeholder/${encodeURIComponent(cat.name || 'Category')}` }}
                      />
                    </div>
                    <p className='text-sm font-semibold text-slate-700 group-hover:text-emerald-700 line-clamp-2 transition-colors px-1'>{cat.name}</p>
                  </div>
                ))
              )
            }
          </div>
        </div>
      </div>

      {/* Category wise products */}
      <div className='py-6'>
        {
          categoryData?.map((c) => (
            <CategoryWiseProductDisplay
              key={c?._id + "catwiseprod"}
              id={c?._id}
              name={c?.name}
            />
          ))
        }
      </div>
    </section>
  )
}

export default Home
