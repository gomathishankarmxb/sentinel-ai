# 🛡️ Project Sentinel AI: Backend Architecture

## 1. Overview
**Project Sentinel AI** is a real-time security monitoring backend designed to detect suspicious objects (weapons, intruders) using computer vision. It is built to be lightweight enough for edge deployment but powerful enough for high-accuracy surveillance.

---

## 2. The Tech Stack
| Component          | Technology                                   |
|:-------------------|:---------------------------------------------|
| **OS** | Ubuntu 24.04 LTS                             |
| **Language** | Python 3.12+                                 |
| **Web Framework** | FastAPI (High-performance, asynchronous API) |
| **AI Engine** | YOLOv8 (Ultralytics)                        |
| **Image Library** | OpenCV & Pillow                              |
| **Server** | Uvicorn (ASGI)                               |

---

## 3. System Components

### A. The API Layer (`testing.py`)
Acts as the **gatekeeper**. It receives images via `POST` requests, manages the lifecycle of the AI model, and formats the final alerts into JSON for the frontend/user.

### B. The Inference Engine (YOLOv8)
The **"Brain"** of the project. It uses a pre-trained neural network to identify objects in milliseconds. It calculates the probability ($P$) that an object belongs to a specific class.

### C. The Logic Controller
A filtering layer that decides if a detection is a "threat" based on:
* **Thresholding:** Only alerts if `Confidence > 0.5` (50%).
* **Classification:** Specifically filters for items in the `SUSPICIOUS_CLASSES` list.

---

## 4. Data Flow Path

1.  **Ingestion:** A client sends a raw image to the `/analyze` endpoint.
2.  **Preprocessing:** Image is converted from a Byte stream into a NumPy array.
3.  **Inference:** The AI model processes the pixels using the function:
    $$Y = f(x, w) + b$$
    *(Where $x$ is image data, $w$ are model weights, and $Y$ is the prediction)*.
4.  **Filtering:** System checks results against the "Threat List."
5.  **Response:** The backend returns a structured JSON object:

```json
{
  "alert": true,
  "detections": [
    {
      "object": "knife", 
      "conf": 0.92
    }
  ],
  "message": "Suspicious activity detected!"
}