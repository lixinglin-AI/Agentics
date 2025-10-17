
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import asyncio
import datetime
from pathlib import Path

from pydantic import Field
from pydantic import BaseModel
from agentics import AG
from agentics.core.atype import pydantic_to_markdown
load_dotenv()

from agentics.core.llm_connections import register_llm_provider
import google.generativeai as genai
# === Force select Gemini as the LLM provider ===
import os
GEMINI_API_KEY= "AIzaSyDPDVnOHQAHqYrUVuYlyE0pRtffILJ1Dwo"
SELECTED_LLM = "gemini"
GEMINI_MODEL_ID= "gemini/gemini-2.0-flash"

def macro_economic_analysis_ui():
    class MarketNewsImpact(BaseModel):
        date: str
        news_headline: str
        news_summary: str | None = None
        predicted_positive_industries: list[str] | None = None
        predicted_negative_industries: list[str] | None = None
        reasoning: str | None = None

    if "pydantic_class" not in st.session_state or st.session_state.pydantic_class is None:
        st.session_state.pydantic_class = MarketNewsImpact

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "gemini"

    if "market_dataset" not in st.session_state:
        st.session_state.market_dataset = AG.from_csv(
            "/Users/david/Desktop/github/Agentics/data/macro_economic_analysis/market_factors_new.csv"
        )

    if "market_dataset_index" not in st.session_state:
        st.session_state.market_dataset_index = {
            s.Date: i for i, s in enumerate(st.session_state.market_dataset.states)
        }

    start = datetime.date(2008, 7, 1)
    end = datetime.date(2025, 10, 3)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
        This application performs macro-economic analysis using market data.
        You can select or build an output Pydantic Type to focus the analysis.
        """
        )
        st.markdown(f"Selected Model: **{st.session_state.selected_model}**")
        with st.form("Selection"):

            selected_start = st.selectbox(
                "start date",
                options=sorted(st.session_state.market_dataset_index.keys()),
                index=0,
            )
            selected_end = st.selectbox(
                "end date",
                options=sorted(st.session_state.market_dataset_index.keys()),
                index=0,
            )
            # type_code = st.text_area("Insert a Pydantic Type to focus your analysis", value=example_class, height=300)
            areduce_batch_size = st.number_input(
                "areduce_batch_size", value=10, min_value=1, max_value=50, step=1
            )

            market_sentiment_analysis = st.form_submit_button("Perform Analysis")

    if market_sentiment_analysis:
        # print (st.session_state.pydantic_class)

        with st.spinner(f"Performing {st.session_state.selected_model} ..."):
            start_index = st.session_state.market_dataset_index[str(selected_start)]
            end_index = st.session_state.market_dataset_index[str(selected_end)]

            sentiment = asyncio.run(
                (
                    AG(
                        atype=st.session_state.pydantic_class,
                        transduction_type="areduce",
                        areduce_batch_size=areduce_batch_size,
                    )
                    << st.session_state.market_dataset.filter_states(
                        start=start_index, end=end_index + 1
                    )
                )
            )
            import yaml

            col2.markdown(f"### Analysis from {selected_start} to {selected_end}")
            col2.text(
                yaml.dump(
                    sentiment[0].model_dump(), sort_keys=False, allow_unicode=True
                )
            )

            col2.markdown("""### Intermediate Batches Analysis""")
            for state in sentiment.areduce_batches:
                col2.markdown("""""")
                col2.text(
                    yaml.dump(state.model_dump(), sort_keys=False, allow_unicode=True)
                )

if __name__ == "__main__":
    import streamlit as st
    st.set_page_config(page_title="Macro Economic Impact", layout="wide")

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = "ExampleModel"
    if "pydantic_class" not in st.session_state:
        st.session_state.pydantic_class = None

    macro_economic_analysis_ui()