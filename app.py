import streamlit as st
import requests
import time
from typing import Dict, List, Optional

DEFAULT_SLOTS = 9
MAX_SLOTS = 20

st.set_page_config(
    page_title="Advanced Multi-API AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "conversation" not in st.session_state:
    st.session_state.conversation = []

if "api_slots" not in st.session_state:
    st.session_state.api_slots = [
        {
            "active": False,
            "label": f"API Slot {i + 1}",
            "key": "",
            "endpoint": "https://api.openai.com/v1/chat/completions",
            "model": "gpt-4o-mini",
            "timeout": 10,
        }
        for i in range(DEFAULT_SLOTS)
    ]

if "last_status" not in st.session_state:
    st.session_state.last_status = "No requests sent yet."

if "last_api_index" not in st.session_state:
    st.session_state.last_api_index = None

if "failover_history" not in st.session_state:
    st.session_state.failover_history = []

if "stats" not in st.session_state:
    st.session_state.stats = {
        "requests": 0,
        "successful": 0,
        "failed": 0,
        "timeouts": 0,
        "slow_responses": 0,
    }


def ensure_slot_count(count: int) -> None:
    if count > len(st.session_state.api_slots):
        for i in range(len(st.session_state.api_slots), count):
            st.session_state.api_slots.append(
                {
                    "active": False,
                    "label": f"API Slot {i + 1}",
                    "key": "",
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "model": "gpt-4o-mini",
                    "timeout": 10,
                }
            )
    elif count < len(st.session_state.api_slots):
        st.session_state.api_slots = st.session_state.api_slots[:count]


def format_response_json(data: Dict) -> str:
    if not isinstance(data, dict):
        return ""
    if choices := data.get("choices"):
        first = choices[0]
        if isinstance(first, dict):
            if message := first.get("message"):
                return message.get("content", "")
            if output_text := first.get("text"):
                return output_text
    if output := data.get("output"):
        if isinstance(output, str):
            return output
        if isinstance(output, list):
            return "\n".join(output)
    return ""


def fetch_ai_response(
    prompt_messages: List[Dict[str, str]],
    active_slots: List[Dict[str, object]],
    speed_threshold: int,
) -> Optional[str]:
    st.session_state.stats["requests"] += 1

    for index, api in enumerate(active_slots, start=1):
        slot_label = api.get("label", f"API Slot {index}")
        st.sidebar.info(f"Trying {slot_label}...")

        endpoint = api["endpoint"].strip()
        api_key = api["key"].strip()
        model = api["model"].strip()
        timeout = int(api["timeout"])
        request_timeout = min(timeout, speed_threshold) if speed_threshold > 0 else timeout

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": prompt_messages,
        }

        try:
            start_time = time.time()
            response = requests.post(endpoint, headers=headers, json=payload, timeout=request_timeout)
            elapsed = time.time() - start_time

            if response.status_code != 200:
                st.session_state.failover_history.append(
                    f"{slot_label} failed with status {response.status_code}."
                )
                st.session_state.stats["failed"] += 1
                continue

            content = format_response_json(response.json())
            if not content:
                st.session_state.failover_history.append(
                    f"{slot_label} returned an unexpected response shape."
                )
                st.session_state.stats["failed"] += 1
                continue

            st.session_state.last_api_index = index
            st.session_state.last_status = f"{slot_label} succeeded in {elapsed:.2f}s"
            st.session_state.stats["successful"] += 1

            if speed_threshold > 0 and elapsed > speed_threshold:
                st.session_state.stats["slow_responses"] += 1
                st.session_state.failover_history.append(
                    f"{slot_label} responded slowly ({elapsed:.2f}s), but still returned an answer."
                )

            return content

        except requests.exceptions.Timeout:
            st.session_state.stats["timeouts"] += 1
            st.session_state.failover_history.append(
                f"{slot_label} timed out after {request_timeout}s."
            )
            continue
        except requests.exceptions.RequestException as exc:
            st.session_state.stats["failed"] += 1
            st.session_state.failover_history.append(
                f"{slot_label} network error: {exc}"
            )
            continue

    return None


