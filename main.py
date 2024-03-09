import streamlit as st
import scipy
from streamlit_card import card
from st_audiorec import st_audiorec

from transformers import AutoProcessor, MusicgenForConditionalGeneration
import torch
import streamlit as st 

def get_model():    
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")

    return processor,model
        #sampling_rate = model.config.audio_encoder.samplingfrom transformers import AutoProcessor, MusicgenForConditionalGeneration_rate
        #scipy.io.wavfile.write("musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())

#def inference(processor, model):
     
    

def create_card(user_id,name):
    st.markdown(
        f"""
        <div style="width: 300px; height: 300px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.5); padding: 20px; position: relative; text-align: center;">
            <h2 style="font-family: serif;">User ID: {user_id}</h2>
            <p>{name}</p>
            <button style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); padding: 10px 20px; border-radius: 5px; background-color: #4CAF50; color: white; font-size: 16px; cursor: pointer; border: none;">Click Me</button>
        </div>
        """,
        unsafe_allow_html=True
    )



def main():
    st.set_page_config(
         page_title="SolGenAI",
         page_icon=":)"
    )
    st.title("SolGenAI")
    
    # Initialize dictionaries to store unique user IDs and names
    unique_users = {}

    # Check if user_ids and names exist in the session_state
    if "user_ids" in st.session_state and "names" in st.session_state:
        user_ids = st.session_state["user_ids"]
        names = st.session_state["names"]
        
        st.write("User IDs and Names:")
        for user_id, name in zip(user_ids, names):
            # Check if the user ID is not already present in the unique_users dictionary
            if user_id not in unique_users:
                unique_users[user_id] = name
                create_card(user_id, name)


    else:
        st.write("No user IDs and names created yet.")
    
    # with open('style.css') as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    processor, model = get_model()

    #st.button("Inference", on_click=inference(processor,model))
    
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
    print(logits.shape)

    with st.spinner("waiting"):
        st.markdown(logits.shape)
        

if __name__ == "__main__":
    main()  
    