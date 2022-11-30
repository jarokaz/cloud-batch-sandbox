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

from alphafold_utils import relax_protein 

flags.DEFINE_string('text', 'Hello world', 'text to print')
flags.DEFINE_string('features_path', None, 'A path to features')
flags.DEFINE_string('msas_path', None, 'A path to msas')
FLAGS = flags.FLAGS

def _main(argv):

    logging.info(f'Running test')  
    logging.info(f'{FLAGS.text}')
    print(f'{FLAGS.text}')

    logging.info(f'Saving features to {FLAGS.features_path}')

    with open(FLAGS.features_path, 'w') as f:
        f.write('Bla bla')

    os.makedirs(FLAGS.msas_path, exist_ok=True)

    with open(os.path.join(FLAGS.msas_path, 'test.fasta'), 'w') as f:
        f.write('Bla bla bal')

    with open(os.path.join(FLAGS.msas_path, 'test1.fasta'), 'w') as f:
        f.write('Bla bla bal')

if __name__ == "__main__":
    app.run(_main)