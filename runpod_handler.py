import runpod
import os
import subprocess

def handler(event):
    try:
        print("=== DEBUG INFO ===")
        print(f"Current directory: {os.getcwd()}")
        print(f"Contents of /app: {os.listdir('/app')}")
        
        # Check if InvSR exists
        invsr_path = "/app/InvSR"
        if os.path.exists(invsr_path):
            print(f"InvSR directory exists")
            print(f"InvSR contents: {os.listdir(invsr_path)}")
            
            # Check if inference script exists
            inference_script = f"{invsr_path}/inference_invsr.py"
            if os.path.exists(inference_script):
                print("inference_invsr.py found")
                
                # Try running Python --version
                result = subprocess.run(["python", "--version"], capture_output=True, text=True)
                print(f"Python version: {result.stdout}")
                
                # Try importing basic modules
                test_cmd = ["python", "-c", "import torch; print('PyTorch version:', torch.__version__)"]
                result = subprocess.run(test_cmd, capture_output=True, text=True)
                print(f"PyTorch test: {result.stdout}")
                print(f"PyTorch errors: {result.stderr}")
                
                return {
                    "status": "debug_success",
                    "message": "Container working, InvSR found",
                    "details": {
                        "invsr_exists": True,
                        "pytorch_working": "torch" in result.stdout
                    }
                }
            else:
                return {"status": "error", "message": "inference_invsr.py not found"}
        else:
            return {"status": "error", "message": "InvSR directory not found"}
            
    except Exception as e:
        return {"status": "error", "message": f"Debug failed: {str(e)}"}

runpod.serverless.start({"handler": handler})
