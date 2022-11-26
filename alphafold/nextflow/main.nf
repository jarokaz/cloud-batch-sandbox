#!/usr/bin/env nextflow
nextflow.enable.dsl=2 


process run_data_pipeline {
  machineType  'c2-standard-16' 
  publishDir 'gs://jk-aff-bucket/results', mode: 'copy'
  input: 
    val x
  output:
    path('features.pkl') 
    path('msas')
  script:
    """
    python /runners/run_test.py '--text=$x' '--features_path=features.pkl' '--msas_path=msas'
    """
}

workflow {
  Channel.of('Bonjour') | run_data_pipeline 
}
