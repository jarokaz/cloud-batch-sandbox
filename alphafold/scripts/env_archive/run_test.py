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

from absl import flags
from absl import app
from absl import logging

from alphafold_utils import run_data_pipeline

flags.DEFINE_string('fasta_input_path', None, 'A path to sequence')
flags.DEFINE_string('msas_output_path', None, 'A path to a directory that will store msas')
flags.DEFINE_integer('model_index', 0, 'Model index')

flags.mark_flag_as_required('fasta_input_path')
flags.mark_flag_as_required('msas_output_path')
FLAGS = flags.FLAGS


def _main(argv):
    
    logging.info(f'Running data pipeline on: {FLAGS.fasta_input_path}') 
    logging.info(f'Model index: {FLAGS.model_index}')

 

if __name__ == "__main__":
    app.run(_main)