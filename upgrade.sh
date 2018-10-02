#!/bin/bash

# Super simple script to update all packages

for package in $(pip list --outdated)
do
	pip install -U $package
done
