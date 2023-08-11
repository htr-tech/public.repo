#!/bin/bash

# Go executable binary builder

if [ -z "$1" ]; then
	echo "Usage: $0 <script>"
	exit 1
fi

TARGET_OS=("linux" "windows")
TARGET_ARCH=("amd64" "386" "arm" "arm64")

for os in "${TARGET_OS[@]}"; do
	for arch in "${TARGET_ARCH[@]}"; do
		OUTPUT="${1%.go}_${os}_${arch}"

		[ "$os" == "windows" ] && OUTPUT="${OUTPUT}.exe"

		echo -n "Building binary for $os $arch... "
		GOOS="$os" GOARCH="$arch" go build -ldflags="-s -w" -buildmode=pie -trimpath -o "$OUTPUT" "$1"
		echo "[done]"
	done
done

# -a -gcflags=all="-l -B"
