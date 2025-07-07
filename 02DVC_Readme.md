
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
| `.dvcignore` | `dvc init`          | Like `.gitignore`for DVC cache                   |
