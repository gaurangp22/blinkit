import React from 'react'
import { useForm } from "react-hook-form"
import Axios from '../utils/Axios'
import SummaryApi from '../common/SummaryApi'
import toast from 'react-hot-toast'
import AxiosToastError from '../utils/AxiosToastError'
import { IoClose } from "react-icons/io5";
import { useGlobalContext } from '../provider/GlobalProvider'

const AddAddress = ({close}) => {
    const { register, handleSubmit, reset, watch, setValue } = useForm()
    const { fetchAddress } = useGlobalContext()
    const [countryCode, setCountryCode] = useState('+91')

    const pincode = watch("pincode")

    React.useEffect(() => {
        if (pincode && pincode.length === 6 && /^\d{6}$/.test(pincode)) {
            const fetchCityState = async () => {
                try {
                    const res = await fetch(`https://api.postalpincode.in/pincode/${pincode}`);
                    const data = await res.json();
                    if (data && data[0] && data[0].Status === 'Success') {
                        const details = data[0].PostOffice[0];
                        setValue("city", details.District);
                        setValue("state", details.State);
                        setValue("country", "India");
                        toast.success("City and State auto-filled!");
                    }
                } catch (error) {
                    console.error("Failed to fetch pincode details", error);
                }
            };
            fetchCityState();
        }
    }, [pincode, setValue]);

    const onSubmit = async(data)=>{
        console.log("data",data)
    
        try {
            const response = await Axios({
                ...SummaryApi.createAddress,
                data : {
                    address_line :data.addressline,
                    city : data.city,
                    state : data.state,
                    country : data.country,
                    pincode : data.pincode,
                    mobile : `${countryCode} ${data.mobile}`
                }
            })

            const { data : responseData } = response
            
            if(responseData.success){
                toast.success(responseData.message)
                if(close){
                    close()
                    reset()
                    fetchAddress()
                }
            }
        } catch (error) {
            AxiosToastError(error)
        }
    }
  return (
    <section className='bg-black fixed top-0 left-0 right-0 bottom-0 z-50 bg-opacity-70 h-screen overflow-auto'>
        <div className='bg-white p-4 w-full max-w-lg mt-8 mx-auto rounded'>
            <div className='flex justify-between items-center gap-4'>
                <h2 className='font-semibold'>Add Address</h2>
                <button onClick={close} className='hover:text-red-500'>
                    <IoClose  size={25}/>
                </button>
            </div>
            <form className='mt-4 grid gap-4' onSubmit={handleSubmit(onSubmit)}>
                <div className='grid gap-1'>
                    <label htmlFor='addressline'>Address Line :</label>
                    <input
                        type='text'
                        id='addressline' 
                        className='border bg-blue-50 p-2 rounded'
                        {...register("addressline",{required : true})}
                    />
                </div>
                <div className='grid gap-1'>
                    <label htmlFor='city'>City :</label>
                    <input
                        type='text'
                        id='city' 
                        className='border bg-blue-50 p-2 rounded'
                        {...register("city",{required : true})}
                    />
                </div>
                <div className='grid gap-1'>
                    <label htmlFor='state'>State :</label>
                    <input
                        type='text'
                        id='state' 
                        className='border bg-blue-50 p-2 rounded'
                        {...register("state",{required : true})}
                    />
                </div>
                <div className='grid gap-1'>
                    <label htmlFor='pincode'>Pincode :</label>
                    <input
                        type='text'
                        id='pincode' 
                        className='border bg-blue-50 p-2 rounded'
                        {...register("pincode",{required : true})}
                    />
                </div>
                <div className='grid gap-1'>
                    <label htmlFor='country'>Country :</label>
                    <input
                        type='text'
                        id='country' 
                        className='border bg-blue-50 p-2 rounded'
                        {...register("country",{required : true})}
                    />
                </div>
                <div className='grid gap-1'>
                    <label htmlFor='mobile'>Mobile No. :</label>
                    <div className='flex gap-2'>
                        <select 
                            value={countryCode} 
                            onChange={(e) => setCountryCode(e.target.value)}
                            className='border bg-blue-50 p-2 rounded w-28 outline-none'
                        >
                            <option value="+91">+91 (IN)</option>
                            <option value="+1">+1 (US)</option>
                            <option value="+44">+44 (UK)</option>
                            <option value="+61">+61 (AU)</option>
                            <option value="+971">+971 (UAE)</option>
                        </select>
                        <input
                            type='text'
                            id='mobile' 
                            className='border bg-blue-50 p-2 rounded flex-1'
                            {...register("mobile",{required : true})}
                        />
                    </div>
                </div>

                <button type='submit' className='bg-primary-200 w-full  py-2 font-semibold mt-4 hover:bg-primary-100'>Submit</button>
            </form>
        </div>
    </section>
  )
}

export default AddAddress
