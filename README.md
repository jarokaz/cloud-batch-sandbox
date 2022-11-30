# Cloud Batch Sandbox

## Deploy Workflow

```
gcloud workflows deploy alphafold-workflow-batch \
  --source=./src/workflows/alphafold-pipeline.yaml
```

## Deploy Functions

```
gcloud functions deploy af-update-experiment-status \
--gen2 \
--runtime=python310 \
--region=us-central1 \
--source=./src/function-update-firestore/ \
--entry-point=af_update_experiment_status \
--trigger-http \
--allow-unauthenticated
```
