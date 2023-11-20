from transformers import BartTokenizer, BartForConditionalGeneration
import gc

def Bart(text):
    gc.enable()
    args = {
    "num_beams" : 4,
    "no_repeat_ngrams_size" : 3,
    "length_penalty" : 1,
    "min_length" : 12,
    "max_length" : 128,
    "early_stopping" : True
    }
    
    bart_model = BartForConditionalGeneration.from_pretrained("facebook/bart-base")
    bart_tokenizer = BartTokenizer.from_pretrained("facebook/bart-base")

    # Coverting the text inputed by user to string format
    input_text = str(text)

    # Splitting the text based spaces
    input_text = ' '.join(input_text.split())

    # Tokenizing the text using pretrained tokenizer
    input_tokenized = bart_tokenizer.encode(input_text, return_tensors = 'pt')
    
    # Generating the summary id's
    summary_ids = bart_model.generate(input_tokenized, num_beams=args["num_beams"], 
                                      no_repeat_ngram_size=args["no_repeat_ngrams_size"], length_penalty=args["length_penalty"],
                                      min_length=args["min_length"], max_length=args["max_length"], 
                                      early_stopping=args["early_stopping"])
    
    # Output
    output = [bart_tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
    del (bart_model, bart_tokenizer, input_text, input_tokenized, summary_ids)
    gc.collect()
    return output


