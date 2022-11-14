#!/bin/bash
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This is a simple wrapper on top of dsub. In this "incarnation"
# we use dsub --wait option to wait for the CLS pipeline to complete
# The next step would be to retrieve status and logs on a more regular
# basis so we can push it back to Vertex Pipelines

set -o errexit
set -o nounset

trap 'exit_handler $? $LINENO' 1 2 3 15 ERR  

exit_handler() {
    echo "Error $1 occured in line $2"
}

function usage {
    echo "Usage: run_step.sh <step name>"
    echo "<step name> can be data_pipeline, predict_relax, relaxation"
    exit 1
}


if [ "$#" -ne 1 ]; then
    echo "incorrect number of parameters"
    usage
fi

ldconfig

case "$1" in

  data_pipeline)
    echo "Running data pipeline"
    python /runners/run_data_pipeline.py \
    --fasta_input_path=${FASTA_INPUT_PATH} \
    --metadata_output_path=${METADATA_OUTPUT_PATH} \
    --msas_output_path=${MSAS_OUTPUT_PATH} \
    --features_output_path=${FEATURES_OUTPUT_PATH} \
    --model_preset=${MODEL_PRESET} \
    --db_preset=${DB_PRESET} \
    --max_template_date=${MAX_TEMPLATE_DATE} \
    --ref_dbs_root_path=${REF_DBS_ROOT_PATH}
    ;;

  predict)
    echo  "Running prediction"
    python /runners/run_predict.py \
    --input_features_path=${INPUT_FEATURES_PATH} \
    --model_params_path=${MODEL_PARAMS_PATH} \
    --metadata_output_path=${METADATA_OUTPUT_PATH} \
    --raw_predictions_output_path=${RAW_PREDICTION_OUTPUT_PATH} \
    --unrelaxed_proteins_output_path=${UNRELAXED_PROTEINS_OUTPUT_PATH} \
    --model_preset=${MODEL_PRESET} \
    --model_index=${MODEL_INDEX} \
    --prediction_index=${PRED_INDEX} \
    --random_seed=${RANDOM_SEED}
    ;;
    
  relax)
    echo  "Running relaxation"
    python /runners/run_relaxation.py \
    ;;


  *)
    echo "Unknown step"
    usage
    ;;
esac