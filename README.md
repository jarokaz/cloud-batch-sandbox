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
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@jk-mlops-dev.iam.gserviceaccount.com" \
  --role=roles/batch.jobsAdmin

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@jk-mlops-dev.iam.gserviceaccount.com" \
  --role=roles/logging.logWriter

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SA_NAME@jk-mlops-dev.iam.gserviceaccount.com" \
  --role=roles/storage.admin
```

#### Sequential pipeline

```
gcloud workflows deploy af-sequential-workflow \
  --source=seq-pipeline.yaml \
  --service-account=workflows-sa@jk-mlops-dev.iam.gserviceaccount.com

gcloud workflows run af-sequential-workflow
```

```
gcloud workflows executions describe-last
```