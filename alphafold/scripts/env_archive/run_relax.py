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
from alphafold_utils import relax_protein


def _main(argv):
    
    del argv
    
    if os.getenv('RUN_RELAXATION', 'false') == 'false':
        logging.info(f'Skipping relaxation for {unrelaxed_protein_path}')
        return
                            
    # Retrieve and validate runner's parameters
    unrelaxed_protein_path = os.environ['UNRELAXED_PROTEIN_PATH']
    metadata_output_path = os.environ['RELAXATION_METADATA_PATH']
    relaxed_protein_path = os.environ['RELAXED_PROTEIN_PATH']
    
    max_iterations = int(os.getenv('MAX_ITERATIONS', 0))
    tolerance = float(os.getenv('TOLERANCE', 2.39))
    stiffness = float(os.getenv('STIFFNESS', 10))
    exclude_residues = os.getenv('EXCLUDE_RESIDUES', None)
    if exclude_residues:
        exclude_residues = exclude_residues.split(',')
    else:
        exclude_residues = []
    max_outer_iterations = int(os.getenv('MAX_OUTER_ITERATIONS', 3)) 

    os.makedirs(os.path.dirname(relaxed_protein_path), exist_ok=True)
    os.makedirs(os.path.dirname(metadata_output_path), exist_ok=True) 

                            
    t0 = time.time()
    logging.info('Starting model relaxation ...')

    relaxed_protein_pdb = relax_protein(
        unrelaxed_protein_path=unrelaxed_protein_path,
        relaxed_protein_path=relaxed_protein_path,
        max_iterations=max_iterations,
        tolerance=tolerance,
        stiffness=stiffness,
        exclude_residues=exclude_residues,
        max_outer_iterations=max_outer_iterations,
        use_gpu=True
    )
    
    relaxation_metadata = {
        'property_1': 'value_1',
    }
    
    with open(metadata_output_path, 'w') as f:
        json.dump(relaxation_metadata, f, indent=4)
                            
    t1 = time.time()
    logging.info(f'Model relaxation completed. Elapsed time: {t1-t0}')     

if __name__ == "__main__":
    app.run(_main)