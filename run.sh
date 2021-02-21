#! /bin/bash

project_dir=$(cd "$(dirname "$0")";pwd)
volume_dir="/workspace"
dev_image="step_2_build"
run_image="alphapose_runtime"
container_name="alphapose"

function build_dev() {
    sudo docker run -dt --name alphapose_dev  -v ${project_dir}:${volume_dir} ${dev_image}
    sudo docker exec -it alphapose_dev bash
    python setup.py build develop
}

function clean() {
    sudo docker stop ${container_name}
    sudo docker rm ${container_name}
}

function run() {
    sudo docker run -dt --name ${container_name}  -v ${project_dir}:${volume_dir} ${run_image}
    sudo docker start ${container_name}
    sudo docker exec -it ${container_name} bash
}

function main() {
    if [ $# != 1 ] ; then
        echo "param:build or clean"
    elif [ $1 == "build" ]; then
        build_dev
    elif [ $1 == "run" ]; then
        run
    elif [ $1 == "clean" ]; then
        clean
    fi
}

main "$@"


