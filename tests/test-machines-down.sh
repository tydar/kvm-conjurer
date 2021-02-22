#!/bin/bash

sudo virsh destroy test1
sudo virsh destroy test2
sudo virsh undefine test1
sudo virsh undefine test2

rm -f test1.qcow2
rm -f test2.qcow2
