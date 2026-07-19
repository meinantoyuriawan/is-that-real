# KGAT_eb0256d05f216c36f623f539b184f176

import os
from dotenv import load_dotenv
import opendatasets as od
import pandas as pd
import weaviate
from weaviate.classes.config import Configure, Property, DataType
load_dotenv()

class Migration:

    def __init__(self):
        self.dataset_url = "https://www.kaggle.com/datasets/mochamadabdulazis/deteksi-berita-hoaks-indo-dataset/data"
        self.csv_path  = os.path.join("deteksi-berita-hoaks-indo-dataset/Cleaned Dataset V3/", "tbh_cleaned_v3.csv")
        self.client = weaviate.connect_to_local(
            headers={
                "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY") # For auto-vectorization
            }
        )

    def download_data_from_kaggle(self):
        print("Downloading dataset...")
        od.download(self.dataset_url)

    def load_dataframe_from_csv(self):
        print("Loading data into memory...")
        df = pd.read_csv(self.csv_path, nrows=1000) #limit to 1000 for a trial
        df = df.fillna("")

        return df

    def fill_data_to_vectorDB(self, dataframe):
        try:
            collection_name = "TurnBackHoax"

            if self.client.collections.exists(collection_name):
                self.client.collections.delete(collection_name)
                
            collection = self.client.collections.create(
                name=collection_name,
                vectorizer_config=Configure.Vectorizer.text2vec_openai(), 
                properties=[
                    Property(name="url", data_type=DataType.TEXT),
                    Property(name="judul", data_type=DataType.TEXT),
                    Property(name="clean_text", data_type=DataType.TEXT),
                ]
            )

            for idx, row in df.iterrows():
                properties = {
                        "url": str(row["url"]),
                        "judul": str(row["judul"]),
                        "clean_text": str(row["clean_text"])
                    }

                uuid_returned = collection.data.insert(properties=properties)
                print(f"[{idx+1}/{len(df)}] Successfully inserted object ID: {uuid_returned}")

            print("\nSuccess! All rows imported using single synchronous insertions.")
        finally:
            self.client.close()

if __name__ == "__main__":
    m = Migration()
    # m.download_data_from_kaggle()
    df = m.load_dataframe_from_csv()
    m.fill_data_to_vectorDB(df)
