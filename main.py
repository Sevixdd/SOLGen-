import streamlit as st
import asyncio
import scipy

from transformers import AutoTokenizer, AutoModelForTextToWaveform

async def generate_text_simulated(prompt, delay=1):
    # Simulating text generation by yielding chunks over time
    for i in range(1, 6):  # Example: Generate 5 chunks of text
        yield f"{prompt} response chunk {i}\n"
        await asyncio.sleep(delay)  # Simulate processing delay

def main():
    st.title("Async Text Generation Demo")

    prompt = st.text_input("Enter your prompt:", "Hello")


    tokenizer = AutoTokenizer.from_pretrained("facebook/musicgen-medium")
    model = AutoModelForTextToWaveform.from_pretrained("facebook/musicgen-medium")
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
    logits.shape  # (bsz * num_codebooks, tgt_len, vocab_size)


    sampling_rate = model.config.audio_encoder.sampling_rate
    scipy.io.wavfile.write("musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())
    if st.button("Generate"):
        text_placeholder = st.empty()
        text_placeholder.text("Generating response...")

        # Run the async text generation in a separate thread
        import threading
        def run_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            async def update_text():
                generated_text = ""
                async for chunk in generate_text_simulated(prompt, 0.5):
                    generated_text += chunk
                    text_placeholder.text(generated_text)

            loop.run_until_complete(update_text())

        threading.Thread(target=run_async).start()

if __name__ == "__main__":
    main()  