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
export PROJECT_ID=jk-mlops-dev

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
```

#### Sequential pipeline

```
gcloud workflows deploy af-sequential-workflow \
  --source=seq-pipeline.yaml \
  --service-account=workflows-sa@jk-mlops-dev.iam.gserviceaccount.com

gcloud workflows run af-sequential-workflow
--data='{"fastaSequence":"jk-alphafold-staging/fasta/T1050.fasta","maxTemplateDate":"2020-05-14","stagingLocation":"jk-alphafold-staging/batch-jobs","refDBsDisk":"projects/jk-mlops-dev/zones/us-central1-a/disks/alphafold-datasets-v220","useSmallBFD":"true"}'
```

```
gcloud workflows executions describe-last
```