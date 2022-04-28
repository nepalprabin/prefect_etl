# A ETL pipeline using [prefect](https://www.prefect.io/)

This repository contains ETL pipeline for https://www.ncbi.nlm.nih.gov/geo/ and scraped about 1000 data.

## Running data pipeline

1. Clone repo: <code> https://github.com/nepalprabin/prefect_etl.git</code>
2. cd prefect_etl
3. <code> pip install -r requirements.txt </code>
4. Setup prefect cloud backend: <code>prefect backend cloud</code>
5. Authenticate with Prefect Cloud: <code> prefect auth login --key YOUR-KEY </code> API key can be created by signing up at https://cloud.prefect.io/user/keys
6. Once authenticated run prefect UI on the cloud.


## Output
1. Running the flow creates gds_data.db which stores scraped data in the form of (id, title, body) as column names.
2. gds_data.json which is loaded to the elasticsearch as well as saved as local files.
    ```
    [
    {
        "id": "200197976",
        "title": "Impact of an Immune Modulator Mycobacterium-w on Adaptive Natural Killer Cells and Protection Against COVID-19",
        "data": "Whole transcriptome Differential Gene Expression (DGE) analysis was carried out on four biological replicates of both Mw (0.1 ml Mw administrated intradermally in each arm) and Control group at 6 months following exposure to Mycobacterium-w. Sequencing was done through Direct cDNA Sequencing (oxford nanopore technologies, Oxford, UK) using RNA isolated from Peripheral blood mononuclear cells (PBMC) by Trizol method. more...Organism:Homo sapiensType:Expression profiling by high throughput sequencingPlatform: GPL24106 8 SamplesFTP download: GEO (XLSX) ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE197nnn/GSE197976/SeriesAccession: GSE197976ID: 200197976"
    },
    {
        "id": "200165182",
        "title": "Single-cell RNA sequencing of PBMCs sampled from COVID-19 patients",
        "data": "To explore the underlying mechanism of recurrent SARS-CoV-2 infection in convalescent patients. We performed single-cell RNA sequencing on peripheral blood mononuclear cells isolated from a recurrent patient, taking 14 recovered COVID-19 patients and 4 dead COVID-19 patients as controls.Organism:Homo sapiensType:Expression profiling by high throughput sequencingPlatform: GPL24676 19 SamplesFTP download: GEO (TXT) ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE165nnn/GSE165182/SeriesAccession: GSE165182ID: 200165182"
    },
    {
        "id": "200198592",
        "title": "The SARS-CoV-2 receptor ACE2 is expressed in mouse pericytes but not endothelial cells \u2013 implications for COVID-19 vascular research",
        "data": "Humanized mouse models and mouse-adapted SARS-CoV-2 virus are increasingly used to study COVID-19 pathogenesis, and it is therefore important to learn where the SARS-CoV-2 receptor ACE2 is expressed. Here we mapped ACE2 expression during mouse postnatal development and in adulthood. Pericytes in the central nervous system, heart and pancreas express ACE2 strongly, as do perineurial and adrenal fibroblasts, whereas endothelial cells do not at any location analyzed. more...Organism:Mus musculusType:Expression profiling by high throughput sequencingPlatform: GPL21493 496 SamplesFTP download: GEO (TXT) ftp://ftp.ncbi.nlm.nih.gov/geo/series/GSE198nnn/GSE198592/SeriesAccession: GSE198592ID: 200198592"
    }
    ]
    ```
3. all ids with given query which is loaded to the elasticsearch as well as saved as local files.
```
    {
    "covid": [
    "200197976", 
    "200165182",
    "200198592", 
    "200200988", 
    "200200896", 
    "200193395", 
    "200182183", 
    "200154272"
        ]
    }
```

## Running on docker (Partial)
1. To run prefect on Docker, write a Dockerfile containing following components:
    - FROM: base image that we will be using for our image
    - WORKDIR: setting working directory for the container
    - ADD: add all of our files from the current directory to the container WORKDIR
    - RUN: install our library . This will also install all requirements.

2. Building an image:
<code>docker build . -t test:latest</code>

3. After creating image push to registry (using DockerHub)