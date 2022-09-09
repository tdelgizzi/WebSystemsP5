#!/bin/bash
#
# Example of how to chain mapreduce jobs together.  The output of one
# job is the input to the next.
#
# Hadoop options
# jar index/hadoop/hadoop-streaming-2.7.2.jar   # Hadoop configuration
# -input <directory>                            # Input directory
# -output <directory>                           # Output directory
# -mapper <exec_name>                           # Mapper executable
# -reducer <exec_name>                          # Reducer executable

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

rm -rf output0

# Run first MapReduce job
hadoop \
  jar ../hadoop-streaming-2.7.2.jar \
  -input input \
  -output output0 \
  -mapper ./map0.py \
  -reducer ./reduce0.py \

# Remove first output directory, if it exists
rm -rf output0
rm -rf output1

# Run first MapReduce job
hadoop \
  jar ../hadoop-streaming-2.7.2.jar \
  -input input \
  -output output1 \
  -mapper ./map1.py \
  -reducer ./reduce1.py \

# Remove second output directory, if it exists
rm -rf output2

# Run second MapReduce job
hadoop \
  jar hadoop-streaming-2.7.2.jar \
  -input output1 \
  -output output2 \
  -mapper ./map2.py \
  -reducer ./reduce2.py \

# Remove third output directory, if it exists
rm -rf output3

# Run third MapReduce job
hadoop \
  jar hadoop-streaming-2.7.2.jar \
  -input output2 \
  -output output3 \
  -mapper ./map3.py \
  -reducer ./reduce3.py \

# Remove third output directory, if it exists
rm -rf output4

# Run third MapReduce job
hadoop \
  jar hadoop-streaming-2.7.2.jar \
  -input output3 \
  -output output4 \
  -mapper ./map4.py \
  -reducer ./reduce4.py \

cat output4/part-* > inverted_index.txt