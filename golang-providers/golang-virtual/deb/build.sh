#!/bin/bash

# Internal variables
PELION_PACKAGE_NAME="golang-virtual"
PELION_PACKAGE_DIR=$(cd "`dirname \"$0\"`" && pwd)

source "$PELION_PACKAGE_DIR"/../../../build-env/inc/build-common.sh

PELION_PACKAGE_PRE_BUILD_CALLBACK=cache_golang_packages

function cache_golang_packages() {
    echo "Caching golang-14 in local repository"
    local OUTPUT_DIR="$ROOT_DIR"/build/apt/$DOCKER_DIST/pe-dependencies/

    mkdir -p $OUTPUT_DIR
    cd $OUTPUT_DIR

    for((i=0; i<5; i++)); do
        if apt-get -y download golang-1.14 golang-1.14-go golang-1.14-src; then
            break;
        else
            if [ $i == 4 ]; then
                echo "Unable to get golang from external repository"
                false
            fi

            echo "Retrying..."
        fi
    done
    cd -
}

pelion_metapackage_main "$@"
