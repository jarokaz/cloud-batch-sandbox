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

from absl import flags
from absl import app
from absl import logging

from alphafold.model import config
from alphafold_utils import predict

flags.DEFINE_string('input_features_path', None, 'A path to input features')
flags.DEFINE_string('model_params_path', None, 'A path to model parameters')
flags.DEFINE_string('metadata_output_path', None, 'A path to a metadata output file')
flags.DEFINE_string('raw_predictions_output_path', None, 'A path to a raw prediction file')
flags.DEFINE_string('unrelaxed_proteins_path', None, 'A path to an unrelaxed protein path')

flags.DEFINE_enum('model_preset', 'monomer',
                  ['monomer', 'monomer_casp14', 'monomer_ptm', 'multimer'],
                  'Choose preset model configuration - the monomer model, '
                  'the monomer model with extra ensembling, monomer model with '
                  'pTM head, or multimer model')
flags.DEFINE_integer('model_index', None, 'Model index')
flags.DEFINE_integer('prediction_index', None, 'Prediction index')
flags.DEFINE_integer('random_seed', None, 'The random seed')


flags.mark_flag_as_required('model_params_path')
flags.mark_flag_as_required('input_features_path')
flags.mark_flag_as_required('metadata_output_path')
flags.mark_flag_as_required('raw_predictions_output_path')
flags.mark_flag_as_required('unrelaxed_proteins_path')
flags.mark_flag_as_required('model_index')
flags.mark_flag_as_required('prediction_index')
flags.mark_flag_as_required('random_seed')                     

FLAGS = flags.FLAGS


def _main(argv):
                            
    logging.info(f'Model index: {FLAGS.model_index}')
    logging.info(f'Prediction index: {FLAGS.prediction_index}')
    logging.info(f'Random seed: {FLAGS.random_seed}')
    return              
               
    os.makedirs(os.path.dirname(FLAGS.raw_predictions=_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(FLAGS.unrelaxed_protein_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(FLAGS.metadata_output_path), exist_ok=True) 
    raw_prediction_path = "tbd"
    unrelaxed_protein_path = "tbd"

    run_multimer_system = 'multimer' == FLAGS.model_preset
    num_ensemble = 8 if FLAGS.model_preset == 'monomer_casp14' else 1
    model_name = config.MODEL_PRESETS[FLAGS.model_preset][FLAGS.model_index]
                            
    logging.info(f'Starting model prediction {prediction_index} using model {model_name}...')
    t0 = time.time()

    prediction_result = alphafold_predict(
        model_features_path=model_features.path,
        model_params_path=model_params.path,
        model_name=model_name,
        num_ensemble=num_ensemble,
        run_multimer_system=run_multimer_system,
        random_seed=FLAGS.random_seed,
        raw_prediction_path=raw_prediction_path,
        unrelaxed_protein_path=unrelaxed_protein_path
    )

    prediction_metadata = {
        'model_name': model_name,
        '
    }
    with open(FLAGS.metadata_output_path, 'w') as f:
        json.dump(prediction_metadata, f, indent=4)
                            
    t1 = time.time()
    logging.info(f'Model prediction completed. Elapsed time: {t1-t0}')     

if __name__ == "__main__":
    app.run(_main)