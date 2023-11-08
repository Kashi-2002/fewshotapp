import { writeFileSync } from 'fs';
import { fail } from '@sveltejs/kit';
import express from "express";

// export const actions = {
//   default: async ({ request }) => {
//     const formData = Object.fromEntries(await request.formData());
//     const { fileToUploads } = formData as { fileToUploads: File };
    
//     // Write the file to the static folder

//     if (
//         !(formData.fileToUploads as File).name ||
//         (formData.fileToUploads as File).name === 'undefined'
//       ) {
       
//         return fail(400, {
//           error: true,
//           message: 'You must provide a file to upload'
//         });
//       }
  


//     writeFileSync(`static/samples/${fileToUploads.name}`, Buffer.from(await fileToUploads.arrayBuffer()));
    
//     return {
//       success: true
//     };
//   }
// }
export const actions = {
    default: async ({ request }) => {
      const formData = Object.fromEntries(await request.formData());
  
      if ('fileToUploads' in formData) {
        // Handle the 'fileToUploads' submit button
        const { fileToUploads } = formData as { fileToUploads: File };
  
        if (!fileToUploads.name || fileToUploads.name === 'undefined') {
          return fail(400, {
            error: true,
            message: 'You must provide a file to upload'
          });
        }
  
        writeFileSync(`static/samples/${fileToUploads.name}`, Buffer.from(await fileToUploads.arrayBuffer()));
  
        return {
          success: true
        };
      } else if ('fileToUpload' in formData) {
        // Handle the 'fileToUpload' submit button
        const { fileToUpload } = formData as { fileToUpload: File };
  
        if (!fileToUpload.name || fileToUpload.name === 'undefined') {
          return fail(400, {
            error: true,
            message: 'You must provide a file to upload'
          });
        }
  
        writeFileSync(`static/query/${fileToUpload.name}`, Buffer.from(await fileToUpload.arrayBuffer()));
  
        return {
          success: true
        };
      } else {
        // Handle the case when neither button is pressed
        return fail(400, {
          error: true,
          message: 'Invalid request'
        });
      }
    }
  }
  