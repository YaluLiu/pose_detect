from pytorch/pytorch:1.1.0-cuda10.0-cudnn7.5-runtime

RUN conda install torchvision==0.3.0 cudatoolkit=10.0 -c pytorch
    && pip install torchvision==0.3.0+cu100 -f https://download.pytorch.org/whl/torch_stable.html
    && pip install -r requirements.txt
    && apt update && apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6 libxrender-dev libyaml-dev