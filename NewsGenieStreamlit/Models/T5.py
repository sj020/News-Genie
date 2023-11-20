import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import gc

def T5(text):
    gc.enable()
    args = {
    "num_beams" : 4,
    "no_repeat_ngrams_size" : 3,
    "length_penalty" : 2,
    "min_length" : 30,
    "max_length" : 200,
    "early_stopping" : True
    }
    
    t5_model = T5ForConditionalGeneration.from_pretrained("t5-base")
    t5_tokenizer = T5Tokenizer.from_pretrained("t5-base")
    input_text = str(text).replace('\n', '')
    input_text = ' '.join(input_text.split())
    input_tokenized = t5_tokenizer.encode(input_text, return_tensors="pt")
    summary_task = torch.tensor([[21603, 10]])
    input_tokenized = torch.cat([summary_task, input_tokenized], dim=-1)
    summary_ids = t5_model.generate(input_tokenized, num_beams=args["num_beams"], 
                                      no_repeat_ngram_size=args["no_repeat_ngrams_size"], length_penalty=args["length_penalty"],
                                      min_length=args["min_length"], max_length=args["max_length"], 
                                      early_stopping=args["early_stopping"])
    output = [t5_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    del (t5_model,t5_tokenizer, input_text, input_tokenized, summary_task, summary_ids)
    gc.collect()
    return output
