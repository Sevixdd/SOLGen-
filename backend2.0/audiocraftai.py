import torch
#import os
import scipy
import torchaudio
from flask import Flask, redirect, url_for, request, jsonify
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
from flask_cors import CORS
from subprocess import PIPE, run


model = MusicGen.get_pretrained('facebook/musicgen-small')


app = Flask(__name__)
cors = CORS(app)

# POST /api/generate/ # curl -X POST -d '{"prompt": "happy rock"}' -H "Content-Type: application/json" localhost:8081/api/generate/;
@app.route('/api/generate/', methods=['POST'])
def generate():
    if (request.method == 'POST'):
        data = request.json
        prompt = data['prompt']
        inference(prompt)
    return 'DONE'

# GET /api/upload/ # curl -X GET localhost:8081/api/upload/
@app.route('/api/upload/', methods=['GET'])
def upload():
    if (request.method == 'GET'):
        # trigger_minting
        command = ['sh', '-c', './upload.sh']
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True)
        out = result.returncode, result.stdout, result.stderr
        print("type: ", len(out))
        print("Index 0: ", out[0])
        print("Index 1 ", out[1])
        print("Index 2: ", out[2])
    return 'UPLOAD_DONE'

def inference(prompt):

    model.set_generation_params(duration=10)  # generate 8 seconds.
    #wav = model.generate_unconditional(2)    # generates 4 unconditional audio samples
    descriptions = [prompt]
    wav = model.generate(descriptions)  # generates 3 samples.
#'happy rock',' Create a bold and heroic music piece that captures the essence of a superheros journey. Start with a strong, memorable motif that can be associated with the hero, using brass and percussion for strength and determination. Incorporate rising strings and choir for moments of triumph and adversity, providing a dynamic backdrop for battles and the heros moral journey.'
   # melody, sr = torchaudio.load('./assets/file.wav')
# generates using the melody from the given audio and the provided descriptions.
   # wav = model.generate_with_chroma(descriptions, melody[None].expand(1, -1, -1), sr)

    for idx, one_wav in enumerate(wav):
        # Will save under {idx}.wav, with loudness normalization at -14 db LUFS.
        audio_write(f'assets/{idx}', one_wav.cpu(), model.sample_rate, strategy="loudness", make_parent_dir = True,loudness_compressor=True)
        #print(res)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8081, debug = True)
