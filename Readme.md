## 🧱 1. Initialize Git + DVC

| **Concept** | **Explanation**  | **Command**                  | **Files Created**                  |
| ----------------- | ---------------------- | ---------------------------------- | ---------------------------------------- |
| Version Control   | Git tracks code        | `git init`                       | `.git/`                                |
| DVC Init          | Set up DVC in the repo | `dvc init`                       | `.dvc/`,`.dvcignore`,`.dvc/config` |
| Save Config       | Track with Git         | `git commit -m "Init Git + DVC"` | Git commits                              |

---

## 📦 2. Add Raw Data to DVC

| **Concept** | **Explanation**                | **Command**                | **Files**                            |
| ----------------- | ------------------------------------ | -------------------------------- | ------------------------------------------ |
| Track large files | DVC tracks data files instead of Git | `dvc add data/raw.csv`         | `data/raw.csv.dvc`,`.gitignore`updated |
| Commit metadata   | Only pointer files go to Git         | `git add data/raw.csv.dvc`     | Version controlled                         |
| Save to history   |                                      | `git commit -m "Add raw data"` |                                            |

---

## 🧹 3. Prepare Script (`prepare.py`)

| **File**     | **Purpose**                      | **Code Snippet**                                                                                                  |
| ------------------ | -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `src/prepare.py` | Cleans raw data → saves clean version | `python<br>import pandas as pd, sys<br>df = pd.read_csv(sys.argv[1])<br>df.dropna().to_csv(sys.argv[2], index=False)` |

---

## 🧠 4. Training Script (`train.py`)

| **File**   | **Purpose**                        | **Code Snippet**                                                                                                                                                                                                                                                 |
| ---------------- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/train.py` | Trains a model → saves as `model.pkl` | `python<br>import pandas as pd, pickle, sys<br>from sklearn.linear_model import LinearRegression<br>df = pd.read_csv(sys.argv[1])<br>X = df[['feature']]<br>y = df['target']<br>model = LinearRegression().fit(X, y)<br>pickle.dump(model, open(sys.argv[2], 'wb'))` |

---

## 🔗 5. Build DVC Pipeline

| **Concept** | **Explanation** | **Command**                                                                                                            |
| ----------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Stage 1: prepare  | Raw → Clean          | `dvc run -n prepare -d src/prepare.py -d data/raw.csv -o data/clean.csv python src/prepare.py data/raw.csv data/clean.csv` |
| Stage 2: train    | Clean → Model        | `dvc run -n train -d src/train.py -d data/clean.csv -o model.pkl python src/train.py data/clean.csv model.pkl`             |
| Output Files      | Pipeline descriptor   | `dvc.yaml`,`dvc.lock`                                                                                                    |

---

## ⚙️ dvc.yaml Generated (Auto)

| **Stage** | **Command**                                     | **Deps**                      | **Outputs**  |
| --------------- | ----------------------------------------------------- | ----------------------------------- | ------------------ |
| `prepare`     | `python src/prepare.py data/raw.csv data/clean.csv` | `data/raw.csv`,`src/prepare.py` | `data/clean.csv` |
| `train`       | `python src/train.py data/clean.csv model.pkl`      | `data/clean.csv`,`src/train.py` | `model.pkl`      |

---

## 🔁 6. Reproduce Pipeline

| **Concept**   | **Explanation**                 | **Command** |
| ------------------- | ------------------------------------- | ----------------- |
| Re-run only changes | Automatically finds what needs update | `dvc repro`     |
| Full pipeline DAG   | Clean → Train → Model               |                   |

---

## ☁️ 7. Add Remote Storage

| **Concept** | **Explanation**         | **Command**(S3 Example)                          |
| ----------------- | ----------------------------- | ------------------------------------------------------ |
| Add remote        | Tell DVC where to store files | `dvc remote add -d myremote s3://mybucket/dvcstore`  |
| Auth setup        | Optional for private buckets  | `dvc remote modify myremote access_key_id <KEY>`etc. |
| Push data         | Push actual data and models   | `dvc push`                                           |

---

## 🔀 8. Commit Everything to Git

| **Item**          | **Command**                       | **Notes**     |
| ----------------------- | --------------------------------------- | ------------------- |
| Code,`dvc.yaml`, .dvc | `git add .`                           | Include all changes |
| Save history            | `git commit -m "Add pipeline stages"` |                     |
| Push code               | `git push origin main`                | Git-only, no data   |

---

## 📥 9. Collaborators Pull & Run

| **Step**     | **Command**        | **Effect**                 |
| ------------------ | ------------------------ | -------------------------------- |
| Clone repo         | `git clone <repo-url>` | Get code and metadata            |
| Pull data          | `dvc pull`             | Downloads actual datasets/models |
| Reproduce pipeline | `dvc repro`            | Re-runs any missing parts        |

---

## 📘 Example Project Tree After Setup

```
my_project/
├── data/
│   ├── raw.csv
│   └── clean.csv           <- generated
├── model.pkl               <- generated
├── src/
│   ├── prepare.py
│   └── train.py
├── dvc.yaml
├── dvc.lock
├── data/raw.csv.dvc
├── .gitignore
└── .dvc/
```

---

## 📊 Summary of Tools by Category

| **Area** | **Tool/Command**    | **Purpose**               |
| -------------- | ------------------------- | ------------------------------- |
| Versioning     | `git`,`dvc add`       | Track code and data             |
| Pipelines      | `dvc run`,`dvc.yaml`  | Define data > model steps       |
| Execution      | `dvc repro`             | Re-run only changed stages      |
| Collaboration  | `dvc push/pull`         | Sync large files                |
| Automation     | `dvc.yaml`,`dvc.lock` | Record dependencies and outputs |

