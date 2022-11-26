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

```
PROJECT_NUMBER=$(gcloud projects describe jk-af-final --format='value(projectNumber)')
gcloud iam service-accounts add-iam-policy-binding \
  $PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --member=serviceAccount:workflows-sa@jk-af-final.iam.gserviceaccount.com \
  --role=roles/iam.serviceAccountUser
```

#### Sequential pipeline

```
gcloud workflows deploy af-sequential-workflow \
  --source=seq-pipeline-nfs.yaml \
  --service-account=workflows-sa@$PROJECT_ID.iam.gserviceaccount.com

gcloud workflows run af-sequential-workflow \
--data='{"fastaSequence":"jk-aff-bucket/fasta/T1050.fasta","maxTemplateDate":"2020-05-14","stagingLocation":"jk-aff-bucket/batch-jobs","modelPreset":"monomer","dbPreset":"reduced_dbs","modelParamsPath":"jk-alphafold-datasets-archive/v2.2.0","runRelax":true,"runsCollection":"AlphaFoldExperiments/T1050-Experiment/InferenceRuns","numMultimerPredictionsPermodel":5}'
```

```
gcloud workflows executions describe-last
```


#### Parallel pipeline

```
export SERVICE_ACCOUNT=workflows-sa
export PROJECT_ID=jk-af-final
```

```
gcloud workflows deploy af-parallel-workflow \
  --source=parallel-pipeline-nfs.yaml \
  --service-account=workflows-sa@$PROJECT_ID.iam.gserviceaccount.com

gcloud workflows run af-parallel-workflow \
--data='{"region":"us-central1","fastaSequence":"jk-aff-bucket/fasta/T1050.fasta","maxTemplateDate":"2020-05-14","stagingLocation":"jk-aff-bucket/batch-jobs","modelPreset":"monomer","dbPreset":"full_dbs","modelParamsPath":"jk-alphafold-datasets-archive/v2.2.0/","runRelax":true,"runsCollection":"AlphaFoldExperiments/Mysterious-Experiment/InferenceRuns","numMultimerPredictionsPerModel":5,"randomSeed":123456,"parallelism":5,"nfs_ip_address":"10.130.0.2","nfs_path":"/datasets","network":"jk-aff-network","subnet":"jk-aff-subnet","dataPipelineMachineType":"c2-standard-16","predictRelaxMachineType":"n1-standard-8-t4"}'
```

```
gcloud workflows executions describe-last
```

gcloud batch jobs describe 

gcloud workflows deploy w-parallel-workflow \
  --source=w-parallel-pipeline.yaml \
  --service-account=workflows-sa@$PROJECT_ID.iam.gserviceaccount.com

gcloud workflows run w-parallel-workflow \
--data='{"region":"us-central1","fastaSequence":"jk-aff-bucket/fasta/T1050.fasta","maxTemplateDate":"2020-05-14","stagingLocation":"jk-aff-bucket/batch-jobs","modelPreset":"monomer","dbPreset":"full_dbs","modelParamsPath":"jk-alphafold-datasets-archive/v2.2.0/","runRelax":true,"runsCollection":"AlphaFoldExperiments/Mysterious-Experiment/InferenceRuns","numMultimerPredictionsPerModel":5,"randomSeed":123456,"parallelism":5,"nfs_ip_address":"10.130.0.2","nfs_path":"/datasets","network":"jk-aff-network","subnet":"jk-aff-subnet","dataPipelineMachineType":"c2-standard-16","predictRelaxMachineType":"n1-standard-8-t4"}'
```