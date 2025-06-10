import json
import time
import requests
import io
import pandas as pd
import streamlit as st
import plotly.express as px

st.markdown("<h2 style='text-align: right; align-items: center; padding: 10px; border-bottom: 2px solid #ccc;'>College Dropout Prediction</h2>", unsafe_allow_html=True)
st.markdown("""<style>
        .stButton > button, .stFormSubmitButton > button {background-color: #0d6efd !important;color: white !important;border: none !important;padding: 10px 20px !important;border-radius: 5px !important;margin-top: 15px !important;cursor: pointer !important;}
        .stButton > button:hover, .stFormSubmitButton > button:hover {background-color: #0b5ed7 !important;}
    </style>""", unsafe_allow_html=True)
st.markdown("### Data Entries")
API_URL = "https://sia-user.azurewebsites.net/API/templetes/processData"
HEADERS = {"userKey":"4909e7f0-14d7-40ca-893e-7162b7249e25"}  

def send_to_api(df, status_placeholder):
    try:
        dataframe_json = df.to_json(orient="records")
        payload = {"dataFrame": dataframe_json}
        try: 
            response = requests.post(API_URL, headers=HEADERS, json=payload)
            print(response.text)
        except Exception as e:
            print(e)
        if response.status_code != 200:
            print("Step 4")
            raise Exception(f"API Error: {response.text}")
        if st.session_state.stop_task:
            raise Exception("Processing stopped by user")
        print("Step 5")
        job_name = json.loads(response.text)['job_name']
        print(job_name)
        status_url = f"https://sia-user.azurewebsites.net/API/templetes/Status?jobName={job_name}"
        start_time = time.time()
        status = ""
        while status != "complete" and not st.session_state.stop_task:
            if (time.time() - start_time) > 300:
                st.session_state.error_message="Job processing timed out"
                raise Exception("Job processing timed out")
            status_response = requests.get(status_url, headers=HEADERS)
            if status_response.status_code != 200:
                st.session_state.error_message=f"Status check failed: {status_response.text}"
                raise Exception(f"Status check failed: {status_response.text}")
            status = json.loads(status_response.text)["status"]
            if status == "Queued":
                status_placeholder.write("**Queuing Job**")
            elif status == "Running":
                status_placeholder.write("**Running Job**")
            elif status == "Finalizing":
                status_placeholder.write("**Finalizing Job**")
            elif status == "complete":
                status_placeholder.write("**Job completed**")
            elif status == "failed":
                status_placeholder.write("**Job failed**")
                st.session_state.error_message="The flow encountered an issue and failed, leading to the job being cancelled"
                st.session_state.stop_task=True
            time.sleep(5)
        HEADERS["fileName"] = json.loads(response.text)['fileName']
        print(HEADERS)
        download_response = requests.post("https://sia-user.azurewebsites.net/API/templetes/generateDownloadUrl",headers=HEADERS)
        print(download_response.text)
        if download_response.status_code != 200:
            st.session_state.error_message=f"Download failed: {download_response.text}"
        download_link = json.loads(download_response.text)["URL"]
        head = pd.DataFrame(json.loads(json.loads(download_response.text)["head"]))
        return head, download_link
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)
        print(HEADERS)
        st.session_state.error_message=error_message
def col2():
    with st.form(key="file_upload_form", border=False):
        st.markdown("#### File Upload")
        uploaded_file = st.file_uploader("Upload File", type=['csv', 'xlsx', 'xls', 'json', 'parquet'], accept_multiple_files=False)
        if 'task_running' not in st.session_state:
            st.session_state.task_running = False
        if 'stop_task' not in st.session_state:
            st.session_state.stop_task = False
        if "error_message" not in st.session_state:
            st.session_state.error_message = None
        cols = st.columns([8, 2])  
        with cols[0]:
            submit_clicked = st.form_submit_button("Submit File", disabled=st.session_state.task_running)    
        if submit_clicked:
            if uploaded_file is not None and not st.session_state.task_running:
                st.session_state.task_running = True
                st.session_state.stop_task = False
                st.rerun()
            else:
                st.warning("Please upload a file first")
    if st.session_state.task_running and uploaded_file is not None:
        cols1 = st.columns([7, 150 , 23])
        with cols1[-1]:
            if st.button("⏹ Stop", help="Stop current processing"):
                st.session_state.stop_task = True
                st.session_state.task_running = False
                st.rerun()
        try:
            with cols1[0]:
                with st.spinner(""):
                    with cols1[-2]:
                        status_placeholder = st.empty()
                        status_placeholder.write("**Starting process**")
                        file_ext = uploaded_file.name.split('.')[-1].lower()
                        read_functions = {
                            'csv': pd.read_csv,
                            'xlsx': pd.read_excel,
                            'xls': pd.read_excel,
                            'json': pd.read_json,
                            'parquet': pd.read_parquet
                        }
                        df = read_functions[file_ext](uploaded_file)
                        res_df, download_link = send_to_api(df, status_placeholder)
                        if not st.session_state.stop_task:
                            st.session_state.api_results = {'res_df': res_df,'download_link': download_link,'initial_df':df}
        except Exception as e:
            if "Processing stopped" not in str(e):
                st.session_state.error_message= str(e)

        finally:
            st.session_state.task_running = False
            st.session_state.stop_task = False
            st.rerun()

row1 = st.columns(1)
grid = [col.container(height=400) for col in row1]
safe_grid = [card.empty() for card in grid]
card_a=grid[0]
container_a = card_a.container()
with container_a:
    col2()


def handle_api_response():
    results = st.session_state.get('api_results', None)
    if results:
        res_df = results['res_df']
        download_link = results['download_link']
        initial_df = results['initial_df']
        response = requests.get(download_link)
        if response.status_code == 200:
            final_df = pd.read_parquet(io.BytesIO(response.content))
        with card_res:
            if res_df is not None:
                st.success("Analysis Complete")
                st.table(res_df)
                st.markdown(f"""<div style="margin-top: 20px; text-align: center;"><a href="{{download_link}}" target="_blank" style="display: inline-block;
                                padding: 12px 24px;background-color: #2ea043;color: white;text-decoration: none;border-radius: 5px;transition: all 0.2s ease;
                                border: none;cursor: pointer;font-size: 16px;font-weight: 500;">Download Results</a></div>""", unsafe_allow_html=True)
            else:
                st.markdown("<div style='border: 0.1px solid #ccc; border-radius: 10px; padding: 15px; height: 400px; margin: 10px; display: flex; justify-content: center; align-items: center; font-size: 18px; font-weight: 300; color: #777;'>No Data</div>", unsafe_allow_html=True)
    else:
        with card_res:
            st.markdown("<div style='border: 0.05px solid #ccc; border-radius: 10px; padding: 15px; height: 400px; margin: 10px; display: flex; justify-content: center; align-items: center; font-size: 18px; font-weight: 300; color: #777;'>No Data</div>", unsafe_allow_html=True)


st.markdown("### Results")
row_res = st.columns(1)
grid_res = [col.container() for col in row_res]
card_res = grid_res[0].container()
handle_api_response()
st.markdown("<div style='text-align: right;'><p>Powered by SIA</p></div>", unsafe_allow_html=True)


