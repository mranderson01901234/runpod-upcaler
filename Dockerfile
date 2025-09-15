FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel

WORKDIR /app

ENV CUDA_HOME=/usr/local/cuda
ENV PATH=${CUDA_HOME}/bin:${PATH}
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64:${LD_LIBRARY_PATH}

RUN apt-get update && apt-get install -y git wget curl libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 && rm -rf /var/lib/apt/lists/*

RUN pip uninstall -y torch torchvision torchaudio
RUN pip install --no-cache-dir torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cu121

RUN pip install --no-cache-dir diffusers transformers accelerate runpod pillow numpy
RUN pip install --no-cache-dir xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121

RUN git clone https://github.com/zsyOAOA/InvSR.git
WORKDIR /app/InvSR
RUN pip install -e ".[torch]" && pip install -r requirements.txt

COPY runpod_handler.py /app/
WORKDIR /app

RUN python -c "import torch; print('PyTorch version:', torch.__version__); print('CUDA available:', torch.cuda.is_available())"

CMD ["python", "runpod_handler.py"]