def render_sidebar() -> int:
    with st.sidebar:
        st.header("⚙️ API Slot Manager")
        st.write(
            "Configure your provider keys, endpoints, model names, and timeout settings. "
            "You can add more slots anytime and the app will preserve the current settings."
        )

        slot_count = st.number_input(
            "Active API slots",
            min_value=1,
            max_value=MAX_SLOTS,
            value=len(st.session_state.api_slots),
            step=1,
            key="slot_count",
        )

        ensure_slot_count(slot_count)

        st.markdown("---")
        st.subheader("Global failover settings")
        speed_threshold = st.number_input(
            "Failover if response is slower than (seconds)",
            min_value=1,
            max_value=30,
            value=8,
            help="If a provider does not respond within this value, the app moves to the next slot.",
            key="speed_threshold",
        )
        st.write("If a provider is too slow or fails, the app automatically tries the next configured API slot.")

        st.markdown("---")
        for index, api in enumerate(st.session_state.api_slots, start=1):
            with st.expander(f"{api['label']}", expanded=(index <= 3)):
                api["active"] = st.checkbox("Enabled", value=api["active"], key=f"active_{index}")
                api["label"] = st.text_input("Label", value=api["label"], key=f"label_{index}")
                api["endpoint"] = st.text_input(
                    "Endpoint URL",
                    value=api["endpoint"],
                    key=f"endpoint_{index}",
                )
                api["key"] = st.text_input(
                    "API Key",
                    type="password",
                    value=api["key"],
                    key=f"key_{index}",
                )
                api["model"] = st.text_input(
                    "Model Name",
                    value=api["model"],
                    key=f"model_{index}",
                )
                api["timeout"] = st.number_input(
                    "Max timeout (seconds)",
                    min_value=1,
                    max_value=60,
                    value=int(api["timeout"]),
                    key=f"timeout_{index}",
                )

        st.markdown("---")
        if st.button("Reset conversation", key="reset_conv"):
            st.session_state.conversation = []
            st.session_state.last_status = "Conversation reset."
            st.session_state.failover_history = []
            st.session_state.stats = {
                "requests": 0,
                "successful": 0,
                "failed": 0,
                "timeouts": 0,
                "slow_responses": 0,
            }
            st.experimental_rerun()

    return speed_threshold


def render_header() -> None:
    st.title("🚀 Advanced AI Assistant with Smart Multi-API Failover")
    st.markdown(
        "Use multiple API providers in a single chat interface. "
        "If one provider fails or is too slow, the request automatically moves to the next available slot."
    )
    st.info(
        "Set up your API slots in the sidebar. The app currently supports up to 20 API slots and will remember your settings while the app is running."
    )


def render_metrics() -> None:
    active_slots = sum(1 for api in st.session_state.api_slots if api["active"] and api["key"].strip())
    total_slots = len(st.session_state.api_slots)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Configured slots", total_slots)
    col2.metric("Ready slots", active_slots)
    col3.metric("Requests sent", st.session_state.stats["requests"])
    col4.metric("Successful answers", st.session_state.stats["successful"])

    if st.session_state.last_api_index is not None:
        st.success(f"Last successful provider: slot {st.session_state.last_api_index}")
    st.caption(st.session_state.last_status)


def render_conversation() -> None:
    if not st.session_state.conversation:
        st.markdown("### Start the chat by sending a message below.")
        st.info("The best provider will be selected automatically based on response speed and availability.")
    for item in st.session_state.conversation:
        with st.chat_message(item["role"]):
            st.markdown(item["content"])


def render_log_panel() -> None:
    with st.expander("📘 Failover and performance log", expanded=True):
        if st.session_state.failover_history:
            for entry in reversed(st.session_state.failover_history[-15:]):
                st.write(f"- {entry}")
        else:
            st.write("No retry history yet. All requests will be shown here.")

        st.write("---")
        st.write(
            "**Stats:** "
            f"timeouts={st.session_state.stats['timeouts']}, "
            f"failures={st.session_state.stats['failed']}, "
            f"slow responses={st.session_state.stats['slow_responses']}"
        )


def main() -> None:
    speed_threshold = render_sidebar()
    render_header()
    render_metrics()
    render_conversation()

    if prompt := st.chat_input("Ask your AI assistant anything..."):
        st.session_state.conversation.append({"role": "user", "content": prompt})
        prompt_messages = [
            {"role": message["role"], "content": message["content"]}
            for message in st.session_state.conversation
        ]

        available_slots = [
            {**api, "index": idx + 1}
            for idx, api in enumerate(st.session_state.api_slots)
            if api["active"] and api["key"].strip()
        ]

        if not available_slots:
            st.error("No enabled API slots with valid API keys were found. Please configure at least one slot in the sidebar.")
            return

        with st.chat_message("assistant"):
            placeholder = st.empty()
            with st.spinner("Contacting the best available provider..."):
                answer = fetch_ai_response(prompt_messages, available_slots, speed_threshold)
                if answer:
                    placeholder.markdown(answer)
                    st.session_state.conversation.append({"role": "assistant", "content": answer})
                else:
                    error_text = (
                        "❌ All enabled providers failed or timed out. "
                        "Check your API keys, endpoint URLs, and network access in the sidebar."
                    )
                    placeholder.markdown(error_text)

    render_log_panel()


if __name__ == "__main__":
    main()
