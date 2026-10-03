# 🎨 Text to Image Generator

An AI-powered **Text-to-Image Generator** built with **Python and Streamlit**. The application converts natural-language text prompts into images using AI image-generation models.

Users can enter a description of the image they want to create, select different styles and image dimensions, and generate an image directly from the web interface.

## 🚀 Live Demo

**[Try the Text to Image Generator](https://text-too-image-ac5l6spiqhh532b3tdak6e.streamlit.app/)**

---

## ✨ Features

* 📝 Generate images from text prompts
* 🤖 AI-powered image generation
* 🎨 Multiple image styles
* 📐 Different image sizes
* ⚡ Simple and interactive Streamlit interface
* 🖼️ Display generated images directly in the application
* 🌐 Deployable as a web application using Streamlit

---

## 🧠 How It Works

The application follows this workflow:

```text
User enters a text prompt
          ↓
Prompt processing
          ↓
AI Image Generation Model
          ↓
Image generation
          ↓
Generated image displayed
```

### Example

**Input prompt:**

```text
A futuristic city at sunset with flying cars
```

**Generated result:**

The AI model generates an image based on the description provided by the user.

---

## 🛠️ Technologies Used

| Technology                 | Purpose                 |
| -------------------------- | ----------------------- |
| 🐍 Python                  | Application development |
| 🎈 Streamlit               | Web interface           |
| 🤗 Hugging Face            | AI model inference      |
| 🧠 FLUX / Stable Diffusion | Image generation        |
| 🖼️ PIL                    | Image processing        |

---

## 📂 Project Structure

```text
Text-too-Image/
│
├── app.py
├── requirements.txt
└── README.md
```

### `app.py`

Contains the main Streamlit application and image-generation functionality.

### `requirements.txt`

Contains the Python packages required to run the application.

### `README.md`

Project documentation and setup instructions.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Shirishalanke/Text-too-image.git
```

Move into the project directory:

```bash
cd Text-too-image
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Hugging Face API Token

The application requires a **Hugging Face access token** to communicate with the image-generation model.

Create a `.env` file in the project directory:

```text
HF_TOKEN=your_huggingface_token
```

⚠️ **Never upload your real API token to GitHub.**

Add `.env` to your `.gitignore` file:

```text
.env
venv/
__pycache__/
*.pyc
```

---

## ▶️ Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will normally open at:

```text
http://localhost:8501
```

---

## 🎨 Image Generation

The application allows users to customize their generated images by selecting options such as:

* **Prompt** – Description of the desired image
* **Image style** – Different artistic styles
* **Image dimensions** – Different output sizes

The selected options are sent to the AI image-generation model, which produces the final image.

---

## 🌐 Deployment

The project is deployed using **Streamlit**.

### Live Application

**[Text to Image Generator](https://text-too-image-ac5l6spiqhh532b3tdak6e.streamlit.app/)**

The GitHub repository contains the source code used for the application:

**[GitHub Repository](https://github.com/Shirishalanke/Text-too-image)**

---

## 💡 Example Prompts

Try prompts such as:

```text
A beautiful mountain landscape during sunrise
```

```text
A futuristic robot walking through a neon city
```

```text
A cute golden retriever playing in a park
```

```text
A fantasy castle surrounded by magical forests
```

```text
A cyberpunk city at night with flying cars
```

---

## 🎯 Applications

Text-to-image generation can be useful for:

* 🎨 Digital art
* 🖼️ Creative design
* 📱 Social media content
* 📚 Educational illustrations
* 🎮 Game concept development
* 💡 Creative visualization
* 🧑‍🎨 AI-assisted artwork

---

## 🔮 Future Improvements

Possible future improvements include:

* 🎨 Adding more artistic styles
* 🖼️ Supporting image-to-image generation
* 📥 Adding an image download button
* 📝 Improving prompt enhancement
* 🌍 Supporting multiple languages
* ⚡ Improving generation speed
* 🔄 Adding image history
* 👤 Adding user accounts
* 📊 Displaying generation parameters

---

## 📸 Demo

### Text Prompt

```text
A futuristic city with flying cars, neon lights,
tall skyscrapers and a beautiful sunset
```

### Result

The application generates an AI-created image based on the entered prompt.

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new branch

```bash
git checkout -b feature/new-feature
```

3. Make your changes
4. Commit your changes

```bash
git commit -m "Add new feature"
```

5. Push the branch

```bash
git push origin feature/new-feature
```

6. Open a Pull Request

---

## 📄 License

This project is available under the **MIT License**.

---

## 👨‍💻 Author

**Shirish Alanke**

GitHub:
https://github.com/Shirishalanke

---

⭐ If you find this project useful, consider giving the repository a star!
