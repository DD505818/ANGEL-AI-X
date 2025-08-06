#!/usr/bin/env bash
printf "Synthetic latency test...\n"
start=$(date +%s%N)
sleep 0.00005   # 50µs
end=$(date +%s%N)
echo "Latency: $(( (end-start)/1000 )) µs"
