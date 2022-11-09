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
from alphafold_utils import predict_relax 

flags.DEFINE_string('metadata_output_path', None, 'A path to a metadata output file')
flags.DEFINE_string('raw_predictions_output_path', None, 'A path to a directory that will store raw predictions')
flags.DEFINE_string('unrelaxed_proteins_output_path', None, 'A path to a directory that will store unrelaxed proteins')
flags.DEFINE_string('relaxed_proteins_output_path', None, 'A path to a directory that will store relaxed proteins')
flags.DEFINE_string('input_features_path', None, 'A path to input features')
flags.DEFINE_string('model_params_path', None, 'A path to model parameters')
flags.DEFINE_enum('model_preset', 'monomer',
                  ['monomer', 'monomer_casp14', 'monomer_ptm', 'multimer'],
                  'Choose preset model configuration - the monomer model, '
                  'the monomer model with extra ensembling, monomer model with '
                  'pTM head, or multimer model')
flags.DEFINE_integer('random_seed', None, 'The random seed for the data '
                     'pipeline. By default, this is randomly generated. Note '
                     'that even if this is set, Alphafold may still not be '
                     'deterministic, because processes like GPU inference are '
                     'nondeterministic.')
flags.DEFINE_integer('num_multimer_predictions_per_model', 5, 'How many '
                     'predictions (each with a different random seed) will be '
                     'generated per model. E.g. if this is 2 and there are 5 '
                     'models then there will be 10 predictions per input. '
                     'Note: this FLAG only applies if model_preset=multimer')
flags.DEFINE_boolean('run_relax', True, 'Whether to run the final relaxation '
                     'step on the predicted models. Turning relax off might '
                     'result in predictions with distracting stereochemical '
                     'violations but might help in case you are having issues '
                     'with the relaxation stage.')
flags.DEFINE_boolean('use_gpu_relax', True, 'Whether to relax on GPU. '
                     'Relax on GPU can be much faster than CPU, so it is '
                     'recommended to enable if possible. GPUs must be available'
                     ' if this setting is enabled.')
flags.mark_flag_as_required('model_params_path')
flags.mark_flag_as_required('artifacts_output_path')
flags.mark_flag_as_required('metadata_output_path')
FLAGS = flags.FLAGS


def _main(argv):

    logging.info(f'Running prediction and relaxation using features in: {FLAGS.input_features_path}')  

    os.makedirs(FLAGS.raw_predictions_output_path, exist_ok=True)
    os.makedirs(FLAGS.unrelaxed_proteins_output_path, exist_ok=True)
    os.makedirs(FLAGS.relaxed_proteins_output_path, exist_ok=True)
    os.makedirs(os.path.dirname(FLAGS.metadata_output_path), exist_ok=True) 

    run_multimer_system = 'multimer' == FLAGS.model_preset
    num_ensemble = 8 if FLAGS.model_preset == 'monomer_casp14' else 1
    num_predictions_per_model = FLAGS.num_multimer_predictions_per_model if FLAGS.model_preset == 'multimer' else 1
    models = config.MODEL_PRESETS[FLAGS.model_preset]

    if FLAGS.random_seed is None:
        random_seed = random.randrange(
            sys.maxsize // (len(models) * num_predictions_per_model)
        )
    else:
        random_seed = FLAGS.random_seed
    
    prediction_runners = []
    for model_name in models:
        for i in range(num_predictions_per_model):
            prediction_runners.append({
                'prediction_index': i,
                'model_name': model_name,
                'random_seed': random_seed
            })
            random_seed += 1

    model_features_path = os.path.join(FLAGS.artifacts_output_path, FEATURES_FILE)

    logging.info(f'Starting predictions on {prediction_runners} ...')
    t0 = time.time()

    ranking_confidences = predict_relax(
        model_features_path=model_features_path,
        model_params_path=FLAGS.model_params_path,
        prediction_runners=prediction_runners,
        num_ensemble=num_ensemble,
        run_multimer_system=run_multimer_system,
        run_relax=FLAGS.run_relax,
        raw_prediction_path=FLAGS.raw_predictions_output_path,
        unrelaxed_protein_path=FLAGS.unrelaxed_proteins_output_path,
        relaxed_protein_path=FLAGS.relaxed_proteins_output_path
    )  

    with open(FLAGS.metadata_output_path, 'w') as f:
        json.dump(ranking_confidences, f, indent=4)
    t1 = time.time()
    logging.info(f'Model predictions completed. Elapsed time: {t1-t0}')     

if __name__ == "__main__":
    app.run(_main)