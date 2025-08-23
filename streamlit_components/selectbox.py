import streamlit as st
from typing import List

def categorized_selectbox(
    label: str,
    options: List[str],
    highlight: List[str] = None,
    deprioritize: List[str] = None,
    key: str = "categorized_selectbox"
) -> str:
    """
    Streamlit selectbox with categories:
      - 🟢 highlight (first, preserves given order)
      - ⚪ normal (middle, preserves original order in `options`)
      - ⚫ deprioritize (last, preserves given order)
    """
    SYMBOLS = {
        "highlight": "🟢 ",
        "normal": "⚪ ",
        "deprioritize": "⚫ ",
    }

    highlight = highlight or []
    deprioritize = deprioritize or []
    highlight_set, deprioritize_set = set(highlight), set(deprioritize)

    ordered = [
        *(o for o in highlight if o in options),
        *(o for o in options if o not in highlight and o not in deprioritize),
        *(o for o in deprioritize if o in options)
    ]

    icon_map = {
        **{o: SYMBOLS["highlight"] for o in highlight},
        **{o: SYMBOLS["deprioritize"] for o in deprioritize},
    }
    display = [icon_map.get(o, SYMBOLS["normal"]) + o for o in ordered]
    display_to_original = dict(zip(display, ordered))
    selected_display = st.selectbox(label, display, key=key)
    
    return display_to_original[selected_display]

