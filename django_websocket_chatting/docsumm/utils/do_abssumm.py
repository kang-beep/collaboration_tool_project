from docsumm.utils.lazy_loader import LazyLoader


def do_abssumm(docs: str) -> str:
    lazy_loader = LazyLoader()
    bart_tokenizer = lazy_loader.get_kobart_tokenizer()
    bart_model = lazy_loader.get_kobart_model()
    
    inputs = bart_tokenizer(docs, return_tensors="pt", padding="max_length", truncation=True, max_length=1026)
    
    summary_text_ids = bart_model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        bos_token_id=bart_model.config.bos_token_id,
        eos_token_id=bart_model.config.eos_token_id,
        length_penalty=1.0,
        max_length=300,
        min_length=12,
        num_beams=6,
        repetition_penalty=1.5,
        no_repeat_ngram_size=15,
    )
    
    result = bart_tokenizer.decode(summary_text_ids[0], skip_special_tokens=True)
    
    return result