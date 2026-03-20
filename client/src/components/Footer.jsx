import React from 'react'
import { FaFacebook, FaInstagram, FaLinkedin } from "react-icons/fa";
import { BsCart4 } from "react-icons/bs";
import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className='bg-slate-900 text-slate-300'>
      <div className='container mx-auto px-4 py-10'>
        <div className='grid grid-cols-1 md:grid-cols-3 gap-8'>
          {/* Brand */}
          <div>
            <div className='flex items-center gap-2 mb-4'>
              <div className='w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center'>
                <BsCart4 size={18} className='text-white' />
              </div>
              <span className='text-xl font-bold text-white'>Cartify</span>
            </div>
            <p className='text-sm text-slate-400 leading-relaxed'>
              A Modern Shopping Cart Solution. Browse products, add to cart, and checkout with ease.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className='text-white font-semibold mb-4'>Quick Links</h4>
            <div className='grid gap-2 text-sm'>
              <Link to="/" className='hover:text-indigo-400 transition-colors'>Home</Link>
              <Link to="/search" className='hover:text-indigo-400 transition-colors'>Search Products</Link>
              <Link to="/login" className='hover:text-indigo-400 transition-colors'>Login</Link>
              <Link to="/register" className='hover:text-indigo-400 transition-colors'>Register</Link>
            </div>
          </div>

          {/* Contact */}
          <div>
            <h4 className='text-white font-semibold mb-4'>Connect</h4>
            <div className='flex items-center gap-4 text-xl'>
              <a href='#' className='hover:text-indigo-400 transition-colors p-2 rounded-lg hover:bg-slate-800'>
                <FaFacebook />
              </a>
              <a href='#' className='hover:text-indigo-400 transition-colors p-2 rounded-lg hover:bg-slate-800'>
                <FaInstagram />
              </a>
              <a href='#' className='hover:text-indigo-400 transition-colors p-2 rounded-lg hover:bg-slate-800'>
                <FaLinkedin />
              </a>
            </div>
          </div>
        </div>

        <div className='border-t border-slate-800 mt-8 pt-6 text-center text-sm text-slate-500'>
          <p>&copy; {new Date().getFullYear()} Cartify &mdash; A Modern Shopping Cart Solution. All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
