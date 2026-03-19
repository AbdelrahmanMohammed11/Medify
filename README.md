# Medify

### Bridging the Gap Between Patients and the Right Specialists

---

## The Problem: The Healthcare Navigation Gap

In today's digital world, platforms like Vezeeta have made it easy to find and book appointments with doctors. However, a significant gap remains: **patients often don't know which type of medical specialist they need to see.**

This lack of knowledge leads to several issues:
*   **Wasted Time and Money:** Patients book appointments with a General Practitioner (GP) or the wrong specialist, only to be referred to another doctor, leading to multiple visits and payments.
*   **Delayed Treatment:** Seeking the wrong medical advice can delay proper diagnosis and treatment, potentially worsening the patient's condition.
*   **Increased Patient Anxiety:** The stress and confusion of not knowing where to turn for help adds a significant emotional burden to being unwell.

The core issue is a **knowledge gap**. Patients can describe their symptoms, but they lack the medical expertise to connect those symptoms to the correct medical specialty.

## The Idea: An Intelligent Symptom-to-Specialist Recommender

What if we could empower patients with a simple tool that acts as a preliminary guide?

The idea behind **Medify** is to create an intelligent, user-friendly platform that takes a patient's self-reported symptoms and recommends the most appropriate type of medical specialist to consult.

Instead of guessing or relying on generic web searches, the patient gets a data-driven recommendation, simplifying their healthcare journey from the very first step. Medify aims to be the "first stop" before a patient even starts searching for a specific doctor.

## The Solution: How Medify Works

Medify will bridge the healthcare navigation gap by providing a clear, simple, and effective solution through a three-step process:

1.  **Symptom Input:**
    *   A user-friendly interface allows the patient to enter their symptoms. This can be done through a simple search bar with auto-completion, a checklist of common symptoms, or a guided questionnaire (e.g., "Where do you feel pain? What other symptoms are you experiencing?").

2.  **Intelligent Analysis:**
    *   Behind the scenes, a smart algorithm analyzes the input symptoms. This engine maps the combination of symptoms to a comprehensive database of medical conditions and their corresponding specialties.
    *   For example, symptoms like "chest pain," "shortness of breath," and "dizziness" would be strongly correlated with the **Cardiology** specialty.

3.  **Clear Recommendation:**
    *   The platform provides a clear and direct recommendation, such as: "**You should consider seeing a Cardiologist.**"
    *   To further educate the user, the recommendation is accompanied by a brief explanation of what that specialist does and why their symptoms point in that direction.
    *   **Disclaimer:** A crucial part of the solution is a clear disclaimer stating that Medify is a guidance tool, **not a diagnostic tool**, and that consulting a certified medical professional is essential for an actual diagnosis.
## Requirements

- python 3.12 or later


### install Python using MiniConda

1) Download and install MiniConda from [here](https://www.anaconda.com/docs/getting-started/miniconda/main)

2) Create a new environment using following command:
```bash
$ conda create -n Medical-rag-app python 3.12
```

3) Activate the environment
```bash
$ conda activate Medical-rag-app
```

## Installation

```bash
$ pip install -r requirements.txt
```

#### setup the environment variables

``` bash
$ cp .env.example .env

```

set your environment variables in the `.env` file , Like `Chatbot APIs` values




## Run Docker Compose Services
```bash
$ cd docker
$ cp .env.example .env
```
- update `.env` with your credentials





## Run FastAPI Server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 500
```
