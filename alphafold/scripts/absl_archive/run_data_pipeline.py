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
flags.DEFINE_string('features_output_path', None, 'A path to a features file')
flags.DEFINE_string('metadata_output_path', None, 'A path to a metadata output file')
flags.DEFINE_string('ref_dbs_root_path', None, 'Mount path to reference dbs')
flags.DEFINE_string('uniref90_database_path', 'uniref90/uniref90.fasta', 'Uniref90 database path')
flags.DEFINE_string('mgnify_database_path', 'mgnify/mgy_clusters_2018_12.fa', 'Mgnify database path')
flags.DEFINE_string('bfd_database_path', 'bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt', 'BFD database path')
flags.DEFINE_string('small_bfd_database_path', 'small_bfd/bfd-first_non_consensus_sequences.fasta', 'Small BFD database path')
flags.DEFINE_string('uniclust30_database_path', 'uniclust30/uniclust30_2018_08/uniclust30_2018_08', 'Uniclust30 database path')
flags.DEFINE_string('uniprot_database_path', 'uniprot/uniprot.fasta', 'Uniprot database path')
flags.DEFINE_string('pdb70_database_path', 'pdb70/pdb70', 'PDB70 database path')
flags.DEFINE_string('obsolete_pdbs_path', 'pdb_mmcif/obsolete.dat', 'Uniref90 database path')
flags.DEFINE_string('seqres_database_path', 'pdb_seqres/pdb_seqres.txt', 'Uniref90 database path')
flags.DEFINE_string('mmcif_path', 'pdb_mmcif/mmcif_files', 'Uniref90 database path')
flags.DEFINE_string('max_template_date', None, 'Max template date')
flags.DEFINE_enum('model_preset', 'monomer',
                  ['monomer', 'monomer_casp14', 'monomer_ptm', 'multimer'],
                  'Choose preset model configuration - the monomer model, '
                  'the monomer model with extra ensembling, monomer model with '
                  'pTM head, or multimer model')
flags.DEFINE_enum('db_preset', 'full_dbs',
                  ['full_dbs', 'reduced_dbs'],
                  'Choose preset MSA database configuration - '
                  'smaller genetic database config (reduced_dbs) or '
                  'full genetic database config  (full_dbs)')
flags.mark_flag_as_required('fasta_input_path')
flags.mark_flag_as_required('max_template_date')
flags.mark_flag_as_required('msas_output_path')
flags.mark_flag_as_required('features_output_path')
flags.mark_flag_as_required('metadata_output_path')
flags.mark_flag_as_required('ref_dbs_root_path')
FLAGS = flags.FLAGS


def _main(argv):
    
    logging.info(f'Running data pipeline on: {FLAGS.fasta_input_path}') 

    os.makedirs(FLAGS.msas_output_path, exist_ok=True)
    os.makedirs(os.path.dirname(FLAGS.features_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(FLAGS.metadata_output_path), exist_ok=True)

    uniref90_database_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.uniref90_database_path)
    mgnify_database_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.mgnify_database_path)
    uniclust30_database_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.uniclust30_database_path)
    bfd_database_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.bfd_database_path)
    small_bfd_database_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.small_bfd_database_path)
    uniprot_database_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.uniprot_database_path)
    pdb70_database_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.pdb70_database_path)
    obsolete_pdbs_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.obsolete_pdbs_path)
    seqres_database_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.seqres_database_path)
    mmcif_path = os.path.join(
        FLAGS.ref_dbs_root_path, FLAGS.mmcif_path)
    
    use_small_bfd = FLAGS.db_preset == 'reduced_dbs'
    run_multimer_system = FLAGS.model_preset == 'multimer'

    features_dict, msas_metadata = run_data_pipeline(
        fasta_path=FLAGS.fasta_input_path,
        run_multimer_system=run_multimer_system,
        use_small_bfd=use_small_bfd,
        uniref90_database_path=uniref90_database_path,
        mgnify_database_path=mgnify_database_path,
        bfd_database_path=bfd_database_path,
        small_bfd_database_path=small_bfd_database_path,
        uniclust30_database_path=uniclust30_database_path,
        uniprot_database_path=uniprot_database_path,
        pdb70_database_path=pdb70_database_path,
        obsolete_pdbs_path=obsolete_pdbs_path,
        seqres_database_path=seqres_database_path,
        mmcif_path=mmcif_path,
        max_template_date=FLAGS.max_template_date,
        msa_output_path=FLAGS.msas_output_path,
        features_output_path=FLAGS.features_output_path,
    ) 

    with open(FLAGS.metadata_output_path, 'w') as f:
        json.dump(msas_metadata, f, indent=4)
 

if __name__ == "__main__":
    app.run(_main)