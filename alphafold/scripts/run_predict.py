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

"""A utility to submit a Vertex Training T5X job."""

import json
import os
import random
import time
import sys


from absl import app
from absl import logging

from alphafold.model import config
from alphafold_utils import predict


def _main(argv):
    
    del argv
                            
    # Retrieve and validate runner's parameters
    input_features_path = os.environ['INPUT_FEATURES_PATH']
    model_params_path = os.environ['MODEL_PARAMS_PATH']
    metadata_output_path = os.environ['METADATA_OUTPUT_PATH']
    raw_predictions_output_path = os.environ['RAW_PREDICTIONS_OUTPUT_PATH']
    unrelaxed_proteins_output_path = os.environ['UNRELAXED_PROTEINS_OUTPUT_PATH']
    model_preset = os.environ['MODEL_PRESET']
    model_index = int(os.environ['MODEL_INDEX'])
    prediction_index = int(os.environ['PRED_INDEX'])
    random_seed = int(os.environ['RANDOM_SEED'])
    
    if model_preset not in ['monomer', 'monomer_casp14', 'monomer_ptm', 'multimer']:
        raise ValueError(f'Incorrect model preset {model_preset}')
                             
    os.makedirs(raw_predictions_output_path, exist_ok=True)
    os.makedirs(unrelaxed_proteins_output_path, exist_ok=True)
    os.makedirs(os.path.dirname(metadata_output_path), exist_ok=True) 

    run_multimer_system = 'multimer' == model_preset
    num_ensemble = 8 if model_preset == 'monomer_casp14' else 1
    model_name = config.MODEL_PRESETS[model_preset][model_index]
    raw_prediction_path = os.path.join(raw_predictions_output_path, f'result_{model_name}_pred_{prediction_index}.pkl')
    unrelaxed_protein_path = os.path.join(unrelaxed_proteins_output_path, f'unrelaxed_{model_name}_pred_{prediction_index}.pkl')
                            
    logging.info(f'Starting model prediction {prediction_index} using model {model_name}...')
    t0 = time.time()

    prediction_result = predict(
        model_features_path=input_features_path,
        model_params_path=model_params_path,
        model_name=model_name,
        num_ensemble=num_ensemble,
        run_multimer_system=run_multimer_system,
        random_seed=random_seed,
        raw_prediction_path=raw_prediction_path,
        unrelaxed_protein_path=unrelaxed_protein_path
    )

    prediction_metadata = {
        'model_name': model_name,
        'ranking_confidence': prediction_result['ranking_confidence'],
    }
    
    with open(metadata_output_path, 'w') as f:
        json.dump(prediction_metadata, f, indent=4)
                            
    t1 = time.time()
    logging.info(f'Model prediction completed. Elapsed time: {t1-t0}')     

if __name__ == "__main__":
    app.run(_main)