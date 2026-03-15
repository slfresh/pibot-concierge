# PiBot Concierge: AI Hotel Assistant

PiBot Concierge is an intelligent, RAG-powered virtual hotel assistant designed to run on a **Raspberry Pi 5**. It provides a text-based chat interface allowing guests to ask questions about the hotel (check-in times, amenities, etc.).

To ensure fast and intelligent responses, the system connects over your local network to a powerful PC (e.g., equipped with an RTX 5080) running a local Large Language Model (LLM) via **LM Studio**.

## How It Works

This project uses **Retrieval-Augmented Generation (RAG)** to answer questions:

1. **Knowledge Base:** The hotel information is stored in a simple text file (`data/hotel_info.txt`).
2. **Vector Database:** When the server starts, it reads the text file, splits it into paragraphs, and stores them in a local ChromaDB vector database.
3. **Retrieval:** When a guest asks a question (e.g., "When is breakfast?"), the system queries ChromaDB to find the most relevant paragraphs from the knowledge base.
4. **Generation:** The retrieved context, along with the guest's question, is sent to your local AI model (running on LM Studio on your main PC). The AI reads the context and generates a polite, accurate response.

## Architecture

*   **Frontend:** A responsive HTML/CSS/JS web interface served via FastAPI.
*   **Backend:** Python + FastAPI running on the Raspberry Pi 5.
*   **Database:** ChromaDB (local embedded vector database).
*   **AI Engine:** LM Studio running on a separate high-end PC on the same local network.

---

## 🛠️ Installation & Setup Instructions

### Part 1: Setting up LM Studio on your Main PC (RTX 5080)

1. Download and install [LM Studio](https://lmstudio.ai/) on your main PC.
2. Search for and download an instruction-tuned model (e.g., `Meta-Llama-3-8B-Instruct.Q4_K_M.gguf` or similar).
3. Go to the **Local Server** tab in LM Studio (the `<->` icon on the left).
4. Load your downloaded model.
5. In the Server Settings on the right side:
   * **Crucial:** Ensure that **"Any (0.0.0.0)"** is checked under Server Configuration, or manually configure the "Bind Address" so that other devices on your network can access it.
   * By default, the port is `1234`.
6. Click **Start Server**.
7. Find your main PC's local IP address (e.g., by running `ipconfig` on Windows or `ip a` on Linux/Mac). Let's say it is `192.168.1.100`.

### Part 2: Setting up the Raspberry Pi 5

1. **Update your Pi:** Ensure your Raspberry Pi 5 is up to date:
   ```bash
   sudo apt update && sudo apt upgrade
   ```

2. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/pibot-concierge.git
   cd pibot-concierge
   ```

3. **Create a Virtual Environment:**
   It is highly recommended to use a virtual environment to manage dependencies on the Pi.
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies:**
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: ChromaDB may take a moment to install as it compiles its dependencies.)*

5. **Customize the Hotel Information:**
   Edit the file located at `data/hotel_info.txt` to include the specific details, rules, and amenities of your hotel.

### Part 3: Running the Assistant

Before starting the server on the Raspberry Pi, you need to tell it where to find your LM Studio server using an environment variable.

Replace `192.168.1.100` with the actual IP address of your RTX 5080 PC:

```bash
export LM_STUDIO_URL="http://192.168.1.100:1234/v1"
```

Now, start the FastAPI server using Uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

*The `--host 0.0.0.0` flag ensures the web interface can be accessed from any device on your network.*

### Part 4: Accessing the Concierge

Open a web browser on your phone, tablet, or another computer on the network, and navigate to:

```
http://<RASPBERRY_PI_IP_ADDRESS>:8000
```

You should see the chat interface! Ask it a question about the hotel, and the Raspberry Pi will securely retrieve the answer and stream it back via your RTX 5080 PC.