## ✅ **DVC Commands Reference Table**

| **Command**                          | **Purpose**                                    | **Flags / Options**                                          | **Explanation**                                                                                                                                                               |
| ------------------------------------------ | ---------------------------------------------------- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dvc init`                               | Initialize DVC in a Git repo                         | `--subdir`                                                       | Sets up `.dvc/`and `.dvcignore`. Use `--subdir`if inside a subfolder of a Git repo.                                                                                           |
| `dvc add <file/dir>`                     | Track a data file or directory                       | `-f <file.dvc>`                                                  | Creates `.dvc`file and adds data to cache; updates `.gitignore`.`-f`sets custom output file.                                                                                  |
| `dvc run`                                | Define a pipeline stage                              | `-n <name>``-d <dependency>``-o <output>``-p <param>``--no-exec` | Runs a command and tracks its inputs/outputs in `dvc.yaml`.`-n`names the stage,`-d`lists dependencies,`-o`lists outputs.`--no-exec`creates the stage but skips execution. |
| `dvc repro`                              | Reproduce pipeline stages                            | `-f`,`--force``--dry`                                          | Re-runs stages that are out-of-date.`-f`forces re-run even if unchanged.`--dry`shows what*would*run.                                                                          |
| `dvc push`                               | Push data to remote storage                          | `-r <remote>``--jobs <n>`                                        | Uploads `.dvc`-tracked data files to remote.`-r`specifies the remote name,`--jobs`sets parallel uploads.                                                                      |
| `dvc pull`                               | Pull data from remote storage                        | `-r <remote>``--jobs <n>`                                        | Downloads data from remote to match current `.dvc`files.                                                                                                                          |
| `dvc fetch`                              | Get data from remote without placing it in workspace | `-r <remote>`                                                    | Downloads files into cache only. Does*not*restore them to workspace like `pull`.                                                                                                |
| `dvc status`                             | Show which stages/data are out of sync               | `-c``--cloud`                                                    | `-c`checks cache status,`--cloud`checks if remote has latest data.                                                                                                              |
| `dvc remote add <name> <url>`            | Add a remote storage backend                         | `-d`                                                             | Adds a named remote location.`-d`sets it as the default remote.                                                                                                                   |
| `dvc remote modify <name> <key> <value>` | Configure remote credentials                         | —                                                                 | Used to set access credentials or settings (e.g.,`access_key_id`,`secret_access_key`for S3).                                                                                    |
| `dvc remote list`                        | List all configured remotes                          | —                                                                 | Shows the names and URLs of remotes.                                                                                                                                                |
| `dvc remove <file.dvc>`                  | Stop tracking a file or directory                    | —                                                                 | Deletes the `.dvc`file and untracks the data.                                                                                                                                     |
| `dvc unprotect <file>`                   | Remove DVC protection (symlinks/readonly)            | —                                                                 | Restores normal file behavior (e.g., if you want to modify a `.dvc`file).                                                                                                         |
| `dvc gc`                                 | Garbage collect unused cache or remote data          | `--workspace`,`--cloud`,`--force`                            | Cleans up unused files.`--workspace`for local,`--cloud`for remote,`--force`required to actually delete.                                                                       |
| `dvc config`                             | View or set DVC config values                        | `--local`,`--global`,`--system`                              | Configure settings like remote URLs. Scope can be local (project), global (user), or system-wide.                                                                                   |
| `dvc checkout`                           | Restore files from DVC cache to workspace            | —                                                                 | Syncs the workspace to match the current `.dvc`or `dvc.lock`files.                                                                                                              |
| `dvc lock`                               | Manually lock pipeline stage                         | —                                                                 | Prevents `repro`from re-running this stage.                                                                                                                                       |
| `dvc unlock`                             | Unlock a stage                                       | —                                                                 | Allows `repro`to re-run it.                                                                                                                                                       |
| `dvc exp run`                            | Run a DVC experiment                                 | `--queue`,`--temp`,`--name`                                  | Tracks multiple experiments without affecting the main pipeline.                                                                                                                    |
| `dvc exp show`                           | List all experiments and metrics                     | —                                                                 | Tabular view of experiments with params and outputs.                                                                                                                                |
| `dvc exp apply <rev>`                    | Apply an experiment result to the workspace          | —                                                                 | Switch your workspace to match the chosen experiment.                                                                                                                               |
| `dvc metrics show`                       | Show tracked metrics                                 | `-T`,`--json`,`--csv`                                        | View metrics from JSON/YAML/text output files.                                                                                                                                      |
| `dvc params diff`                        | Compare parameter changes across revisions           | —                                                                 | Useful when using `params.yaml`for hyperparameters.                                                                                                                               |
| `dvc plots show`                         | Visualize plots (JSON, CSV)                          | `--json`,`--html`                                              | Used for line plots or other metrics across experiments.                                                                                                                            |

---

## 📝 Notes on File Types

| **File** | **Created by**  | **Purpose**                                  |
| -------------- | --------------------- | -------------------------------------------------- |
| `*.dvc`      | `dvc add`           | Pointer to large file (like `.git`)              |
| `dvc.yaml`   | `dvc run`           | Pipeline definition (commands, deps, outs)         |
| `dvc.lock`   | `dvc run`,`repro` | Exact versions and hashes for full reproducibility |
| `.dvcignore` | `dvc init`          | Like `.gitignore`for DVC cache<br />             |

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
