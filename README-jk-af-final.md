# Cloud Batch Sandbox

### Hello World

```
gcloud batch jobs submit alphafold-inference-job-42 \
  --location us-central1 \
  --config alphafold-data-pipeline.json 
```


### Google Workflows

```
gcloud services enable \
  artifactregistry.googleapis.com \
  batch.googleapis.com \
  cloudbuild.googleapis.com \
  workflowexecutions.googleapis.com \
  workflows.googleapis.com
```

```
export SERVICE_ACCOUNT=workflows-sa
export PROJECT_ID=jk-af-final

gcloud iam service-accounts create $SERVICE_ACCOUNT
```

```
# Needed for Workflows to create Jobs
# See https://cloud.google.com/batch/docs/release-notes#October_03_2022
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/batch.jobsEditor

# Needed for Workflows to submit Jobs
# See https://cloud.google.com/batch/docs/release-notes#October_03_2022
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/iam.serviceAccountUser

# Needed for Workflows to create buckets
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/storage.admin

# Need for Workflows to log
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/logging.logWriter

# Need for Workflows to use Firestore
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member serviceAccount:$SERVICE_ACCOUNT@$PROJECT_ID.iam.gserviceaccount.com \
    --role roles/datastore.owner
```

#### Sequential pipeline

```
gcloud workflows deploy af-sequential-workflow \
  --source=seq-pipeline-nfs.yaml \
  --service-account=workflows-sa@jk-af-final.iam.gserviceaccount.com

gcloud workflows run af-sequential-workflow \
--data='{"fastaSequence":"jk-aff-bucket/fasta/T1050.fasta","maxTemplateDate":"2020-05-14","stagingLocation":"jk-aff-bucket/batch-jobs","modelPreset":"monomer","dbPreset":"reduced_dbs","modelParamsPath":"jk-alphafold-datasets-archive/v2.2.0","runRelax":true,"runsCollection":"AlphaFoldExperiments/T1050-Experiment/InferenceRuns"}'
```

```
gcloud workflows executions describe-last
```


8116723-data-pipeline
