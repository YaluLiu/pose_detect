set -x

# Stable parameter
CONFIG="configs/coco/resnet/256x192_res50_lr1e-3_1x.yaml"
CKPT="pretrained_models/fast_res50_256x192.pth"


# input 
IMAGE="examples/demo/cross.jpg"
WEBCAM="examples/video/throw.mp4"

# detect interval,detect every N frames,only work on webcam-mode
GAP=2

# post json(detect result) to server interface
HOST="192.168.200.246"
PORT="7010"
API_IMAGE="api_show_image"
API_INFO="api_show_info"

function post_image() {
    SERVER="http://${HOST}:${PORT}/${API_IMAGE}"
    python scripts/demo_inference.py \
        --cfg ${CONFIG} \
        --checkpoint ${CKPT} \
        --image ${IMAGE} \
        --server ${SERVER} \
        --post_image
}

function post_webcam() {
    SERVER="http://${HOST}:${PORT}/${API_IMAGE}"
    python scripts/demo_inference.py \
        --cfg ${CONFIG} \
        --checkpoint ${CKPT} \
        --webcam ${WEBCAM} \
        --gap ${GAP} \
        --server ${SERVER} \
        --post_image
}

function image() {
    python scripts/demo_inference.py \
        --cfg ${CONFIG} \
        --checkpoint ${CKPT} \
        --image ${IMAGE} \
        --save_img
}

function webcam() {
    SERVER="http://${HOST}:${PORT}/${API_INFO}"
    python scripts/demo_inference.py \
        --cfg ${CONFIG} \
        --checkpoint ${CKPT} \
        --webcam ${WEBCAM} \
        --gap ${GAP} \
        --server ${SERVER}
}

function test_simple_pose() {
    INDIR="examples/simple_pose/"
    python scripts/demo_inference.py \
        --cfg ${CONFIG} \
        --checkpoint ${CKPT} \
        --indir ${INDIR} \
        --save_img
}

function main() {
    if [ $1 == "image" ]; then
        image
    elif [ $1 == "post_image" ]; then
        post_image
    elif [ $1 == "webcam" ]; then
        webcam
    elif [ $1 == "post_webcam" ]; then
        post_webcam
    fi
}

main "$@"