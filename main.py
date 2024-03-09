import streamlit as st
import scipy

from transformers import AutoProcessor, MusicgenForConditionalGeneration
import torch

@st.cache_resource
def get_model():    
        processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

        inputs = processor(
            text=["80s pop track with bassy drums and synth", "90s rock song with loud guitars and heavy drums"],
            padding=True,
            return_tensors="pt",
        )
    
        pad_token_id = model.generation_config.pad_token_id


        decoder_input_ids = (
            torch.ones((inputs.input_ids.shape[0] * model.decoder.num_codebooks, 1), dtype=torch.long)
            * pad_token_id
        )

        logits = model(**inputs, decoder_input_ids=decoder_input_ids).logits
        logits.shape


        #sampling_rate = model.config.audio_encoder.samplingfrom transformers import AutoProcessor, MusicgenForConditionalGeneration_rate
        #scipy.io.wavfile.write("musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())

def main():
    st.title("Async Text Generation Demo")

    st.text_input("Enter your prompt:", "Hello")
    
    st.button("Get Model", on_click=get_model)
    


if __name__ == "__main__":
    main()  
    