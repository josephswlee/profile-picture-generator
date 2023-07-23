/*
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ],
  }
  ```
*/
import { PhotoIcon, UserCircleIcon } from '@heroicons/react/24/solid'

import React, { useState } from 'react';
import { Element } from 'react-scroll';

export default function Form() {
  // Use state to manage the form data
  const [positiveData, setPositiveData] = useState('');
  const [negativeData, setNegativeData] = useState('');
  const [imageUrl, setImageUrl] = useState(''); // State for the image preview URL

  // Function to handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();

    // Rest of your form submission code...
    // Use positiveData and negativeData to fetch data and update the resultImageDiv accordingly.
        
        fetch('http://localhost:5000/generate', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
            'positivePrompts': positiveData, 
            'negativePrompts': negativeData
            })
        })
        .then(response => response.blob())
        .then(blob => {
            // const url = URL.createObjectURL(blob);
            // setImageUrl(url); // Update the imageUrl state with the new image URL
            // Convert the response blob to a base64 data URL
            const reader = new FileReader();
            reader.onloadend = () => {
              setImageUrl(reader.result);
            };
            reader.readAsDataURL(blob);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };

  return (
    <Element name="formSection">
      <div className="mx-auto max-w-screen-xl px-4 py-16 sm:px-6 lg:px-8">
    <div className="mx-auto max-w-lg">
        <h1 className="text-2xl font-bold sm:text-3xl">Try it!</h1>

        <p className="mt-4 text-gray-500">
        Add positive prompts for how the image should looks like and negative prompts for the stuff you want to avoid.
        </p>
    </div>

    <form id="generateForm" onSubmit={handleSubmit}>
      <div className="space-y-12">
        <div className="border-b border-gray-900/10 pb-12">
          {/* <h2 className="text-base font-semibold leading-7 text-gray-900">Profile</h2>
          <p className="mt-1 text-sm leading-6 text-gray-600">
            This information will be displayed publicly so be careful what you share.
          </p> */}

          <div className="mt-10 grid grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
            <div className="sm:col-span-3">
                <label htmlFor="positive-prompts" className="block text-sm font-medium leading-6 text-gray-900">
                Positive Prompts
                </label>
                <div className="mt-2">
                <textarea
                    id="positive-prompts"
                    name="positive-prompts"
                    rows={3}
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    value={positiveData} // Bind the value to state
                    onChange={(event) => setPositiveData(event.target.value)} // Update the state when the value changes
                    placeholder="Add positive prompts"
                />
                </div>
            </div>
            <div className="sm:col-span-3">
                <label htmlFor="negative-prompts" className="block text-sm font-medium leading-6 text-gray-900">
                Negative Prompts
                </label>
                <div className="mt-2">
                <textarea
                    id="negative-prompts"
                    name="negative-prompts"
                    rows={3}
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    value={negativeData} // Bind the value to state
                    onChange={(event) => setNegativeData(event.target.value)} // Update the state when the value changes
                    placeholder="Add positive prompts"
                />
                </div>
            </div>

            <div className="sm:col-span-2">
              <label htmlFor="cover-photo" className="block text-sm font-medium leading-6 text-gray-900">
                Upload your photo
              </label>
              <div className="mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-10">
                <div className="text-center">
                  <PhotoIcon className="mx-auto h-12 w-12 text-gray-300" aria-hidden="true" />
                  <div className="mt-4 flex text-sm leading-6 text-gray-600">
                    <label
                      htmlFor="file-upload"
                      className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500"
                    >
                      <span>Upload a file</span>
                      <input id="file-upload" name="file-upload" type="file" className="sr-only" />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs leading-5 text-gray-600">PNG, JPG, GIF up to 10MB</p>
                </div>
              </div>
            </div>
            <div className="sm:col-span-1 mt-2 flex items-center justify-center gap-x-6">
                <button
                type="submit"
                className="rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                >
                Generate
                </button>
            </div>
            <div className="sm:col-span-3 mt-2 flex justify-center rounded-lg border border-dashed border-gray-900/25 px-6 py-0" style={{ height: '400px' }}>
                <div className="text-center flex flex-col items-center justify-center">
                {imageUrl ? (
                    // Image preview when imageUrl is not empty
                    <div style={{ width: '100%', height: '100%' }}>
                    <img
                        src={imageUrl}
                        alt="Result Image"
                        style={{ objectFit: 'cover', maxWidth: '100%', maxHeight: '100%' }}
                    />
                    </div>
                ) : (
                    // Label and icon when imageUrl is empty
                    <div>
                    <PhotoIcon className="mx-auto h-12 w-12 text-gray-300" aria-hidden="true" />
                    <div className="mt-4 flex text-sm leading-6 text-gray-600">
                        <label
                        htmlFor="image-preview"
                        className="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500"
                        >
                        <span>Image Preview</span>
                        </label>
                    </div>
                    </div>
                )}
                </div>
            </div>
            
        </div>
        </div>
      </div>     
    </form>   
    </div>
    </Element>
    
  );
}
