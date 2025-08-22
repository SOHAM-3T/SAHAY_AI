import streamlit as st

# Simple test app
st.title("🧪 Test App - AI Career Mentor")
st.write("This is a simple test to verify Streamlit is working correctly.")

# Test basic components
st.header("Testing Basic Components")

# Test button
if st.button("Click me!"):
    st.success("✅ Button works!")

# Test file uploader
uploaded_file = st.file_uploader("Test file upload", type=["txt", "pdf"])
if uploaded_file is not None:
    st.write(f"✅ File uploaded: {uploaded_file.name}")

# Test columns
col1, col2 = st.columns(2)
with col1:
    st.write("Column 1 works!")
with col2:
    st.write("Column 2 works!")

# Test metrics
st.metric("Test Metric", "100", "10")

st.success("🎉 If you can see this, Streamlit is working correctly!")
