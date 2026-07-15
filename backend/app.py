import streamlit as st
import requests

# ==========================================
# CONFIG
# ==========================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Farming Assistant",
    page_icon="🌾",
    layout="wide"
)

# ==========================================
# SESSION STATE
# ==========================================


defaults = {

    "token": None,

    "logged_in": False,

    "farmer_id": None,

    "farmer_name": "",

    "district": "",

    "village": "",

    "language": "English"

}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

if "selected_farm_id" not in st.session_state:
    st.session_state.selected_farm_id = None

if "selected_farm_name" not in st.session_state:
    st.session_state.selected_farm_name = ""
    
# ==========================================
# TITLE
# ==========================================

st.title("🌾 AI Farming Assistant")

st.markdown("---")

# ==========================================
# SIDEBAR
# ==========================================

# ==========================================
# SIDEBAR
# ==========================================

if st.session_state.logged_in:

    st.sidebar.success(
        f"👤 Welcome, {st.session_state.farmer_name}"
    )

    st.sidebar.write(
        f"📍 District : {st.session_state.district}"
    )

    st.sidebar.write(
        f"🏡 Village : {st.session_state.village}"
    )

    st.sidebar.write(
        f"🌐 Language : {st.session_state.language}"
    )

    st.sidebar.markdown("---")

page = st.sidebar.radio(

    "Menu",

    [

        "Login",

        "Register",

        "Dashboard"

    ]

)
# ==========================================
# LOGIN
# ==========================================
if page == "Login" and st.session_state.logged_in:

    st.success(
        f"Already logged in as {st.session_state.farmer_name}"
    )

    st.info(
        "Go to Dashboard or Logout from the sidebar."
    )

    st.stop()

