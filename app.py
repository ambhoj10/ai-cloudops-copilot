import streamlit as st
import os

from dotenv import load_dotenv

from langchain_openai import AzureChatOpenAI

# Page config
st.set_page_config(
    page_title="AI CloudOps Copilot",
    page_icon="🤖",
    layout="wide"
)

# Load environment variables
load_dotenv()

# Azure OpenAI model
llm = AzureChatOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    temperature=0
)

# CPU monitoring tool
def check_cpu_usage(issue):

    if "cpu" in issue.lower():

        return "🔴 CPU ALERT: CPU usage is currently 95% on production VM."

    return "🟢 CPU systems operating normally."


# Memory monitoring tool
def check_memory_usage(issue):

    if "memory" in issue.lower() or "ram" in issue.lower():

        return "🟠 MEMORY ALERT: Memory usage is currently 92%."

    return "🟢 Memory systems operating normally."


# Kubernetes diagnostics tool
def check_kubernetes(issue):

    if "kubernetes" in issue.lower() or "pod" in issue.lower():

        return "🔴 KUBERNETES ALERT: Pods are in CrashLoopBackOff state."

    return "🟢 Kubernetes cluster healthy."


# Deployment diagnostics tool
def check_deployment(issue):

    if "deploy" in issue.lower() or "pipeline" in issue.lower():

        return "🟠 DEPLOYMENT ALERT: CI/CD pipeline timeout detected."

    return "🟢 Deployment systems healthy."


# Streamlit UI
st.title("🤖 AI CloudOps Copilot")

st.caption(
    "Enterprise AI-powered cloud incident investigation assistant"
)

# Dashboard cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Cloud Status",
        value="Operational"
    )

with col2:
    st.metric(
        label="AI Agent",
        value="Active"
    )

with col3:
    st.metric(
        label="Monitoring",
        value="Enabled"
    )

with col4:
    st.metric(
        label="Incident Memory",
        value="Online"
    )

st.divider()

# Session memory
if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

user_input = st.text_area(
    "Describe your cloud incident",
    height=180,
    placeholder="Example: Kubernetes pods are crashing after deployment pipeline execution..."
)

if st.button("🚀 Investigate Incident"):

    with st.spinner("AI Copilot investigating incident..."):

        # Autonomous tool selection
        tool_results = []

        if "cpu" in user_input.lower():

            tool_results.append(
                check_cpu_usage(user_input)
            )

        if "memory" in user_input.lower() or "ram" in user_input.lower():

            tool_results.append(
                check_memory_usage(user_input)
            )

        if "kubernetes" in user_input.lower() or "pod" in user_input.lower():

            tool_results.append(
                check_kubernetes(user_input)
            )

        if "deploy" in user_input.lower() or "pipeline" in user_input.lower():

            tool_results.append(
                check_deployment(user_input)
            )

        if not tool_results:

            tool_results.append(
                "🟢 No critical monitoring alerts detected."
            )

        monitoring_data = "\n".join(tool_results)

        # Build conversation history
        history = "\n".join(st.session_state.chat_history)

        prompt = f'''
You are an enterprise AI CloudOps Copilot.

You investigate cloud incidents professionally.

Conversation History:
{history}

Current Incident:
{user_input}

Monitoring Data:
{monitoring_data}

Generate a professional incident report with:

1. Incident Summary
2. Root Cause Analysis
3. Recommended Actions
4. Severity Level
5. Operational Impact
'''

        response = llm.invoke(prompt)

        # Save memory
        st.session_state.chat_history.append(
            f"User: {user_input}"
        )

        st.session_state.chat_history.append(
            f"AI: {response.content}"
        )

        # AI Response Section
        st.subheader("📖 AI Incident Report")

        st.markdown(response.content)

        st.divider()

        # Monitoring dashboard
        st.subheader("📡 Monitoring Dashboard")

        st.success("Monitoring tools executed successfully")

        st.code(monitoring_data)

# Investigation memory section
with st.expander("🧠 Investigation Memory Timeline"):

    if st.session_state.chat_history:

        for item in st.session_state.chat_history:

            st.write(item)

    else:

        st.write("No investigation history available yet.")

st.divider()

st.caption(
    "Built with Azure OpenAI + Streamlit + Autonomous AI Workflows"
)