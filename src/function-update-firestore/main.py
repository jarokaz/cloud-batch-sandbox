####
# Alphafold:
#   - Update Experiment status
####

import json
import functions_framework
from google.cloud import firestore
from google.cloud import storage

@functions_framework.http
def af_update_experiment_status(request):
    # Instantiate clients
    db = firestore.Client()
    storage_client = storage.Client()

    # Retrieve request arguments from json
    args = request.get_json()

    # Create reference to the RUN document
    run_document_ref = db.collection('experiments').document(args['job_id'])
    base_bucket = storage_client.bucket(args['bucket_name'])

    # Update Features Data
    if args['mode'] == 'data':
        features_blob = base_bucket.blob(args['args']['blob_data_metadata_path'])
        features_data = json.loads(features_blob.download_as_string())

        run_document_ref.set(
            {'features_results': features_data, 'status':args['status']}, merge=True)

    elif args['mode'] == 'predict_relax':
        # Update Predict / Relax metadata
        update_data = []
        for i in args['args']['predict_relax']:
            if args['status'][i['batch_job_id']] == 'SUCCEEDED':
                prediction_blob = base_bucket.blob(i['blob_prediction_metadata_path'])
                prediction_data = json.loads(prediction_blob.download_as_string())

                relax_blob = base_bucket.blob(i['blob_relaxation_metadata_path'])
                relax_data = json.loads(relax_blob.download_as_string())

                i['results'] = {**prediction_data, **relax_data}
                update_data.append(i)
            else:
                update_data.append(i)

        run_document_ref.set({'predict_relax': update_data, 'status':args['status']}, merge=True)

    return 'ok'
