#!/bin/bash

CLI_PATH=/usr/local/bin/simple_switch_CLI

bytes_s1h2=0
pre_bytes_s1h2=0

#get current unix time in milliseconds
prev_time=`date +%s%N | cut -b1-13`


while true; do
  bytes_s1h2=`echo counter_read egressPortCounter 2 | $CLI_PATH --thrift-port 9090 | grep egressPortCounter | tr '=' ' ' | tr ')' ' ' | awk '{print $6}'`       

  now=`date +%s%N | cut -b1-13` 
 
  if [ ! $pre_bytes_s1h2 -eq 0 ];then
     thr=`echo "scale=2;($bytes_s1h2-$pre_bytes_s1h2) * 8.0  / ($now-$pre_time)" | bc -l`
     echo "BW consumption (s1-h2):" $thr "kbps"      
  fi


  
  echo $thr >temp
  read $thr <temp
  echo "BW consumption (s1-h2):" $thr "kbps" 

  echo $bytes_s1h2 >temp2
  read $bytes_s1h2 <temp2
  echo $bytes_s1h2 
  
  pre_bytes_s1h2=$bytes_s1h2
  pre_time=$now
  sleep 1
done