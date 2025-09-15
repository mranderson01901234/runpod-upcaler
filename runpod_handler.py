import runpod
import os
import base64
import subprocess

def handler(event):
    try:
        input_data = event.get("input", {})
        
        if "image" not in input_data:
            return {"error": "No image provided"}
        
        # Test PyTorch first
        try:
            import torch
            if not torch.cuda.is_available():
                return {"status": "error", "message": "CUDA not available in PyTorch"}
        except ImportError:
            return {"status": "error", "message": "PyTorch import failed"}
        
        # Decode and save image
        image_bytes = base64.b64decode(input_data["image"])
        with open("/tmp/input.jpg", "wb") as f:
            f.write(image_bytes)
        
        # Get quality settings
        quality_mode = input_data.get("quality_mode", "standard")
        num_steps = 1 if quality_mode == "fast" else 3
        chopping_size = 128 if quality_mode == "fast" else 256
        
        # Change to InvSR directory
        os.chdir("/app/InvSR")
        
        # Run InvSR
        cmd = [
            "python", "inference_invsr.py",
            "-i", "/tmp/input.jpg", 
            "-o", "/tmp/",
            "--num_steps", str(num_steps),
            "--chopping_size", str(chopping_size),
            "--chopping_bs", "1"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Look for output file
            output_files = [f for f in os.listdir("/tmp/") if f.startswith("input") and f.endswith((".jpg", ".png"))]
            
            if output_files:
                output_path = f"/tmp/{output_files[0]}"
                with open(output_path, "rb") as f:
                    enhanced_data = base64.b64encode(f.read()).decode()
                
                return {
                    "status": "success",
                    "enhanced_image": enhanced_data,
                    "quality_mode": quality_mode
                }
            else:
                return {"status": "error", "message": "No output file generated"}
        else:
            return {
                "status": "error", 
                "message": f"InvSR failed: {result.stderr}",
                "stdout": result.stdout
            }
            
    except Exception as e:
        return {"status": "error", "message": str(e)}

runpod.serverless.start({"handler": handler})
