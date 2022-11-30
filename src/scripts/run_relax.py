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
from alphafold_utils import relax_protein 

flags.DEFINE_string('metadata_output_path', None, 'A path to a metadata output file')
flags.DEFINE_string('unrelaxed_protein_path', None, 'A path to a directory that will store unrelaxed proteins')
flags.DEFINE_string('relaxed_protein_path', None, 'A path to a directory that will store relaxed proteins')
flags.DEFINE_boolean('run_relax', True, 'Whether to run the final relaxation '
                     'step on the predicted models. Turning relax off might '
                     'result in predictions with distracting stereochemical '
                     'violations but might help in case you are having issues '
                     'with the relaxation stage.')
flags.DEFINE_boolean('use_gpu_relax', True, 'Whether to relax on GPU. '
                     'Relax on GPU can be much faster than CPU, so it is '
                     'recommended to enable if possible. GPUs must be available'
                     ' if this setting is enabled.')
flags.DEFINE_integer('max_iterations', 0, 'Max iterations')
flags.DEFINE_float('tolerance', 2.39, 'Tolerance')
flags.DEFINE_float('stiffness', 10, 'Stiffness')
flags.DEFINE_integer('max_outer_iterations', 3, 'Max outer iterations')
flags.DEFINE_list('exclude_residues', [], 'The list of residues to exclude')

flags.mark_flag_as_required('metadata_output_path')
flags.mark_flag_as_required('relaxed_protein_path')
flags.mark_flag_as_required('unrelaxed_protein_path')
FLAGS = flags.FLAGS


def _main(argv):

    if not FLAGS.run_relax:
        logging.info('Skipping relaxation')
        return

    logging.info(f'Running relaxation on: {FLAGS.unrelaxed_protein_path}')  

    os.makedirs(os.path.dirname(FLAGS.relaxed_protein_path), exist_ok=True)
    os.makedirs(os.path.dirname(FLAGS.metadata_output_path), exist_ok=True) 
    t0 = time.time()
    logging.info('Starting model relaxation ...')

    relaxed_protein_pdb = relax_protein(
        unrelaxed_protein_path=FLAGS.unrelaxed_protein_path,
        relaxed_protein_path=FLAGS.relaxed_protein_path,
        max_iterations=FLAGS.max_iterations,
        tolerance=FLAGS.tolerance,
        stiffness=FLAGS.stiffness,
        exclude_residues=FLAGS.exclude_residues,
        max_outer_iterations=FLAGS.max_outer_iterations,
        use_gpu=FLAGS.use_gpu_relax
    )
    
    relaxation_metadata = {
        'property_1': 'value_1',
    }
    
    with open(FLAGS.metadata_output_path, 'w') as f:
        json.dump(relaxation_metadata, f, indent=4)
                            
    t1 = time.time()
    logging.info(f'Model relaxation completed. Elapsed time: {t1-t0}') 

if __name__ == "__main__":
    app.run(_main)