import json
import time
import base64
import requests
import os


class Text2ImageAPI:

  def __init__(self, url, api_key, secret_key):
    self.URL = url
    self.AUTH_HEADERS = {
        'X-Key': f'Key {api_key}',
        'X-Secret': f'Secret {secret_key}',
    }

  def get_model(self):
    response = requests.get(self.URL + 'key/api/v1/models',
                            headers=self.AUTH_HEADERS)
    data = response.json()
    return data[0]['id']

  def generate(self,
               prompt,
               model,
               images=1,
               width=1024,
               height=1024,
               style=3):
    styles = ["KANDINSKY", "UHD", "ANIME", "DEFAULT"]
    params = {
        "type": "GENERATE",
        "numImages": images,
        "width": width,
        "height": height,
        "style": styles[style],
        "generateParams": {
            "query": f"{prompt}"
        }
    }

    data = {
        'model_id': (None, model),
        'params': (None, json.dumps(params), 'application/json')
    }
    response = requests.post(self.URL + 'key/api/v1/text2image/run',
                             headers=self.AUTH_HEADERS,
                             files=data)
    data = response.json()
    return data['uuid']

  def check_generation(self, request_id, attempts=100, delay=1):
    while attempts > 0:
      response = requests.get(self.URL + 'key/api/v1/text2image/status/' +
                              request_id,
                              headers=self.AUTH_HEADERS)
      data = response.json()
      if data['status'] == 'DONE':
        return data['images']

      attempts -= 1
      time.sleep(delay)


def draw_image(promt, styling):
  try:
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/',
                        '708A87B4291A147605949F2396DE76A0',
                        'DFC98FECE12695B06675FF5EA2B30647')
    model_id = api.get_model()
    uuid = api.generate(str(promt), model_id, style=styling)
    images = api.check_generation(uuid)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)

    return image_data
  except Exception as e:
    print(f"!Fusionbrain error: {e}")
    return None
