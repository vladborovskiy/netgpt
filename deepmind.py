import google.generativeai as ai


class DeepMind:

  def __init__(self, api_key):
    try:
      ai.configure(api_key=api_key)
      self.model = ai.GenerativeModel(model_name='gemini-pro')
      self.chat = self.model.start_chat(history=[])
    except Exception as e:
      print(f"!DeepMind init-error: {e}")

  def generate(self, prompt):
    try:
      response = self.chat.send_message(str(prompt))
      return response.text
    except Exception as e:
      print(f"!DeepMind error: {e}")
      return 'Ошибка генерации, попробуйте еще раз'
        
  
  def generate_content(self, promt):
    try:
      model = ai.GenerativeModel(model_name="gemini-pro-vision")
      response = model.generate_content(promt)
      return response.text
    except Exception as e:
      print(f"!DeepMind error: {e}")
      return 'Ошибка генерации, попробуйте ещё раз'

  def clear_history(self):
    try:
      self.chat = self.model.start_chat(history=[])
    except Exception as e:
      print(f"!DeepMind error: {e}")
      return 'Ошибка очистки истории, попробуйте ещё раз'
