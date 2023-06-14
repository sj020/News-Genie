# Importing the Libraries
import warnings
warnings.filterwarnings("ignore")
import pandas as pd
from fastai.text.all import *
from transformers import *
from blurr.text.data.all import *
from blurr.text.modeling.all import *
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")


# Getting the Data
df = pd.read_csv("Data/data_small.csv", nrows = 10)
df = df.dropna().reset_index()
df = df.drop('index', axis = 1)
df['full_text'] = df['full_text'].apply(lambda x: x.replace('\n',''))

## Configuration for BART Model for Summary
pretrained_model_name = "facebook/bart-large-cnn"
hf_arch, hf_config, hf_tokenizer, hf_model = get_hf_objects(pretrained_model_name, model_cls=BartForConditionalGeneration)
hf_batch_tfm = Seq2SeqBatchTokenizeTransform(hf_arch, hf_config, hf_tokenizer, hf_model, task='summarization',
    text_gen_kwargs={'max_length': 40,'min_length': 20,'do_sample': False, 'early_stopping': True, 'num_beams': 4, 'temperature': 1.0, 
                     'top_k': 50, 'top_p': 1.0, 'repetition_penalty': 1.0, 'bad_words_ids': None, 'bos_token_id': 0, 'pad_token_id': 1,
                     'eos_token_id': 2, 'length_penalty': 2.0, 'no_repeat_ngram_size': 3, 'encoder_no_repeat_ngram_size': 0,'num_return_sequences': 1, 
                     'decoder_start_token_id': 2, 'use_cache': True, 'num_beam_groups': 1, 'diversity_penalty': 0.0, 'output_attentions': False, 
                     'output_hidden_states': False, 'output_scores': False, 'return_dict_in_generate': False, 'forced_bos_token_id': 0, 'forced_eos_token_id': 2, 
                     'remove_invalid_values': False})


## BART Model for Summary
bart_model = BartForConditionalGeneration.from_pretrained(pretrained_model_name)
bart_tokenizer = BartTokenizer.from_pretrained(pretrained_model_name)

# BART Large
def BART_summary(input_text):
    blocks = (Seq2SeqTextBlock(batch_tokenize_tfm=hf_batch_tfm), noop)
    dblock = DataBlock(blocks=blocks, get_x=ColReader('full_text'), get_y=ColReader('synopsis'), splitter=RandomSplitter())
    dls = dblock.dataloaders(df, batch_size = 2)
    seq2seq_metrics = {
        'rouge': {
            'compute_kwargs': { 'rouge_types': ["rouge1", "rouge2", "rougeL"], 'use_stemmer': True },
            'returns': ["rouge1", "rouge2", "rougeL"]
        },
        'bertscore': {
            'compute_kwargs': { 'lang': 'en' },
            'returns': ["precision", "recall", "f1"]
        }
    }
    model = BaseModelWrapper(hf_model)
    learn_cbs = [BaseModelCallback]
    fit_cbs = [Seq2SeqMetricsCallback(custom_metrics=seq2seq_metrics)]

    learn = Learner(dls, model, opt_func=ranger, loss_func=CrossEntropyLossFlat(), cbs=learn_cbs, splitter=partial(blurr_seq2seq_splitter, arch=hf_arch))
    learn.load('BART')
    outputs = learn.blurr_generate(input_text, early_stopping=False, num_return_sequences=1)
    for idx, o in enumerate(outputs):
        return o['generated_texts']
    
def BART_headline(input_text):
    print("Getting the Headline 1......")
    input_text = str(input_text)
    input_text = ' '.join(input_text.split())
    input_tokenized = bart_tokenizer.encode(input_text, return_tensors='pt', max_length = 64)
    bart_model.resize_token_embeddings(len(bart_tokenizer))
    headline_ids = bart_model.generate(input_tokenized,num_beams= 5, no_repeat_ngram_size=1, length_penalty=2, min_length=3, max_length=30, early_stopping=True)
    output_headline = [bart_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False)for g in headline_ids]
    print("Returning the headline!!!!")
    output_headline = output_headline[0].split(".")[0].strip()
    return output_headline

def T5_Headline(input_text):        
    max_len = 256
    encoding = tokenizer.encode_plus(input_text, return_tensors = "pt")
    input_ids = encoding["input_ids"]
    attention_masks = encoding["attention_mask"]
    beam_outputs = model.generate(input_ids = input_ids, attention_mask = attention_masks, max_length = 64, num_beams = 3,early_stopping = True)
    result = tokenizer.decode(beam_outputs[0])
    result = result.replace("<pad>", "").replace("</s>", "")
    return result

def BERT_headline(input_text):
    tokenizer = AutoTokenizer.from_pretrained("patrickvonplaten/bert2bert_cnn_daily_mail")
    model = AutoModelForSeq2SeqLM.from_pretrained("patrickvonplaten/bert2bert_cnn_daily_mail")
    max_len = 256
    encoding = tokenizer.encode_plus(input_text, return_tensors = "pt", truncation=True)
    input_ids = encoding["input_ids"]
    attention_masks = encoding["attention_mask"]
    beam_outputs = model.generate(input_ids = input_ids,num_beams= 5, no_repeat_ngram_size=1, length_penalty=2, min_length=3, max_length=64, early_stopping=True)
    result = tokenizer.decode(beam_outputs[0])
    result = result.replace("[CLS]", "").replace("[SEP]", "")
    result = result.split(".")[0].strip()
    result = result.strip().capitalize() + '.'
    return result