if page == "Login":

    st.header("Login")

    phone = st.text_input(
        "Phone Number"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        response = requests.post(

            f"{API_URL}/auth/login",

            json={
                "phone": phone,
                "password": password
            }

        )

        if response.status_code == 200:

         data = response.json()

         farmer = data["farmer"]

         st.session_state.token = data["access_token"]

         st.session_state.logged_in = True

         st.session_state.farmer_id = farmer["id"]

         st.session_state.farmer_name = farmer["name"]

         st.session_state.district = farmer["district"]

        st.session_state.village = farmer["village"]

        st.session_state.language = farmer["language"]

        st.success(
           f"Welcome {farmer['name']} 👋"
       )

    st.rerun()

# ==========================================
# REGISTER
# ==========================================

elif page == "Register":

    st.header("Farmer Registration")

    name = st.text_input("Name")

    phone = st.text_input("Phone")

    password = st.text_input(
        "Password",
        type="password"
    )

    district = st.text_input("District")

    village = st.text_input("Village")

    language = st.selectbox(

        "Language",

        [

            "Malayalam",

            "English"

        ]

    )

    if st.button("Register Farmer"):

        response = requests.post(

            f"{API_URL}/farmers",

            json={

                "name": name,

                "phone": phone,

                "password": password,

                "district": district,

                "village": village,

                "language": language

            }

        )

        if response.status_code == 200:

            st.success(
                "Farmer Registered Successfully"
            )

        else:

            st.error(
                response.text
            )

# ==========================================
# DASHBOARD
# ==========================================

elif page == "Dashboard":

    if not st.session_state.logged_in:

        st.warning("Please login first.")

    else:

        st.header("🌾 Farmer Dashboard")
        
        # ======================================
# FARM SELECTION
# ======================================

response = requests.get(

    f"{API_URL}/farmers/{st.session_state.farmer_id}/farms",

    headers={

        "Authorization":
        f"Bearer {st.session_state.token}"

    }

)

if response.status_code == 200:

    farms = response.json()

    if len(farms) == 0:

        st.warning(
            "No farms registered. Please register a farm first."
        )

    else:

        farm_names = [

            farm["farm_name"]

            for farm in farms

        ]

        selected_name = st.selectbox(

            "🌱 Select Farm",

            farm_names

        )

        selected_farm = next(

            farm

            for farm in farms

            if farm["farm_name"] == selected_name

        )

        st.session_state.selected_farm_id = selected_farm["id"]

        st.session_state.selected_farm_name = selected_farm["farm_name"]

        st.success(
            f"Selected Farm : {selected_farm['farm_name']}"
        )
        
        
        

        st.info(
    f"""
👤 Farmer : {st.session_state.farmer_name}

📍 District : {st.session_state.district}

🏡 Village : {st.session_state.village}

🌐 Language : {st.session_state.language}
"""
)

        tab1, tab2 ,tab3,tab4,tab5= st.tabs(

            [

                "Farm",
                "AI Chat",
                "Voice",
                "History"
                "Remainders"

            ]

        )

        # ======================================
        # FARM TAB
        # ======================================

        with tab1:

            st.subheader("Register Farm")

            farm_name = st.text_input(
                "Farm Name"
            )

            crop = st.text_input(
                "Crop"
            )

            crop_stage = st.selectbox(

                "Crop Stage",

                [

                    "Seedling",

                    "Vegetative",

                    "Flowering",

                    "Harvest"

                ]

            )

            land_size = st.number_input(
                "Land Size (Acres)",
                min_value=0.0
            )

            soil_type = st.text_input(
                "Soil Type"
            )

            irrigation = st.text_input(
                "Irrigation"
            )

            latitude = st.number_input(
                "Latitude",
                value=0.0
            )

            longitude = st.number_input(
                "Longitude",
                value=0.0
            )

            if st.button("Save Farm"):

                response = requests.post(

                    f"{API_URL}/farms",

                    headers={

                        "Authorization":
                        f"Bearer {st.session_state.token}"

                    },

                   json={

    "farmer_id": st.session_state.farmer_id,

    "farm_name": farm_name,

    "crop": crop,

    "crop_stage": crop_stage,

    "land_size": land_size,

    "soil_type": soil_type,

    "irrigation": irrigation,

    "latitude": latitude,

    "longitude": longitude

}

                )

                if response.status_code == 200:

                    st.success("Farm Saved Successfully")

                else:

                    st.error(response.text)

        # ======================================
        # CHAT TAB
        # ======================================

        with tab2:

            st.subheader("💬 AI Farming Assistant")

            message = st.text_area(

                "Ask your question"

            )

            if st.button("Send"):

                response = requests.post(

                    f"{API_URL}/chat/",

                    headers={

                        "Authorization":
                        f"Bearer {st.session_state.token}"

                    },

                    json={

                        "message": message

                    }

                )

                if response.status_code == 200:

                    answer = response.json()["answer"]

                    st.success(answer)

                else:

                    st.error(response.text)


        # ======================================
        # VOICE TAB
        # ======================================

        import tempfile

        from streamlit_mic_recorder import mic_recorder

        with tab3:

            st.subheader("🎤 Voice Assistant")

            audio = mic_recorder(

                start_prompt="🎙 Start Recording",

                stop_prompt="⏹ Stop Recording",

                just_once=True,

                key="voice"

            )

            if audio:

                with tempfile.NamedTemporaryFile(

                    delete=False,

                    suffix=".wav"

                ) as f:

                    f.write(audio["bytes"])

                    audio_path = f.name

                with open(audio_path, "rb") as audio_file:

                    response = requests.post(

                        f"{API_URL}/chat/voice",

                        headers={

                            "Authorization":
                            f"Bearer {st.session_state.token}"

                        },

                        files={

                            "audio": audio_file

                        }

                    )

                if response.status_code == 200:

                    result = response.json()

                    st.success(result["question"])

                    st.info(result["answer"])

                    st.audio(result["audio_file"])

                else:
                    st.error(response.text)
                    
# ======================================
# HISTORY TAB
# ======================================

with tab4:

    st.subheader("📜 Chat History")

    response = requests.get(

        f"{API_URL}/farmers/{st.session_state.farmer_id}/chat-history",

        headers={

            "Authorization":
            f"Bearer {st.session_state.token}"

        }

    )

    if response.status_code == 200:

        chats = response.json()

        if len(chats) == 0:

            st.info("No previous chats.")

        else:

            for chat in reversed(chats):

                with st.expander(

                    chat["question"]

                ):

                    st.markdown(

                        f"**👨 You:** {chat['question']}"

                    )

                    st.markdown(

                        f"**🤖 AgriMitra:** {chat['answer']}"

                    )

    else:

        st.error("Unable to load chat history.")
        
        
        
        
# ======================================
# REMINDER TAB
# ======================================

with tab5:

    st.subheader("🔔 Upcoming Reminders")

    response = requests.get(

        f"{API_URL}/farms/{st.session_state.farmer_id}/reminders",

        headers={

            "Authorization":
            f"Bearer {st.session_state.token}"

        }

    )

    if response.status_code == 200:

        reminders = response.json()

        if len(reminders) == 0:

            st.info("No reminders available.")

        else:

            for reminder in reminders:

                st.info(
                    f"""
📌 {reminder['title']}

📝 {reminder['description']}

📅 {reminder['reminder_date']}
"""
                )

    else:

        st.error("Unable to fetch reminders.")
        

st.sidebar.markdown("---")



if st.session_state.logged_in:

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout"):

        st.session_state.token = None

        st.session_state.logged_in = False

        st.session_state.farmer_id = None

        st.session_state.farmer_name = ""

        st.session_state.district = ""

        st.session_state.village = ""

        st.session_state.language = "English"

        st.rerun()