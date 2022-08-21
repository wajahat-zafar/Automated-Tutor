import pandas as pd
import gzip
from sklearn.model_selection import train_test_split
import os
from tqdm.auto import tqdm

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)

def getDF(path):
  i = 0
  df = {}
  for d in parse(path):
    df[i] = d
    i += 1
  return pd.DataFrame.from_dict(df, orient='index')

df1 = getDF('qa_Industrial_and_Scientific.json.gz')
df2 = getDF('meta_Industrial_and_Scientific.json.gz')

df = pd.merge(df1, df2, on="asin", how="left")
df = df[["question", "answer", "description"]]
df = df.dropna()
df = df.drop_duplicates(subset="answer")
print(df.head())

df.to_csv("Industrial_and_Scientific.tsv", "\t")

df = pd.read_csv("Industrial_and_Scientific.tsv", sep="\t")
df = df[["question", "description"]]
df["description"] = df["description"].apply(lambda x: x[2:-2])
df.columns = ["target_text", "input_text"]
df["prefix"] = "ask_question"

df.to_csv(f"data_all.tsv", "\t")

train_df, eval_df = train_test_split(df, test_size=0.05)

train_df.to_csv("train_df.tsv", "\t")
eval_df.to_csv("eval_df.tsv", "\t")




import pandas as pd

from simpletransformers.t5 import T5Model


train_df = pd.read_csv("train_df.tsv", sep="\t").astype(str)
eval_df = pd.read_csv("eval_df.tsv", sep="\t").astype(str)

model_args = {
    "reprocess_input_data": True,
    "overwrite_output_dir": True,
    "max_seq_length": 128,
    "train_batch_size": 8,
    "num_train_epochs": 1,
    "save_eval_checkpoints": True,
    "save_steps": -1,
    "use_multiprocessing": False,
    "evaluate_during_training": True,
    "evaluate_during_training_steps": 15000,
    "evaluate_during_training_verbose": True,
    "fp16": False,

    "wandb_project": "Question Generation with T5",
}

model = T5Model("t5", "t5-large", args=model_args)

model.train_model(train_df, eval_data=eval_df)
