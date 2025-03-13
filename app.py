import streamlit as st
from attendance import campus
from membership import member
from streamlit.components.v1 import html

# Set page configuration
st.set_page_config(page_title="Campus Attendance App", page_icon="🌱", layout="centered")

# Main container with border
with st.container(border=True):
    # Display image
    st.image('./media/reportlogo.png')
    # Display markdown text
    st.markdown("""
                **NB: Kindly submit your report by completing the form:**  
                    🗸 *Contact the national campus secretary for any assistance/enquiry*.  
                    🗸 *All fields are required to fill*.
                       """)
    
    # Create two columns
    col1, col2 = st.columns(2)
    # Section selection
    sections = col1.selectbox("SELECT OPTION", ["Membership Attendance","Monthly Attendance"], key="sec121")
    # Main function based on selection
    if sections == "Membership Attendance":
        member()

    if sections == "Monthly Attendance":
        campus()

# Add JavaScript keep-alive
html("""
<script>
setInterval(function() {
    fetch(window.location.href).then(() => console.log('Keep-alive request sent.'));
}, 5 * 60 * 1000);
</script>
""")

# Hide Streamlit elements
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}  /* Hide the hamburger menu */
    footer {visibility: hidden;}  /* Hide the footer */
    header {visibility: hidden;}  /* Hide the header */
    </style>
    """,
    unsafe_allow_html=True
)