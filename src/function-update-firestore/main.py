####
# Alphafold:
#   - Update Experiment status
####

import functions_framework
from google.cloud import firestore

@functions_framework.http
def af_update_experiment_status(request):
    # Instantiate clients
    db = firestore.Client()

    # Retrieve request arguments from json
    args = request.get_json()

    # Create reference to the RUN document
    run_document_ref = db.collection('experiments').document(args['job_id'])
    
    # Update run STATUS on private and public documents
    run_document_ref.set({'status':args['status']}, merge=True)

    return 'ok'