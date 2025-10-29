from build_chromdb import insert_dataframe, datasets

def insert_all():
    # Diagnosis
    insert_dataframe(
        datasets["diagnosis"],
        collection_name="diagnosis",
        text_fields=["intruction", "question", "symptom", "diagnosis"],
        meta_fields=[
            'icd_10',
            'icd_10/title',
            "intruction", 
            "question", 
            "symptom", 
            "diagnosis",
            'document/title',
            'document/description',
            'cme/title',
            'cme/description'
        ]
    )

    # Guide
    insert_dataframe(
        datasets["guide"],
        collection_name="guide",
        text_fields=["intruction", "question", "answer"],
        meta_fields=[
            "intruction", 
            "question", 
            "answer",
            'document/title',
            'document/tool',
            'document/description',
            'cme/title',
            'cme/tool',
            'cme/description'
        ]
    )

    # Medical Talk
    insert_dataframe(
        datasets["medical_talk"],
        collection_name="medical_talk",
        text_fields=["intruction", "question", "answer"],
        meta_fields=["intruction", "question", "answer"]
    )

    # Small Talk
    insert_dataframe(
        datasets["small_talk"],
        collection_name="small_talk",
        text_fields=["intruction", "question", "answer"],
        meta_fields=["intruction", "question", "answer"]
    )

    insert_dataframe(
        datasets["icd10"],
        collection_name="icd10",
        text_fields=["mô tả"],
        meta_fields=["MÃ BỆNH", "TÊN BỆNH", "mô tả"]
    )

    print("Inserted ChromDB")
if __name__ == "__main__":
    insert_all()