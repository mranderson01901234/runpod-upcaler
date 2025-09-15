import runpod
import os
import base64
import subprocess

def handler(event):
    try:
        input_data = event.get("input", {})
        
        if "image" not in input_data:
            return {"error": "No image provided"}
        
        # Decode and save image
        image_bytes = base64.b64decode(input_data["image"])
        with open("/tmp/input.jpg", "wb") as f:
            f.write(image_bytes)
        
        # Get quality settings
        quality_mode = input_data.get("quality_mode", "standard")
        num_steps = 1 if quality_mode == "fast" else 3
        chopping_size = 128 if quality_mode == "fast" else 256
        
        # Run InvSR
        cmd = [
            "python", "/app/InvSR/inference_invsr.py",
            "-i", "/tmp/input.jpg",
            "-o", "/tmp/",
            "--num_steps", str(num_steps),
            "--chopping_size", str(chopping_size),
            "--chopping_bs", "1"
        ]
        
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        
        if result.returncode == 0:
            with open("/tmp/input_enhanced.jpg", "rb") as f:
                enhanced_data = base64.b64encode(f.read()).decode()
            
            return {
                "status": "success",
                "enhanced_image": enhanced_data,
                "quality_mode": quality_mode
            }
        else:
            return {"status": "error", "message": "Enhancement failed"}
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

runpod.serverless.start({"handler": handler})
