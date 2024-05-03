ARG CUDA_VERSION="12.1.1"
ARG OS="ubuntu22.04"

ARG CUDA_BUILDER_IMAGE="${CUDA_VERSION}-devel-${OS}"
ARG CUDA_RUNTIME_IMAGE="${CUDA_VERSION}-runtime-${OS}"
FROM nvidia/cuda:${CUDA_BUILDER_IMAGE} as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y git build-essential \
    python3 python3-pip python3-venv gcc wget \
    ocl-icd-opencl-dev opencl-headers clinfo \
    libclblast-dev libopenblas-dev \
    && mkdir -p /etc/OpenCL/vendors && echo "libnvidia-opencl.so.1" > /etc/OpenCL/vendors/nvidia.icd

# 
WORKDIR /code

COPY . .

# setting build related env vars
ENV CUDA_DOCKER_ARCH=all
ENV LLAMA_CUBLAS=1


# Install depencencies
ENV VIRTUAL_ENV=venv
RUN python3 -m pip install --upgrade pip
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH=$VIRTUAL_ENV/bin:$PATH

# Install PyTorch and torchvision
RUN pip install torch --index-url https://download.pytorch.org/whl/cu121

# Install depencencies
RUN pip install transformers tqdm scikit-learn scipy nltk numpy sentencepiece langChain chromadb fastapi uvicorn sentence-transformers
# RUN pip install --no-deps sentence-transformers 
# Install llama-cpp-python (build with cuda)
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python

FROM nvidia/cuda:${CUDA_RUNTIME_IMAGE} as runtime

# We need to set the host to 0.0.0.0 to allow outside access
ENV HOST 0.0.0.0
ENV CUDA_DOCKER_ARCH=all

RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3 python3-pip python3-venv

WORKDIR /code

ENV VIRTUAL_ENV=venv
COPY --from=builder /code/venv venv
ENV PATH=$VIRTUAL_ENV/bin:$PATH
COPY ./app /code/app

# Now uvicorn should be found since it's installed in the virtual environment
# CMD ["python3", "app/test.py", "--host", "0.0.0.0", "--port", "80"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
# CMD python3 -m uvicorn app.main:app --host 0.0.0.0 --port 80