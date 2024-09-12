# Clinical Psychology Intake Interview Chatbot

![Cute robot logo for Therabot.](/static/logo.png)

## Overview

This repository contains a chatbot designed to assist clinical psychology students in practicing and improving their initial intake interview skills. The chatbot simulates a patient, providing realistic responses to help students learn how to conduct effective initial assessments.

## Purpose

The primary goals of this chatbot are to:

1. Provide a safe, low-stakes environment for students to practice intake interviews
2. Offer varied patient scenarios to expose students to different clinical presentations
3. Give immediate feedback on interview techniques and question choices
4. Help students develop confidence in their interviewing skills before working with real patients

## Features

- Simulates patient profiles with various psychological conditions
- Responds dynamically to student questions, mimicking realistic patient behavior
- Provides feedback on interview structure and question appropriateness
- Allows for multiple conversation paths based on student choices
- Includes a scoring system to evaluate student performance

## Technical Stack

- Backend: FastAPI (Python)
- Frontend: HTML, CSS, JavaScript
- NLP Model: Anthropic's Claude API

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/clinical-psychology-chatbot.git
   cd clinical-psychology-chatbot
   ```

2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your Anthropic API key:
   - Sign up for an account at [Anthropic's website](https://www.anthropic.com)
   - Obtain your API key from the dashboard

4. Run the application:
   ```
   python therabot.py --api-key YOUR_ANTHROPIC_API_KEY
   ```

5. Open a web browser and navigate to `http://localhost:8000` to access the chatbot interface.

## Usage

1. Start a new session by opening the chatbot interface in your web browser.
2. You will be presented with a brief scenario describing the patient you'll be interviewing.
3. Type your questions or responses in the chat input field.
4. The chatbot will respond as the patient, providing realistic answers based on the scenario.
5. Continue the interview, asking appropriate intake questions and gathering relevant information.
6. At the end of the session, you'll receive feedback on your performance and areas for improvement.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This chatbot is designed for educational purposes only and should not be used as a substitute for real clinical experience or supervision. Always consult with qualified instructors and supervisors in your clinical psychology program for guidance on conducting actual patient interviews.