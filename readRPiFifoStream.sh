#!/bin/bash

if [ -p fifo264 ]
then
rm fifo264
fi
mkfifo fifo264

