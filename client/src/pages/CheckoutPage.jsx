import React, { useState } from 'react'
import { useGlobalContext } from '../provider/GlobalProvider'
import { DisplayPriceInRupees } from '../utils/DisplayPriceInRupees'
import { useSelector } from 'react-redux'
import AxiosToastError from '../utils/AxiosToastError'
import Axios from '../utils/Axios'
import SummaryApi from '../common/SummaryApi'
import toast from 'react-hot-toast'
import { useNavigate, useLocation } from 'react-router-dom'
import { pricewithDiscount } from '../utils/PriceWithDiscount'
import { FaCheck } from "react-icons/fa6"

const CheckoutPage = () => {
  const { notDiscountTotalPrice, totalPrice, totalQty, fetchCartItem, fetchOrder } = useGlobalContext()
  const cartItemsList = useSelector(state => state.cartItem.cart)
  const navigate = useNavigate()
  const location = useLocation()
  const [step, setStep] = useState(location?.state?.step || 1)
  const [loading, setLoading] = useState(false)
  const [addressErrors, setAddressErrors] = useState({})
  const [countryCode, setCountryCode] = useState('+91')
  const [address, setAddress] = useState({
    name: '',
    mobile: '',
    address_line: '',
    city: '',
    state: '',
    pincode: '',
  })

  const handleAddressChange = (e) => {
    setAddress(prev => ({ ...prev, [e.target.name]: e.target.value }))
    if (addressErrors[e.target.name]) setAddressErrors(prev => ({ ...prev, [e.target.name]: "" }))
  }

  const handlePincodeChange = async (e) => {
    const value = e.target.value;
    setAddress(prev => ({ ...prev, pincode: value }));
    if (addressErrors.pincode) setAddressErrors(prev => ({ ...prev, pincode: "" }));

    if (value.length === 6 && /^\d{6}$/.test(value)) {
      try {
        const res = await fetch(`https://api.postalpincode.in/pincode/${value}`);
        const data = await res.json();
        
        if (data && data[0] && data[0].Status === 'Success') {
          const details = data[0].PostOffice[0];
          setAddress(prev => ({ 
            ...prev, 
            city: details.District, 
            state: details.State 
          }));
          setAddressErrors(prev => ({ ...prev, city: "", state: "" }));
          toast.success("City and State auto-filled!");
        } else {
          setAddressErrors(prev => ({ ...prev, pincode: "Invalid Pincode" }));
        }
      } catch (error) {
        console.error("Failed to fetch pincode details", error);
      }
    }
  }

  const validateAddress = () => {
    const err = {}
    if (!address.name.trim() || address.name.trim().length < 2) err.name = "Full name is required"
    const cleanMobile = address.mobile.replace(/[\s\-\+]/g, '')
    if (!cleanMobile || cleanMobile.length < 8 || cleanMobile.length > 15) err.mobile = "Enter a valid phone number"
    if (!address.address_line.trim()) err.address_line = "Address is required"
    if (!address.city.trim()) err.city = "City is required"
    if (!address.state.trim()) err.state = "State is required"
    if (!address.pincode.trim() || !/^\d{6}$/.test(address.pincode.trim())) err.pincode = "Enter a valid 6-digit pincode"
    setAddressErrors(err)
    return Object.keys(err).length === 0
  }

  const isAddressValid = address.name && address.mobile && address.address_line && address.city && address.state && address.pincode

  const handlePlaceOrder = async () => {
    try {
      setLoading(true)
      const response = await Axios({
        ...SummaryApi.CashOnDeliveryOrder,
        data: {
          list_items: cartItemsList,
          delivery_address: { ...address, mobile: `${countryCode} ${address.mobile}` },
          subTotalAmt: totalPrice,
          totalAmt: totalPrice,
        }
      })
      const { data: responseData } = response
      if (responseData.success) {
        toast.success(responseData.message)
        if (fetchCartItem) fetchCartItem()
        if (fetchOrder) fetchOrder()
        navigate('/success', { state: { text: "Order" } })
      }
    } catch (error) {
      AxiosToastError(error)
    } finally {
      setLoading(false)
    }
  }

  const StepIndicator = () => (
    <div className='flex items-center justify-center gap-0 mb-8'>
      {[
        { num: 1, label: 'Review Cart' },
        { num: 2, label: 'Delivery Address' },
        { num: 3, label: 'Confirm Order' },
      ].map((s, i) => (
        <React.Fragment key={s.num}>
          <div className='flex flex-col items-center'>
            <div className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold transition-all ${step > s.num ? 'bg-emerald-500 text-white' : step === s.num ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200' : 'bg-slate-100 text-slate-400'}`}>
              {step > s.num ? <FaCheck size={14} /> : s.num}
            </div>
            <p className={`text-xs mt-1.5 font-medium ${step >= s.num ? 'text-slate-700' : 'text-slate-400'}`}>{s.label}</p>
          </div>
          {i < 2 && (
            <div className={`w-16 sm:w-24 h-0.5 mx-1 mb-5 ${step > s.num ? 'bg-emerald-500' : 'bg-slate-200'}`} />
          )}
        </React.Fragment>
      ))}
    </div>
  )

  return (
    <section className='bg-slate-50 min-h-[80vh] py-6'>
      <div className='container mx-auto px-4 max-w-3xl'>
        <h1 className='text-2xl font-bold text-slate-800 text-center mb-2'>Checkout</h1>
        <StepIndicator />

        {/* Step 1: Review Cart */}
        {step === 1 && (
          <div className='bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden'>
            <div className='p-5 border-b border-slate-100'>
              <h2 className='font-bold text-lg text-slate-800'>Review Your Cart ({totalQty} items)</h2>
            </div>
            <div className='divide-y divide-slate-50'>
              {cartItemsList.map((item) => (
                <div key={item._id} className='flex items-center gap-4 p-4'>
                  <div className='w-16 h-16 min-w-16 bg-slate-50 rounded-xl overflow-hidden flex items-center justify-center border border-slate-100'>
                    <img
                      src={item?.productId?.image?.[0]}
                      className='w-full h-full object-scale-down'
                      alt={item?.productId?.name}
                      onError={(e) => { e.target.src = `/api/placeholder/${encodeURIComponent(item?.productId?.name || 'Item')}` }}
                    />
                  </div>
                  <div className='flex-1 min-w-0'>
                    <p className='font-medium text-slate-800 text-sm line-clamp-1'>{item?.productId?.name}</p>
                    <p className='text-xs text-slate-400 mt-0.5'>{item?.productId?.unit}</p>
                    <p className='text-xs text-slate-500 mt-0.5'>Qty: {item?.quantity}</p>
                  </div>
                  <div className='text-right'>
                    <p className='font-bold text-slate-800 text-sm'>
                      {DisplayPriceInRupees(pricewithDiscount(item?.productId?.price, item?.productId?.discount) * item?.quantity)}
                    </p>
                    {Boolean(item?.productId?.discount) && (
                      <p className='text-xs text-slate-400 line-through'>
                        {DisplayPriceInRupees(item?.productId?.price * item?.quantity)}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </div>
            <div className='p-5 bg-slate-50 border-t border-slate-100'>
              <div className='flex justify-between text-sm text-slate-500'>
                <span>Subtotal</span>
                <span className='flex gap-2'>
                  <span className='line-through text-slate-300'>{DisplayPriceInRupees(notDiscountTotalPrice)}</span>
                  <span className='text-slate-700 font-medium'>{DisplayPriceInRupees(totalPrice)}</span>
                </span>
              </div>
              <div className='flex justify-between text-sm text-slate-500 mt-1'>
                <span>Delivery</span>
                <span className='text-emerald-600 font-medium'>Free</span>
              </div>
              <div className='flex justify-between font-bold text-slate-800 mt-2 pt-2 border-t border-slate-200'>
                <span>Total</span>
                <span>{DisplayPriceInRupees(totalPrice)}</span>
              </div>
            </div>
            <div className='p-6'>
              <button
                onClick={() => setStep(2)}
                disabled={!cartItemsList.length}
                className='btn-premium w-full py-4 bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-lg rounded-xl transition-all shadow-lg shadow-emerald-600/20 disabled:opacity-50'
              >
                Continue to Address
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Delivery Address */}
        {step === 2 && (
          <div className='bg-white rounded-3xl shadow-soft border border-slate-100 overflow-hidden'>
            <div className='p-6 border-b border-slate-100'>
              <h2 className='font-extrabold text-xl text-slate-900'>Delivery Address</h2>
              <p className='text-sm text-slate-500 mt-1 font-medium'>Enter the address where you want your order delivered</p>
            </div>
            <div className='p-5 grid gap-4'>
              <div className='grid sm:grid-cols-2 gap-4'>
                <div>
                  <label className='text-sm font-medium text-slate-700 mb-1 block'>Full Name *</label>
                  <input name='name' value={address.name} onChange={handleAddressChange}
                    className={`w-full px-4 py-2.5 border rounded-xl outline-none text-sm transition-all ${addressErrors.name ? 'border-red-400 ring-2 ring-red-100' : 'border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'}`}
                    placeholder='John Doe' />
                  {addressErrors.name && <p className='text-xs text-red-500 mt-1'>{addressErrors.name}</p>}
                </div>
                <div>
                  <label className='text-sm font-medium text-slate-700 mb-1 block'>Phone Number *</label>
                  <div className="flex gap-2">
                    <select 
                      value={countryCode} 
                      onChange={(e) => setCountryCode(e.target.value)}
                      className="w-24 px-2 py-2.5 border border-slate-200 rounded-xl outline-none text-sm bg-white focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100 transition-all font-medium text-slate-700"
                    >
                      <option value="+91">+91 (IN)</option>
                      <option value="+1">+1 (US)</option>
                      <option value="+44">+44 (UK)</option>
                      <option value="+61">+61 (AU)</option>
                      <option value="+971">+971 (UAE)</option>
                    </select>
                    <input name='mobile' value={address.mobile} onChange={handleAddressChange}
                      className={`flex-1 px-4 py-2.5 border rounded-xl outline-none text-sm transition-all sm:text-base ${addressErrors.mobile ? 'border-red-400 ring-2 ring-red-100' : 'border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'}`}
                      placeholder='9876543210' />
                  </div>
                  {addressErrors.mobile && <p className='text-xs text-red-500 mt-1'>{addressErrors.mobile}</p>}
                </div>
              </div>
              <div>
                <label className='text-sm font-medium text-slate-700 mb-1 block'>Address Line *</label>
                <input name='address_line' value={address.address_line} onChange={handleAddressChange}
                  className={`w-full px-4 py-2.5 border rounded-xl outline-none text-sm transition-all ${addressErrors.address_line ? 'border-red-400 ring-2 ring-red-100' : 'border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'}`}
                  placeholder='House/Flat No., Street, Landmark' />
                {addressErrors.address_line && <p className='text-xs text-red-500 mt-1'>{addressErrors.address_line}</p>}
              </div>
              <div className='grid sm:grid-cols-3 gap-4'>
                <div>
                  <label className='text-sm font-medium text-slate-700 mb-1 block'>City *</label>
                  <input name='city' value={address.city} onChange={handleAddressChange}
                    className={`w-full px-4 py-2.5 border rounded-xl outline-none text-sm transition-all ${addressErrors.city ? 'border-red-400 ring-2 ring-red-100' : 'border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'}`}
                    placeholder='City' />
                  {addressErrors.city && <p className='text-xs text-red-500 mt-1'>{addressErrors.city}</p>}
                </div>
                <div>
                  <label className='text-sm font-medium text-slate-700 mb-1 block'>State *</label>
                  <input name='state' value={address.state} onChange={handleAddressChange}
                    className={`w-full px-4 py-2.5 border rounded-xl outline-none text-sm transition-all ${addressErrors.state ? 'border-red-400 ring-2 ring-red-100' : 'border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'}`}
                    placeholder='State' />
                  {addressErrors.state && <p className='text-xs text-red-500 mt-1'>{addressErrors.state}</p>}
                </div>
                <div>
                  <label className='text-sm font-medium text-slate-700 mb-1 block'>Pincode *</label>
                  <input name='pincode' value={address.pincode} onChange={handlePincodeChange}
                    className={`w-full px-4 py-2.5 border rounded-xl outline-none text-sm transition-all ${addressErrors.pincode ? 'border-red-400 ring-2 ring-red-100' : 'border-slate-200 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-100'}`}
                    placeholder='110001 (Auto-fills City/State)' maxLength={6} />
                  {addressErrors.pincode && <p className='text-xs text-red-500 mt-1'>{addressErrors.pincode}</p>}
                </div>
              </div>
            </div>
            <div className='p-6 flex gap-4 bg-slate-50/50 border-t border-slate-100'>
              <button onClick={() => setStep(1)}
                className='flex-1 py-4 bg-white border border-slate-200 text-slate-700 font-bold rounded-xl hover:bg-slate-50 hover:border-slate-300 transition-all shadow-sm'>
                Back
              </button>
              <button onClick={() => { if (validateAddress()) setStep(3) }}
                className='btn-premium flex-1 py-4 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-xl transition-all shadow-lg shadow-slate-900/20 disabled:opacity-50 disabled:cursor-not-allowed'>
                Review Order
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Confirm Order */}
        {step === 3 && (
          <div className='bg-white rounded-3xl shadow-soft border border-slate-100 overflow-hidden'>
            <div className='p-6 border-b border-slate-100'>
              <h2 className='font-extrabold text-xl text-slate-900'>Order Summary</h2>
            </div>
            <div className='p-6 grid gap-6'>
              {/* Delivery Address Card */}
              <div className='bg-emerald-50/50 border border-emerald-100 rounded-2xl p-5'>
                <div className='flex items-center justify-between mb-3'>
                  <h3 className='font-bold text-emerald-900 text-sm'>Delivering to</h3>
                  <button onClick={() => setStep(2)} className='text-xs text-emerald-600 hover:text-emerald-700 font-bold bg-emerald-100/50 px-3 py-1 rounded-md'>Change</button>
                </div>
                <p className='text-sm text-emerald-950 font-bold'>{address.name}</p>
                <p className='text-sm text-emerald-800 font-medium mt-0.5'>{address.address_line}</p>
                <p className='text-sm text-emerald-800 font-medium'>{address.city}, {address.state} - {address.pincode}</p>
                <p className='text-sm text-emerald-800 font-medium'>Phone: {address.mobile}</p>
              </div>

              {/* Items summary */}
              <div className='border border-slate-100 rounded-xl p-4'>
                <h3 className='font-semibold text-slate-800 text-sm mb-3'>{totalQty} Items</h3>
                <div className='grid gap-2'>
                  {cartItemsList.map((item) => (
                    <div key={item._id} className='flex justify-between text-sm'>
                      <span className='text-slate-600 line-clamp-1 flex-1'>{item?.productId?.name} x{item?.quantity}</span>
                      <span className='text-slate-800 font-medium ml-4'>
                        {DisplayPriceInRupees(pricewithDiscount(item?.productId?.price, item?.productId?.discount) * item?.quantity)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Price summary */}
              <div className='border border-slate-100 rounded-xl p-4'>
                <div className='flex justify-between text-sm text-slate-500'>
                  <span>Items Total</span>
                  <span>{DisplayPriceInRupees(notDiscountTotalPrice)}</span>
                </div>
                <div className='flex justify-between text-sm text-emerald-600 mt-1'>
                  <span>Discount</span>
                  <span>- {DisplayPriceInRupees(notDiscountTotalPrice - totalPrice)}</span>
                </div>
                <div className='flex justify-between text-sm text-slate-500 mt-1'>
                  <span>Delivery</span>
                  <span className='text-emerald-600'>Free</span>
                </div>
                <div className='flex justify-between font-bold text-slate-800 mt-2 pt-2 border-t border-slate-200 text-lg'>
                  <span>Total</span>
                  <span>{DisplayPriceInRupees(totalPrice)}</span>
                </div>
              </div>

              {/* Payment method */}
              <div className='bg-emerald-50 rounded-xl p-4 flex items-center gap-3'>
                <div className='w-10 h-10 rounded-full bg-emerald-100 flex items-center justify-center'>
                  <span className='text-lg'>💵</span>
                </div>
                <div>
                  <p className='font-semibold text-emerald-900 text-sm'>Cash on Delivery</p>
                  <p className='text-xs text-emerald-700'>Pay when your order arrives</p>
                </div>
              </div>
            </div>

            <div className='p-6 flex gap-4 bg-slate-50/50 border-t border-slate-100'>
              <button onClick={() => setStep(2)}
                className='flex-1 py-4 bg-white border border-slate-200 text-slate-700 font-bold rounded-xl hover:bg-slate-50 transition-colors shadow-sm'>
                Back
              </button>
              <button onClick={handlePlaceOrder} disabled={loading}
                className='btn-premium flex-1 py-4 bg-emerald-600 hover:bg-emerald-500 text-white font-extrabold rounded-xl transition-all shadow-lg shadow-emerald-500/20 disabled:opacity-50 text-lg'>
                {loading ? 'Placing Order...' : 'Place Order'}
              </button>
            </div>
          </div>
        )}
      </div>
    </section>
  )
}

export default CheckoutPage
