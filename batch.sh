#!/usr/bin/env bash

for config in configs/*; do
  echo "Running $config"
  python3 ./forum-driver.py "$config"
done