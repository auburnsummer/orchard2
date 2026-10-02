#!/bin/bash

# Base URL for downloads
BASE_URL="https://pub-35aaba1d303a4c5da33a0967816cd58a.r2.dev/vitals"

# Change to the script's directory
cd "$(dirname "$0")"

# Array of files to download
FILES=(
    "auburnsummer_-_Triplet_Testaaaaa1.rdzip"
    "onething.rdzip"
    "bdf3cf10799f4309ecea59f37f1fdba2538f5.rdzip"
    "yi-xiao-Hg3afme47nr.rdzip"
    "swing-c2QGYcw8GLq.rdzip"
    "sol-e-ma-dVMtiNt856v.rdzip"
    "Samario_Making_A_Mistake_-_One_Uncued_Tresillo2.rdzip"
    "rgb-7krFijAGF4D.rdzip"
    "pull-EpgEYcGYPnU.rdzip"
    "one-uncu-eqSkB1ZX7Xz.rdzip"
    "one-forg-NqVywpSrZs1.rdzip"
    "know-you-2zRJRCjPqJx.rdzip"
    "jimmy-s-Ccby1RK3XJK.rdzip"
    "ennui-og-3VFE7LSmzSo.rdzip"
    "banas-QbMoyaG2nfK.rdzip"
)

# Download each file
for file in "${FILES[@]}"; do
    echo "Downloading $file..."
    curl -L -O "$BASE_URL/$file"
done

echo "All downloads completed!"