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
import time

from absl import app
from absl import logging

from alphafold_utils import run_data_pipeline


def _main(argv):
    
    del argv
    
    # Retrieve and validate runner parameters
    fasta_input_path = os.environ['FASTA_INPUT_PATH']
    msas_output_path = os.environ['MSAS_OUTPUT_PATH']
    features_output_path = os.environ['FEATURES_OUTPUT_PATH']
    metadata_output_path = os.environ['METADATA_OUTPUT_PATH']
    ref_dbs_root_path = os.environ['REF_DBS_ROOT_PATH']
    max_template_date = os.environ['MAX_TEMPLATE_DATE']
    model_preset = os.environ['MODEL_PRESET']
    db_preset = os.environ['DB_PRESET']
    
    uniref90_database_path = os.path.join(ref_dbs_root_path, 
                                          os.getenv('UNIREF90_DATABASE_PATH', 'uniref90/uniref90.fasta'))
    mgnify_database_path = os.path.join(ref_dbs_root_path, 
                                        os.getenv('MGNIFY_DATABASE_PATH', 'mgnify/mgy_clusters_2018_12.fa'))
    bfd_database_path = os.path.join(ref_dbs_root_path, 
                                     os.getenv('BFD_DATABASE_PATH', 'bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt'))
    small_bfd_database_path = os.path.join(ref_dbs_root_path, 
                                           os.getenv('SMALL_BFD_DATABASE_PATH', 'small_bfd/bfd-first_non_consensus_sequences.fasta'))
    uniclust30_database_path = os.path.join(ref_dbs_root_path, 
                                            os.getenv('UNICLUST30_DATABASE_PATH', 'uniclust30/uniclust30_2018_08/uniclust30_2018_08'))
    uniprot_database_path = os.path.join(ref_dbs_root_path, 
                                         os.getenv('UNIPROT_DATABASE_PATH', 'uniprot/uniprot.fasta'))
    pdb70_database_path = os.path.join(ref_dbs_root_path, 
                                       os.getenv('PDB70_DATABASE_PATH', 'pdb70/pdb70'))
    obsolete_pdbs_path = os.path.join(ref_dbs_root_path, 
                                      os.getenv('OBSOLETE_PDBS_PATH', 'pdb_mmcif/obsolete.dat'))
    seqres_database_path = os.path.join(ref_dbs_root_path, 
                                        os.getenv('SEQRES_DATABASE_PATH', 'pdb_seqres/pdb_seqres.txt'))
    mmcif_path = os.path.join(ref_dbs_root_path, 
                              os.getenv('MMCIF_PATH', 'pdb_mmcif/mmcif_files'))
    
    if model_preset not in ['monomer', 'monomer_casp14', 'monomer_ptm', 'multimer']:
        raise ValueError(f'Incorrect model preset {model_preset}')
                         
    if db_preset not in ['full_dbs', 'reduced_dbs']:
        raise ValueError(f'Incorrect db preset {db_preset}')
        
    # TBD: Validate max_template_date

    os.makedirs(msas_output_path, exist_ok=True)
    os.makedirs(os.path.dirname(features_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(metadata_output_path), exist_ok=True)
    
    use_small_bfd = db_preset == 'reduced_dbs'
    run_multimer_system = model_preset == 'multimer'

    logging.info(f'Running data pipeline on: {fasta_input_path}') 
    t0 = time.time()
    
    features_dict, msas_metadata = run_data_pipeline(
        fasta_path=fasta_input_path,
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
        max_template_date=max_template_date,
        msa_output_path=msas_output_path,
        features_output_path=features_output_path,
    ) 

    with open(metadata_output_path, 'w') as f:
        json.dump(msas_metadata, f, indent=4)
        
    t1 = time.time()
    logging.info(f'Data pipeline completed. Elapsed time: {t1-t0}')    

if __name__ == "__main__":
    app.run(_main)