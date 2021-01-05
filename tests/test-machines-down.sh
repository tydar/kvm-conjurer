#!/bin/bash

virsh destroy test1
virsh destroy test2
virsh undefine test1
virsh undefine test2

rm -f test1.qcow2
rm -f test2.qcow2
