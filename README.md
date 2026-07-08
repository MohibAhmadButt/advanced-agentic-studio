# 🧠 Advanced Agentic Art Studio v5.0

An autonomous, full-stack AI Art Director dashboard that leverages **Gemini 2.5 Flash** for agentic prompt expansion and the **FLUX.1-schnell** image generation model through Hugging Face Inference API. The application includes a local **SQLite** database for image analytics, generation history, and reinforcement learning feedback.

---

## 🚀 Features

- **Agentic Prompt Expansion**  
  Converts simple user prompts into detailed, production-ready prompts using Gemini 2.5 Flash.

- **FLUX Image Generation**  
  Generates high-quality AI artwork using the FLUX.1-schnell model.

- **Batch Prompt Processing**  
  Generate multiple images by separating prompts with semicolons.

- **Image Analytics**  
  Automatically extracts dominant color palettes and grayscale contrast metrics using Pillow.

- **SQLite Studio Vault**  
  Stores prompts, generated images, metadata, timestamps, and analytics locally.

- **History & Reconstruction**  
  Browse previous generations and recreate images using historical prompts.

- **RLHF Feedback System**  
  Collect human preference feedback with simple **👍 Good** and **👎 Bad** ratings.

---

## 📂 Project Structure

```text
advanced-agentic-studio/
├── app.py
├── engine.py
├── database.py
├── config.py
├── requirements.txt
├── .env.example
├── LICENSE
└── README.md
```

---

## 🏗️ System Architecture

```text
User Prompt
      │
      ▼
Gemini 2.5 Flash
(Prompt Expansion)
      │
      ▼
FLUX.1-schnell
(Image Generation)
      │
      ▼
Image Analytics
(Color & Contrast)
      │
      ▼
SQLite Database
      │
      ▼
Gradio Dashboard
```

---

## 📦 Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12+ |
| Prompt Engineering | Gemini 2.5 Flash |
| Image Generation | FLUX.1-schnell |
| Interface | Gradio |
| Database | SQLite |
| Image Processing | Pillow |
| Environment Management | Python Virtual Environment |

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MohibAhmadButt/advanced-agentic-studio.git
cd advanced-agentic-studio
```

### 2. Create a Virtual Environment

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Variables

Create a `.env` file in the project root:

```env
HF_TOKEN=your_hugging_face_token
GEMINI_API_KEY=your_gemini_api_key
```

---

## ▶️ Run the Application

```bash
python app.py
```

---

## 📊 Database

The application uses a local SQLite database to store:

- Generated prompts
- Image metadata
- Dominant color palettes
- Contrast metrics
- Generation timestamps
- RLHF feedback

---

## 🤝 Contributing

Contributions are welcome.

Feel free to submit issues, feature requests, or pull requests to improve the project.

---

## 📄 License

This project is distributed under the MIT License.

See the **LICENSE** file for more information.

---

## 👨‍💻 Author

**Mohib Ahmad Butt**

Artificial Intelligence Student • AI/ML Engineer • Open Source Developer
