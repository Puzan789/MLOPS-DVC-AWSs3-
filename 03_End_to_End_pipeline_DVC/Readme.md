1.  create and end to end ML pipeline
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
