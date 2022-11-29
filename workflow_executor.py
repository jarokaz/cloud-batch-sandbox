# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Execute a workflow and print the execution results."""
import json
import time
import typing as T

from google.cloud import workflows_v1beta
from google.cloud.workflows import executions_v1beta
from google.cloud.workflows.executions_v1beta.types import executions

from google.cloud import storage
from google.cloud import firestore


def prepare_args_for_experiments(
    project_id: str,
    bucket_name: str,
    region: str,
    sequence_str: str,
    job_id: str,
    blob_sequence_path: str,
    gcs_job_path: str,
    image_uri: str,
    network_name: str,
    subnetwork_name: str,
    nfs_ip_address: str,
    nfs_path: str,
    network: str,
    subnet: str,
    max_template_date: str,
    model_preset: str,
    db_preset: str,
    data_metadata_filename: str,
    msas_folder: str,
    data_features_filename: str,
    blob_data_metadata_path: str,
    blob_data_features_path: str,
    num_predictions_per_model: int,
    model_params_path: str,
    num_models: int,
    run_relax: bool,
    random_seed: int,
    parallelism: int
) -> T.Dict:
    """Prepare arguments to execute Workflow"""
    storage_client = storage.Client()
    db = firestore.Client()

    args = {}
    args['project_id'] = project_id
    args['bucket_name'] = bucket_name
    args['region'] = region
    args['sequence_str'] = sequence_str
    args['job_id'] = job_id
    args['blob_sequence_path'] = blob_sequence_path
    args['gcs_job_path'] = gcs_job_path
    args['image_uri'] = image_uri
    args['network_name'] = network_name
    args['subnetwork_name'] = subnetwork_name
    args['nfs_ip_address'] = nfs_ip_address
    args['nfs_path'] = nfs_path
    args['network'] = network
    args['subnet'] = subnet
    args['max_template_date'] = max_template_date
    args['model_preset'] = model_preset
    args['db_preset'] = db_preset
    args['data_metadata_filename'] = data_metadata_filename
    args['msas_folder'] = msas_folder
    args['data_features_filename'] = data_features_filename
    args['blob_data_metadata_path'] = blob_data_metadata_path
    args['blob_data_features_path'] = blob_data_features_path
    args['num_predictions_per_model'] = num_predictions_per_model
    args['model_params_path'] = model_params_path
    args['num_models'] = num_models
    args['run_relax'] = run_relax
    args['random_seed'] = random_seed
    args['parallelism'] = parallelism

    status = {f'{job_id}-data-pipeline': 'SCHEDULED'}

    model_relax_info = []
    for i in range(num_predictions_per_model * num_models):
        model_relax = {}
        model_relax['batch_job_id'] = f'{job_id}-predict-relax-{i}'
        model_relax['model_index'] = f'{i // num_predictions_per_model}'
        model_relax['prediction_index'] = f'{i % num_predictions_per_model}'
        model_relax['prediction_random_seed'] = f'{random_seed + i}'
        model_relax['blob_raw_prediction_path'] = f'result_model_{model_relax["model_index"]}_pred_{model_relax["prediction_index"]}.pkl'
        model_relax['blob_unrelaxed_protein_path'] = f'unrelaxed_model_{model_relax["model_index"]}_pred_{model_relax["prediction_index"]}.pdb'
        model_relax['blob_relaxed_protein_path'] = f'relaxed_model_{model_relax["model_index"]}_pred_{model_relax["prediction_index"]}.pdb'
        model_relax['blob_prediction_metadata_path'] = f'pred_metadata_model_{model_relax["model_index"]}_pred_{model_relax["prediction_index"]}.json'
        model_relax['blob_relaxation_metadata_path'] = f'relax_metadata_model_{model_relax["model_index"]}_pred_{model_relax["prediction_index"]}.json'

        model_relax_info.append(model_relax)
        status[model_relax['batch_job_id']] = 'SCHEDULED'

    args['status'] = status
    args['model_relax'] = model_relax_info

    # Upload sequence to GCS
    base_bucket = storage_client.bucket(args['bucket_name'])
    blob = base_bucket.blob(args['blob_sequence_path'])
    blob.upload_from_string(args['sequence_str'])

    # Log metadata to Firestore
    experiment_document_ref = db.collection('experiments').document()
    experiment_document_ref.set(args, merge=True)

    return args


def execute_workflow( 
    workflow_name: str,
    args: T.Dict
):
    # Set up API clients.
    execution_client = executions_v1beta.ExecutionsClient()
    workflows_client = workflows_v1beta.WorkflowsClient()

    # Construct the fully qualified location path.
    parent = workflows_client.workflow_path(
        args['project_id'], args['region'], workflow_name)

    # Execute the workflow.
    response = execution_client.create_execution(
        request={"parent": parent, "arguments": json.dumps(args)}, )
    print(f"Created execution: {response.name}")

    # Wait for execution to finish, then print results.
    execution_finished = False
    backoff_delay = 1  # Start wait with delay of 1 second
    print('Poll every second for result...')
    while (not execution_finished):
        execution = execution_client.get_execution(request={"name": response.name})
        execution_finished = execution.state != executions.Execution.State.ACTIVE

        # If we haven't seen the result yet, wait a second.
        if not execution_finished:
            print('- Waiting for results...')
            time.sleep(backoff_delay)
            backoff_delay *= 2  # Double the delay to provide exponential backoff.
        else:
            print(f'Execution finished with state: {execution.state.name}')
            print(execution.result)
            return execution.result