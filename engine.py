import io
from PIL import Image, ImageStat
from huggingface_hub import InferenceClient
from google import genai
from config import HF_TOKEN, GEMINI_API_KEY

hf_client = InferenceClient(api_key=HF_TOKEN)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

def generate_agentic_prompt(user_prompt, art_style, lighting, framing, modifier):
    """Leverages Gemini to blend concepts alongside raw style modifier configurations."""
    reasoning_prompt = f"""
    You are an expert AI Art Director. The user wants to create an image of: "{user_prompt}".
    Technical Design Constraints:
    - Artistic Presets: Style = {art_style}, Light Rendering Profile = {lighting}, Lens Framing = {framing}.
    - Hard Render Token Engine: Apply the aesthetic properties of {modifier} smoothly into the theme.
    Respond ONLY in the following strict format:
    THOUGHTS: Write 2 short sentences explaining how you are combining this lighting, framing, and concept cleanly.
    EXPANDED_PROMPT: Write a highly detailed, descriptive 1-paragraph prompt for an image generator based on your choices. Include specific elements of light, angle, and atmosphere. Do not use generic buzzwords like 'photorealistic'.
    """
    try:
        response = gemini_client.models.generate_content(model='gemini-2.5-flash', contents=reasoning_prompt)
        llm_response = response.text
        response_upper = llm_response.upper()
        
        if "THOUGHTS:" in response_upper and "EXPANDED_PROMPT:" in response_upper:
            idx_thoughts = response_upper.find("THOUGHTS:")
            idx_expanded = response_upper.find("EXPANDED_PROMPT:")
            return llm_response[idx_thoughts + len("THOUGHTS:"):idx_expanded].strip(), llm_response[idx_expanded + len("EXPANDED_PROMPT:"):].strip()
    except Exception as e:
        print(f"Gemini API issue: {e}")
        
    return "Fallback active.", f"{user_prompt}, {art_style} style, {lighting}, {framing}, {modifier}, detailed composition"

def generate_flux_image(final_prompt):
    response_data = hf_client.text_to_image(final_prompt, model="black-forest-labs/FLUX.1-schnell")
    if isinstance(response_data, Image.Image):
        return response_data
    return Image.open(io.BytesIO(response_data))

def analyze_image_properties(img_obj):
    """Computes lightweight pixel analytics metrics completely on CPU in milliseconds."""
    thumbnail = img_obj.resize((1, 1))
    pixel = thumbnail.getpixel((0, 0))
    dominant_hex = f"#{pixel[0]:02x}{pixel[1]:02x}{pixel[2]:02x}"
    
    stat = ImageStat.Stat(img_obj.convert("L"))
    contrast_score = round(stat.stddev[0], 2)
    
    return dominant_hex, contrast_score