#from typing import Union

import torch
#import os
import scipy
from flask import Flask, redirect, url_for, request, jsonify
from transformers import AutoProcessor, MusicgenForConditionalGeneration

#from IPython.display import Audio
#from flask import request, jsonify
#from app import app
app = Flask(__name__)

# MODEL_NAME = 'facebook/musicgen-small'  # Adjust model name if necessary
# processor = AutoProcessor.from_pretrained(MODEL_NAME)
# model = AutoModelForTextToWaveform.from_pretrained(MODEL_NAME)

@app.route('/api/generate/', methods=['POST'])
def generate():
  if (request.method == 'POST'):
    data = request.json
    prompt = data['prompt']
    print('calling the ai with the folloing: ', prompt)
    result = inference_model(prompt)
    if (result == 1):
      print('DONE! ALL GOOD!')
    return 'something'



# audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=256)

#print( type(audio_values) )

print("DONE")

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
  
def inference_model(prompt):
 #model.set_generation_params(duration=10)
  print(model.generation_config)
  inputs = processor(
    text=[prompt],
    padding=True,
    return_tensors="pt",
  )

  audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=256)

  print( type(audio_values) )
  sampling_rate = model.config.audio_encoder.sampling_rate
  res = scipy.io.wavfile.write("musicgen_out.wav", rate=sampling_rate, data=audio_values[0, 0].numpy())
  print(type(res))

  return 1




def inference(processor):
  
  inputs = processor(
    text=["80s pop track with bassy drums and synth"],
    padding=True,
    return_tensors="pt",
  )

  music_tokens = model.generate(input_ids, max_length=300)

    # Here, you'd convert the tokens or output into a playable audio format
    # This will vary greatly depending on the model and expected output format
    # For demonstration, we'll just return the token IDs (this is NOT the final audio)
    # In practice, you should replace this with proper conversion to audio file
  music_output = music_tokens.tolist()[0]
  filename = 'output.mid' or 'output.mp3'
  with open(filename, 'wb') as audio_file:
      audio_file.write(convert_tokens_to_audio(music_output))
  return send_file(filename, as_attachment=True)

  print("music generated")


  return jsonify({'music_tokens': music_output})





if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug = True)
