import gradio as gr
import os
from datetime import datetime
import database as db
import engine as eng
from config import OUTPUT_DIR

db.init_db()
CURRENT_RECORD_ID = None

def run_studio_pipeline(user_prompt, art_style, lighting, framing, modifier):
    global CURRENT_RECORD_ID
    
    concepts = [c.strip() for c in user_prompt.split(";") if c.strip()]
    if not concepts:
        raise gr.Error("Please enter a valid core concept.")
        
    for concept in concepts:
        timestamp_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        timestamp_db = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        thoughts, expanded_prompt = eng.generate_agentic_prompt(concept, art_style, lighting, framing, modifier)
        
        try:
            img_obj = eng.generate_flux_image(expanded_prompt)
            saved_path = os.path.abspath(f"{OUTPUT_DIR}/art_{timestamp_id}.png")
            img_obj.save(saved_path)
            
            dominant_color, contrast_score = eng.analyze_image_properties(img_obj)
            
            CURRENT_RECORD_ID = db.insert_generation(
                timestamp_db, concept, art_style, lighting, framing, modifier, thoughts, expanded_prompt, saved_path, dominant_color, contrast_score
            )
        except Exception as e:
            raise gr.Error(f"Generation pipeline issue: {str(e)}")
            
    status_msg = f"🟢 Pipeline Successful. Dominant Color: {dominant_color} | Contrast Score: {contrast_score}"
    return img_obj, thoughts, expanded_prompt, saved_path, gr.update(value=status_msg)

def handle_feedback(rating):
    global CURRENT_RECORD_ID
    if CURRENT_RECORD_ID is None:
        return "*Error: No current session target.*"
    score = 1 if rating == "Good 👍" else 0
    db.update_reward(CURRENT_RECORD_ID, score)
    return f"Metric saved successfully! Score: {score}"

def refresh_studio_vault():
    items = db.get_all_records()
    return items, f"### Total Synchronized Vault Logs: {len(items)}"

def handle_gallery_inspection(evt: gr.SelectData):
    selected_label = evt.caption
    if not selected_label or "#" not in selected_label:
        return [gr.update()] * 9
    try:
        record_id = int(selected_label.split("|")[0].replace("#", "").strip())
        row = db.get_single_record(record_id)
        if row:
            status_text = "Good 👍" if row['human_reward'] == 1 else ("Bad 👎" if row['human_reward'] == 0 else "Unrated")
            meta_markdown = f"**Inspecting Archived Record #{row['id']}**\n* Preference Rating: `{status_text}`\n* Calculated Color Profile: `{row['dominant_color']}`\n* Root Mean Square Contrast: `{row['contrast_score']}`"
            
            # Interactive visualization preview box tracking color fields
            color_box_html = f"<div style='width:100%; height:40px; background-color:{row['dominant_color']}; border-radius:4px; border:1px solid #555;'></div>"
            
            return (
                row['core_concept'], row['art_style'], row['lighting'], row['framing'],
                row['agent_logic'], row['expanded_prompt'], row['image_path'], meta_markdown, color_box_html
            )
    except Exception:
        pass
    return [gr.update()] * 9

def handle_data_export():
    path = db.export_vault_to_csv()
    return path

