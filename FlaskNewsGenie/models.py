from summarizer import Summarizer,TransformerSummarizer
from transformers import BartForConditionalGeneration, BartTokenizer, AutoModelForSeq2SeqLM, AutoTokenizer, T5ForConditionalGeneration, T5Tokenizer


# Loading all models once and not loading again 

## BART Model & Tokenizer for Synopsis
bart_model_synopsis = BartForConditionalGeneration.from_pretrained("fine_tuned_bart_large_synopsis/")
bart_tokenizer_synopsis = BartTokenizer.from_pretrained("fine_tuned_bart_large_synopsis/")

## BART Model & Tokenizer for Headline
bart_model_headline = BartForConditionalGeneration.from_pretrained("fine_tuned_bart_large_headline/")
bart_tokenizer_headline = BartTokenizer.from_pretrained("fine_tuned_bart_large_headline/")

## BERT Model & Tokenizer for Headline
bert_model_headline = AutoModelForSeq2SeqLM.from_pretrained("patrickvonplaten/bert2bert_cnn_daily_mail")
bert_tokenizer_headline = AutoTokenizer.from_pretrained("patrickvonplaten/bert2bert_cnn_daily_mail")

## T5 Model & Tokenizer for Headline
t5_model_headline = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
t5_model_tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")


# Generating BART Summary
def BART_Summary(article):
    # Tokenize the Input
    input_ids = bart_tokenizer_synopsis.encode(article, truncation=True, padding=True, return_tensors='pt')
    # Generate the Summary
    summary_ids = bart_model_synopsis.generate(input_ids, max_length = 40, min_length = 20, top_k = 50, top_p = 1, 
                                               no_repeat_ngram_size = 3, length_penalty = 2.0, num_beams=4)
    # Decode the Summary
    summary = bart_tokenizer_synopsis.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Generating BART Headline - 1
def BART_headline(article):
    # Tokeninze the Input
    input_ids = bart_tokenizer_synopsis.encode(article, truncation=True, padding=True, return_tensors='pt')
    # Generate the Summary
    article_ids = bart_model_synopsis.generate(input_ids, min_length = 3,max_length = 30, length_penalty = 2.0, 
                                               num_beams = 5, no_repeat_ngram_size = 1)
    # Decode the Summary
    headline = bart_tokenizer_synopsis.decode(article_ids[0], skip_special_tokens=True)
    return headline

# Generating BART Headline - 2
def BERT_headline(input_text):
    encoding = bert_tokenizer_headline.encode_plus(input_text, return_tensors = "pt", truncation=True)
    input_ids = encoding["input_ids"]
    # attention_masks = encoding["attention_mask"]
    beam_outputs = bert_model_headline.generate(input_ids = input_ids,num_beams= 5, no_repeat_ngram_size=1, 
                                                length_penalty=2, min_length=3, max_length=64, early_stopping=True)
    result = bert_tokenizer_headline.decode(beam_outputs[0])
    result = result.replace("[CLS]", "").replace("[SEP]", "")
    result = result.split(".")[0].strip()
    result = result.strip().capitalize() + '.'
    return result

# Generating T5 Headline - 3
def T5_Headline(input_text):        
    encoding = t5_model_tokenizer.encode_plus(input_text, return_tensors = "pt", truncation = True)
    input_ids = encoding["input_ids"]
    attention_masks = encoding["attention_mask"]
    beam_outputs = t5_model_headline.generate(input_ids = input_ids, attention_mask = attention_masks, max_length = 64, 
                                              num_beams = 3,early_stopping = True)
    result = t5_model_tokenizer.decode(beam_outputs[0])
    result = result.replace("<pad>", "").replace("</s>", "")
    return result