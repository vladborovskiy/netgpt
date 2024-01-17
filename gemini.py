import google.generativeai as ai

ai.configure(api_key="AIzaSyCQyNOv4RcZF8os4wRUuRBNqabcROdIQKI")

def generate(aimodel, promt, streaming):
 
 if aimodel == "gemini-pro":
    model = ai.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content(promt, stream=streaming)
 elif aimodel == "gemini-pro-vision":
    model = ai.GenerativeModel(model_name="gemini-pro-vision")
    response = model.generate_content(promt, stream=streaming)
 elif aimodel == "embedding-001":
    model = ai.GenerativeModel(model_name="embedding-001")
    response = model.embed_Content(promt)
 else:
    model = ai.GenerativeModel(model_name="aqa")
    response = model.generate_Answer(promt)
 if streaming == True:
    return response
 else:
    truncated_response = response.text[:4093]
    if len(response.text) > 4093:
        truncated_response += "..."
    return truncated_response

def reset_context():
    model = ai.GenerativeModel(model_name="gemini-pro")
    model.generate_content("Сбрось наш диалог, начнем новый", stream=False)