# ==============================================================================
# VIEW INTERFACE CONFIGURATION
# ==============================================================================
with gr.Blocks(theme=gr.themes.Monochrome(radius_size="sm", font=["Courier New", "monospace"])) as demo:
    gr.Markdown("# 🧠 Advanced Agentic Art Studio v5.0 (Ultimate Generation Suite)")
    
    with gr.Tabs():
        with gr.Tab("Studio Control Dashboard"):
            with gr.Row():
                with gr.Column(scale=5):
                    user_input = gr.Textbox(label="1. Core Concept(s)", placeholder="A sleeping fox; A flying eagle...", lines=2)
                    with gr.Row():
                        style_input = gr.Dropdown(label="Artistic Style Preset", choices=["Cinematic Macro Photography", "Cyberpunk Neon", "Oil Painting", "Minimalist Vector Art", "Dark Fantasy Sketch", "Hyper-Detailed Anime Painting"], value="Cinematic Macro Photography")
                        lighting_input = gr.Dropdown(label="Lighting Configuration", choices=["Volumetric God Rays", "High-Contrast Chiaroscuro", "Cyberpunk Golden Hour", "Moody Soft Twilight", "Harsh Studio Flash", "Neon Bi-Color Rim Light"], value="Volumetric God Rays")
                        framing_input = gr.Dropdown(label="Lens Framing/Angle", choices=["Extreme Close-Up Macro", "Wide-Angle Dramatic Dutch Tilt", "Low-Angle Hero Shot", "Eye-Level Cinematic Frame", "Bird's-Eye Satellite View"], value="Low-Angle Hero Shot")
                    
                    modifier_input = gr.Dropdown(
                        label="3. Engine Rendering Modifiers (Hyper-Aesthetics)",
                        choices=["Octane Render, 8k Resolution, Unreal Engine 5 Style", "Vintage 35mm Film Grain, Kodachrome Profile", "Ray Tracing Global Illumination, Soft Textures", "Minimal Vector Path Elements, Clean Solid Fills"],
                        value="Ray Tracing Global Illumination, Soft Textures"
                    )
                    
                    generate_btn = gr.Button("Execute Agentic Loop", variant="primary")
                    gr.Markdown("### 📊 Explainable AI (XAI) Architecture Logs")
                    xai_thoughts = gr.Textbox(label="Director's System Reasoning Framework", interactive=False, lines=3)
                    xai_prompt = gr.Textbox(label="Autonomous Synthesized Prompt String", interactive=False, lines=4)
                    
                with gr.Column(scale=4):
                    output_img = gr.Image(label="Generated Pipeline Output Asset", type="pil")
                    download_file = gr.DownloadButton("Download Output Image", size="sm")
                    gr.Markdown("### 🤖 Reward Metric Tuning (RLHF)")
                    with gr.Row():
                        upvote_btn = gr.Button("Good 👍", variant="secondary")
                        downvote_btn = gr.Button("Bad 👎", variant="secondary")
                    rl_status = gr.Markdown("*Awaiting pipeline generation execution...*")
                    
        with gr.Tab("Studio Vault & History Hub") as history_tab:
            with gr.Row():
                vault_count = gr.Markdown("### Loading database references...")
                export_btn = gr.Button("📊 Export System Vault Logs to CSV", variant="secondary", size="sm")
                csv_download = gr.DownloadButton("Download CSV File", visible=False, size="sm")
            with gr.Row():
                with gr.Column(scale=1):
                    refresh_btn = gr.Button("Sync & Update History Hub", variant="secondary")
                    history_gallery = gr.Gallery(label="Synchronized Visual Matrix Logs", columns=2, height=600, interactive=False, allow_preview=True)
                with gr.Column(scale=1):
                    gr.Markdown("### 🔍 Historical Matrix Inspection Engine")
                    inspect_status = gr.Markdown("*Select a thumbnail image from the gallery matrix to reconstruct state...*")
                    color_preview = gr.HTML(label="Dominant Color Palette Strip")
                    h_concept = gr.Textbox(label="Archived Core Concept", interactive=False)
                    h_style = gr.Textbox(label="Archived Style Profile", interactive=False)
                    h_lighting = gr.Textbox(label="Archived Lighting Profile", interactive=False)
                    h_framing = gr.Textbox(label="Archived Lens Profile", interactive=False)
                    h_logic = gr.Textbox(label="Historical Director Logic", interactive=False, lines=3)
                    h_prompt = gr.Textbox(label="Historical Compiled Prompt String", interactive=False, lines=4)

    # Wireframes Event Actions 
    generate_btn.click(fn=run_studio_pipeline, inputs=[user_input, style_input, lighting_input, framing_input, modifier_input], outputs=[output_img, xai_thoughts, xai_prompt, download_file, rl_status])
    upvote_btn.click(fn=lambda: handle_feedback("Good 👍"), inputs=None, outputs=rl_status)
    downvote_btn.click(fn=lambda: handle_feedback("Bad 👎"), inputs=None, outputs=rl_status)
    
    refresh_btn.click(fn=refresh_studio_vault, inputs=None, outputs=[history_gallery, vault_count])
    history_tab.select(fn=refresh_studio_vault, inputs=None, outputs=[history_gallery, vault_count])
    history_gallery.select(fn=handle_gallery_inspection, inputs=None, outputs=[h_concept, h_style, h_lighting, h_framing, h_logic, h_prompt, output_img, inspect_status, color_preview])
    
    export_btn.click(fn=handle_data_export, inputs=None, outputs=csv_download)
    # Automatically show download button once compiled
    export_btn.click(fn=lambda: gr.update(visible=True), inputs=None, outputs=csv_download)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)