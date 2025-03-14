import streamlit as st
import pandas as pd
from datetime import datetime
from links import cred
import gspread
import re

@st.cache_resource
def get_worksheet():
    """Load and return the Google Sheets worksheet. Cached to avoid repeated connections."""
    try:
        client = cred()
        spreadsheet = client.open("campus_data")
        worksheet = spreadsheet.worksheet("atten")
        return worksheet
    except Exception as e:
        st.session_state['worksheet_error'] = str(e)
        return None

def campus():
    """Main function to handle UI and data submission."""
    worksheet = get_worksheet()
    
    # Handle connection errors
    if worksheet is None:
        error = st.session_state.get('worksheet_error', 'Unknown error connecting to Google Sheets.')
        st.error(f"⚠️ Network issue: {error}")
        return
    
    st.write("✅ Network Active!")

    try:
        df = pd.read_csv("./data/campus.csv", encoding="ISO-8859-1")
    except Exception as e:
        st.error(f"⚠️ Error loading campus data: {e}")
        return

    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        # Region selection
        unique_regions = df['Region'].unique()
        selected_region = col1.selectbox("Select Region", ["Select"] + list(unique_regions), key="region")
        
        # Campus selection
        if selected_region != "Select":
            filtered_campuses = df[df['Region'] == selected_region]['Campus'].unique()
            selected_campus = col2.selectbox("Select Campus", ["Select"] + list(filtered_campuses), key="campus")
        else:
            selected_campus = col2.selectbox("Select Campus", ["Select"], key="campus")

        # Month selection
        current_year = datetime.now().year
        months_list = ["Select"] + [f"{datetime(2025, i, 1).strftime('%B')} {current_year}" for i in range(1, 13)]
        month = col1.selectbox("Select Month", months_list, key="month")
        
        # Name input
        fullname = col1.text_input("Full Name", key="fullname", placeholder="Enter your full name")
        if fullname:
            formatted_name = fullname.strip().title()
            if not re.match(r"^[A-Za-z\- ]+$", formatted_name):
                st.warning("⚠️ Names should only contain letters, spaces, or hyphens (-).")
            else:
                st.session_state.formatted_fullname = formatted_name

        # Offering and baptized inputs
        off1 = col2.number_input("1st Offering Amt (Ghȼ)", min_value=0.0, value=0.0, key="offering1")
        baptized = col2.number_input("Enter Number Baptized", min_value=0, value=0, key="baptized")

    st.markdown("**SUNDAY WORSHIP SERVICE ATTENDANCE SUMMARY**")
    
    # High Attendance Week
    with st.container(border=True):
        st.markdown("Highest Attendance Week || Pick the highest attendance week in the month")
        col1, col2, col3 = st.columns(3)
        bro = col1.number_input("Brothers", min_value=0, value=0, key="brothers")
        sis = col1.number_input("Sisters", min_value=0, value=0, key="sisters")
        boys = col2.number_input("Children Boys", min_value=0, value=0, key="boys")
        girls = col2.number_input("Children Girls", min_value=0, value=0, key="girls")
        vis_male = col3.number_input("Visitors Male", min_value=0, value=0, key="visitors_male")
        vis_female = col3.number_input("Visitors Female", min_value=0, value=0, key="visitors_female")
        high_total = bro + sis + boys + girls
        st.write("High Attendance Total:", high_total)


    # Low Attendance Week
    with st.container(border=True):
        st.markdown("Lowest Attendance Week || Pick the lowest attendance week in the month")
        col1, col2, col3 = st.columns(3)
        bro_low = col1.number_input("Brothers", min_value=0, value=0, key="brothers_low")
        sis_low = col1.number_input("Sisters", min_value=0, value=0, key="sisters_low")
        boys_low = col2.number_input("Children Boys", min_value=0, value=0, key="boys_low")
        girls_low = col2.number_input("Children Girl", min_value=0, value=0, key="girls_low")
        vis_male_low = col3.number_input("Visitors Male", min_value=0, value=0, key="visitors_male_low")
        vis_female_low = col3.number_input("Visitors Female", min_value=0, value=0, key="visitors_female_low")    
        low_total = bro_low + sis_low + boys_low + girls_low
        st.write("Low Attendance Total:", low_total)

    with st.container(border=True):
        st.markdown("Overall Month Attendance || Sum each Category attendance in the month")
        col1, col2, col3 = st.columns(3)
        bro_total = col1.number_input("Total Brothers", min_value=0, value=0, key="brothers_total")
        sis_total = col2.number_input("Total Sisters", min_value=0, value=0, key="sisters_total")
        child_total = col3.number_input("Total Children", min_value=0, value=0, key="boys_total")
        st.write("Overall Attendance:",bro_total+sis_total+child_total)

    submit = st.button("Submit")

    if submit:
        # Validation checks
        validation_failed = False
        if selected_region == "Select":
            st.warning("⚠️ Please select a Region.")
            validation_failed = True
        if selected_campus == "Select":
            st.warning("⚠️ Please select a Campus.")
            validation_failed = True
        if month == "Select":
            st.warning("⚠️ Please select a Month.")
            validation_failed = True
        if not fullname:
            st.warning("⚠️ Please enter your Full Name.")
            validation_failed = True
        if baptized == 0:
            st.warning("⚠️ Please enter the Number Baptized.")
            validation_failed = True
        if off1 == 0.0:
            st.warning("⚠️ Please enter the 1st Offering amount.")
            validation_failed = True
        
        # New validation checks for attendance totals
        if low_total > high_total:
            st.warning("⚠️ Low attendance total should not be greater than high attendance total.")
            validation_failed = True
        
        overal_att = bro_total + sis_total + child_total
        if (low_total + high_total) > overal_att:
            st.warning("⚠️ The sum of low and high attendance totals should not exceed overall monthly attendance.")
            validation_failed = True
        
        if validation_failed:
            st.stop()
        
        # Prepare and submit data
        data_to_submit = [
            str(datetime.now()), selected_region, selected_campus, month, baptized, bro, sis, 
            boys, girls, vis_male, vis_female, bro_low, sis_low, boys_low, girls_low, 
            vis_male_low, vis_female_low, off1,bro_total, sis_total, child_total, fullname
        ]
        
        try:
            worksheet.append_row(data_to_submit)
            st.success("✅ Successfully submitted!")
            st.balloons()
            
            # Clear inputs
            for key in ["region", "campus", "month", "fullname", "baptized", 
                       "brothers", "sisters", "boys", "girls", "visitors_male", 
                       "visitors_female", "offering1"]:
                if key in st.session_state:
                    del st.session_state[key]
                    
        except Exception as e:
            st.error(f"⚠️ Failed to submit data: {str(e)}")

if __name__ == "__main__":
    campus()