1. create and end to end ML pipeline
2. Automate hte pipeline using DVC
3. Adding configurable params to pipeline
4. Experiment tracking using dvclive
5. AWS setup with DVC for data versioning

# Data Science Pipeline Bracket

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│                 │    │                 │    │                 │    │                 │    │                 │
│  Data Ingestion │───▶│ Data Preprocessing│───▶│Feature Engineering│───▶│ Model Training  │───▶│Model Evaluation │
│                 │    │                 │    │                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Pipeline Flow

1. **Data Ingestion** → 2. **Data Preprocessing** → 3. **Feature Engineering** → 4. **Model Training** → 5. **Model Evaluation**



# DVC and DVCLive Commands - Theoretical Overview

## DVC Repro Commands

### `dvc repro`

 **Purpose** : Reproduces DVC pipeline stages that have changed dependencies or outputs

* Automatically detects which stages need to be re-executed
* Only runs stages whose dependencies have changed
* Maintains data lineage and reproducibility
* Creates `.dvc/cache` entries for outputs

### `dvc repro --force`

 **Purpose** : Forces reproduction of all pipeline stages regardless of changes

* Ignores dependency checking
* Rebuilds entire pipeline from scratch
* Useful for troubleshooting or ensuring clean runs

### `dvc repro <stage-name>`

 **Purpose** : Reproduces only a specific pipeline stage

* Targets individual stages in the pipeline
* Runs dependencies if they've changed
* More granular control over execution

### `dvc repro --dry`

 **Purpose** : Shows what would be reproduced without actually running

* Preview mode for pipeline execution
* Displays which stages would run
* Helps verify pipeline logic before execution

## DVC Experiment Commands

### `dvc exp run`

 **Purpose** : Executes experiments with current parameters and tracks results

* Creates experiment branches in Git
* Tracks metrics, parameters, and artifacts
* Integrates with DVCLive for automatic logging

### `dvc exp run --set-param <param>=<value>`

 **Purpose** : Runs experiment with modified parameters

* Temporarily overrides parameter values
* Creates new experiment with different configuration
* Useful for hyperparameter tuning

### `dvc exp run --queue`

 **Purpose** : Queues experiments for batch execution

* Adds experiments to execution queue
* Allows scheduling multiple parameter combinations
* Enables parallel experiment execution

### `dvc exp run --name <experiment-name>`

 **Purpose** : Assigns custom name to experiment

* Creates identifiable experiment runs
* Easier experiment management and comparison
* Overrides auto-generated experiment names

### `dvc exp show`

 **Purpose** : Displays table of all experiments with metrics and parameters

* Tabular view of experiment results
* Compares metrics across different runs
* Shows parameter variations and outcomes

### `dvc exp list`

 **Purpose** : Lists all available experiments

* Shows experiment names and timestamps
* Helps navigate experiment history
* Identifies available experiments for comparison

### `dvc exp diff`

 **Purpose** : Compares experiments and shows differences

* Highlights parameter and metric changes
* Side-by-side comparison of experiments
* Identifies best performing configurations

### `dvc exp apply <experiment-name>`

 **Purpose** : Applies experiment results to workspace

* Restores workspace to experiment state
* Brings back specific model/data versions
* Switches between experiment configurations

### `dvc exp remove <experiment-name>`

 **Purpose** : Deletes specified experiments

* Cleans up experiment history
* Removes unwanted or failed experiments
* Manages storage space

### `dvc exp push <remote> <experiment-name>`

 **Purpose** : Pushes experiments to remote storage

* Shares experiments with team members
* Backs up experiment results
* Enables collaborative experiment tracking

### `dvc exp pull <remote> <experiment-name>`

 **Purpose** : Downloads experiments from remote storage

* Retrieves shared experiments
* Syncs experiment data across environments
* Enables distributed experimentation

## DVCLive Commands

### `dvc live init`

 **Purpose** : Initializes DVCLive in the current project

* Sets up experiment tracking infrastructure
* Creates necessary configuration files
* Prepares project for live experiment monitoring

### `dvc live show`

 **Purpose** : Displays live experiment metrics and status

* Real-time view of running experiments
* Shows current metrics and progress
* Monitors experiment execution

### `dvc live diff`

 **Purpose** : Compares live experiments

* Shows differences between active experiments
* Helps track experiment variations
* Provides real-time comparison capabilities

## Pipeline Management Commands

### `dvc dag`

 **Purpose** : Visualizes pipeline dependency graph

* Shows stage dependencies and relationships
* Identifies pipeline structure and flow
* Helps understand data lineage

### `dvc status`

 **Purpose** : Shows pipeline and data status

* Identifies changed files and dependencies
* Shows which stages need reproduction
* Provides workspace state overview

### `dvc pipeline show`

 **Purpose** : Displays pipeline structure and stages

* Lists all pipeline stages and their configurations
* Shows stage inputs, outputs, and commands
* Provides pipeline documentation

### `dvc stage add`

 **Purpose** : Adds new stage to DVC pipeline

* Defines stage dependencies and outputs
* Specifies commands and parameters
* Builds pipeline incrementally

## Data Management Commands

### `dvc add <file>`

 **Purpose** : Tracks large files/datasets with DVC

* Creates `.dvc` files for data tracking
* Moves data to DVC cache
* Enables version control for large files

### `dvc push`

 **Purpose** : Uploads data and models to remote storage

* Syncs local cache with remote storage
* Backs up tracked data and artifacts
* Enables data sharing across environments

### `dvc pull`

 **Purpose** : Downloads data and models from remote storage

* Retrieves data to local workspace
* Syncs remote changes to local environment
* Restores data from backups

### `dvc fetch`

 **Purpose** : Downloads data to cache without checkout

* Populates local cache from remote
* Prepares data for fast switching
* Pre-loads data for offline work

### `dvc checkout`

 **Purpose** : Updates workspace with cached data

* Restores files from DVC cache
* Switches between data versions
* Updates workspace to match Git commit

### `dvc import`

 **Purpose** : Imports data from external DVC repositories

* Creates dependency on external data
* Tracks external data versions
* Enables data sharing between projects

### `dvc update`

 **Purpose** : Updates imported data to latest version

* Refreshes external data dependencies
* Pulls updates from source repositories
* Maintains data currency

## Remote and Storage Commands

### `dvc remote add <name> <url>`

 **Purpose** : Configures remote storage location

* Sets up cloud storage backends
* Defines data storage destinations
* Enables multi-environment data sharing

### `dvc remote list`

 **Purpose** : Lists configured remote storage locations

* Shows available storage backends
* Displays remote configurations
* Helps manage storage settings

### `dvc remote modify <name> <option> <value>`

 **Purpose** : Modifies remote storage configuration

* Updates authentication settings
* Changes storage parameters
* Configures access permissions

### `dvc cache dir`

 **Purpose** : Shows or sets cache directory location

* Displays current cache location
* Allows cache directory customization
* Manages local storage usage
