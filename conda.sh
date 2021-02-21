#! /bin/bash

export PATH=/usr/local/cuda/bin/:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:$LD_LIBRARY_PATH
apt install -y libgl1-mesa-glx libglib2.0-0 libsm6 libxext6
apt install -y libxrender-dev libyaml-dev
python setup.py build develop
python scripts/demo_inference.py --cfg configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml --checkpoint pretrained_models/fast_res50_256x192.pth --indir examples/demo/ --save_img