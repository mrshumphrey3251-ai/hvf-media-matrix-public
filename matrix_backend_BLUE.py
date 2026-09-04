import os
import random
from fastapi import FastAPI, Header, HTTPException
from PIL import Image, ImageDraw
import openvino_genai as ov_genai

app = FastAPI(title="HVF Media Matrix API")
REPO_DIR = os.path.abspath(r"C:\HVF_Repos\hvf-media-matrix-private")
MODEL_ID = os.path.join(REPO_DIR, "sovereign_ir_model")

native_pipe = None

def apply_executive_compositor(base_img: Image.Image) -> Image.Image:
    img = base_img.convert("RGBA")
    width, height = img.size
    
    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)
    
    # 1. TOP BANNER
    banner_height = 60
    draw.rectangle([(0, 0), (width, banner_height)], fill=(10, 15, 26, 220))
    draw.line([(0, banner_height), (width, banner_height)], fill=(0, 230, 255, 255), width=2)
    draw.text((width // 2, 20), "PROJECT EBONY", fill=(255, 255, 255, 255), anchor="mm")
    draw.text((width // 2, 42), "STRATEGIC JOINT VENTURE MERGER", fill=(0, 230, 255, 255), anchor="mm")
    
    # 2. BOTTOM ATTRIBUTION FOOTER
    footer_height = 80
    footer_top = height - footer_height
    draw.rectangle([(0, footer_top), (width, height)], fill=(10, 15, 26, 230))
    draw.line([(0, footer_top), (width, footer_top)], fill=(0, 230, 255, 255), width=2)
    draw.line([(width // 2, footer_top + 10), (width // 2, height - 10)], fill=(70, 80, 100, 255), width=1)
    
    # Left Attribution
    draw.text((20, footer_top + 18), "HUMPHREY VIRTUAL FARMS", fill=(255, 255, 255, 255))
    draw.text((20, footer_top + 38), "52% Majority Owner | Sovereign AI Core", fill=(0, 255, 170, 255))
    draw.text((20, footer_top + 55), "Agronomy & Edge Telemetry Governance", fill=(180, 190, 205, 255))
    
    # Right Attribution
    draw.text((width - 20, footer_top + 18), "SIGNALLINK PROTOCOL", fill=(255, 255, 255, 255), anchor="ra")
    draw.text((width - 20, footer_top + 38), "48% Minority Partner | WebRTC Core", fill=(140, 180, 255, 255), anchor="ra")
    draw.text((width - 20, footer_top + 55), "Communications Infrastructure", fill=(180, 190, 205, 255), anchor="ra")
    
    composed = Image.alpha_composite(img, overlay)
    return composed.convert("RGB")

@app.post("/synthesis/image")
def generate_image(prompt: str, x_auth_token: str = Header(None)):
    global native_pipe
    if x_auth_token != "CEO_OVERRIDE":
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    if native_pipe is None:
        try:
            print("[HVF NEURAL CORE] Igniting bare-metal OpenVINO GenAI pipeline...")
            native_pipe = ov_genai.Text2ImagePipeline(MODEL_ID, "AUTO")
        except Exception as e:
            return {"status": "ERROR", "message": f"Native Core Fault: {str(e)}", "image_path": ""}
    
    try:
        output_filename = "generated_asset.png"
        output_path = os.path.join(REPO_DIR, output_filename)
        
        # UI prompt is now passed directly to the engine
        enhanced_prompt = f"{prompt}, 8k resolution, highly detailed, professional photography, sharp focus"
        
        print("[HVF NEURAL CORE] Synthesizing visual plate...")
        image_tensor = native_pipe.generate(
            enhanced_prompt,
            num_inference_steps=5,
            guidance_scale=1.5,
            width=512,
            height=512
        )
        
        raw_image = Image.fromarray(image_tensor.data[0])
        final_asset = apply_executive_compositor(raw_image)
        final_asset.save(output_path)
        
        return {
            "status": "SUCCESS",
            "message": "Executive Asset synthesized and Compositor Banner applied.",
            "image_path": output_filename
        }
    except Exception as e:
        return {"status": "ERROR", "message": f"Generation Fault: {str(e)}", "image_path": ""}
