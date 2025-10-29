import pandas as pd

def load_datasets():
    df_diagnosis = pd.read_parquet(
        'hf://datasets/NV9523/SVYKHOA/diagnosis/SVYKHOA_dataset_diagnosis.parquet'
    )
    df_guide = pd.read_parquet(
        'hf://datasets/NV9523/SVYKHOA/guide/SVYKHOA_dataset_guide.parquet'
    )
    df_medical_talk = pd.read_parquet(
        'hf://datasets/NV9523/SVYKHOA/medical_talk/SVYKHOA_dataset_medicaltalk.parquet'
    )
    df_small_talk = pd.read_parquet(
        'hf://datasets/NV9523/SVYKHOA/small_talk/SVYKHOA_dataset_smalltalk.parquet'
    )
    df_icd10 = pd.read_parquet(
        'hf://datasets/NV9523/SVYKHOA/icd10/SVYKHOA_dataset_icd10_mota.parquet'
    )

    return {
        "diagnosis": df_diagnosis,
        "guide": df_guide,
        "medical_talk": df_medical_talk,
        "small_talk": df_small_talk,
        "icd10": df_icd10
    }
