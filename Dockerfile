FROM pytorch/pytorch:2.4.0-cuda12.1-cudnn9-devel

WORKDIR /app

RUN apt-get update && apt-get install -y git wget curl && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cu121
RUN pip install --no-cache-dir xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121
RUN pip install --no-cache-dir diffusers transformers accelerate runpod pillow numpy

RUN git clone https://github.com/zsyOAOA/InvSR.git
WORKDIR /app/InvSR
RUN pip install -e ".[torch]" && pip install -r requirements.txt

COPY runpod_handler.py /app/
WORKDIR /app

CMD ["python", "runpod_handler.py"]
