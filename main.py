import streamlit as st
import asyncio

async def generate_text_simulated(prompt, delay=1):
    # Simulating text generation by yielding chunks over time
    for i in range(1, 6):  # Example: Generate 5 chunks of text
        yield f"{prompt} response chunk {i}\n"
        await asyncio.sleep(delay)  # Simulate processing delay

def main():
    st.title("Async Text Generation Demo")

    prompt = st.text_input("Enter your prompt:", "Hello")

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