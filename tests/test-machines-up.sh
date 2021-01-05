#!/bin/bash

## Step 1: Obtain (or detect cached) .qcow2 base image

test -f images/debian10.qcow2 || wget -O images/debian10.qcow2 https://cloud.debian.org/images/cloud/buster/20201214-484/debian-10-generic-amd64-20201214-484.qcow2

## Step 2. Create .qcow2 with backing image debian10.qcow2

qemu-img create -f qcow2 -F qcow2 -o backing_file=images/debian10.qcow2 test1.qcow2
qemu-img create -f qcow2 -F qcow2 -o backing_file=images/debian10.qcow2 test2.qcow2

## Step 3: Create .img with cloud-init configuration

cloud-localds -v test-seed1.img cloud-init.cfg
cloud-localds -v test-seed2.img cloud-init.cfg

virt-install --name test1 \
    --memory 1000 --vcpus 1 \
    --boot hd,menu=on \
    --disk path=test-seed1.img,device=cdrom \
    --disk path=test1.qcow2,device=disk \
    --graphics none \
    --noautoconsole \
    --network network:default \
    --os-type=linux --os-variant=debian10

virt-install --name test2 \
    --memory 1000 --vcpus 1 \
    --boot hd,menu=on \
    --disk path=test-seed2.img,device=cdrom \
    --disk path=test2.qcow2,device=disk \
    --graphics none \
    --noautoconsole \
    --network network:default \
    --os-type=linux --os-variant=debian10