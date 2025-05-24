from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import Optional

@app.post("/api/hide")
async def hide_data(
    method: str = Form(...),  # "DWT", "LSB", or "DCT"
    image: UploadFile = File(...),
    secret_text: str = Form(...),
):
    try:
        # Save uploaded image
        temp_image = f"temp_{image.filename}"
        with open(temp_image, "wb") as buffer:
            buffer.write(await image.read())
        
        # Call the selected method
        if method == "DWT":
            from services.dwt_steganography_service import embed_data
            output_path = "output_dwt.png"
            embed_data(temp_image, secret_text, output_path)
        elif method == "LSB":
            from services.lsb_steganography_service import hide_data
            output_path = "output_lsb.png"
            hide_data(temp_image, secret_text, output_path)
     
        else:
            raise HTTPException(status_code=400, detail="Invalid method")
        
        return {
            "status": "success",
            "output_path": output_path,
            "method_used": method
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    