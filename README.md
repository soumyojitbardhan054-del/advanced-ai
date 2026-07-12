# Advanced Multi-API AI Assistant

A Streamlit chat app that supports multiple AI provider slots with automatic failover.

## Features
- Configure up to 20 API slots.
- Automatically moves to the next slot when one fails or times out.
- Global speed threshold to avoid slow providers.
- Advanced UI with slot management, metrics, and retry logs.
- Support for any API endpoint that accepts OpenAI-style chat payloads.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the sidebar.
2. Set the number of active API slots.
3. Enable and configure each slot with the endpoint, model, API key, and timeout.
4. Send a message in the chat box.
5. The app selects the fastest working provider and falls back automatically.

## Notes
- If your provider uses a different request shape than OpenAI-style `model/messages`, use a custom API gateway or wrapper.
- The app is designed to add more slots in the future without code changes.
