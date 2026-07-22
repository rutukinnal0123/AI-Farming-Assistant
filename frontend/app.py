import streamlit as st
import requests
import tempfile
from streamlit_mic_recorder import mic_recorder

# ============================================================
# CONFIG
# ============================================================

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="🌾 AI Farming Assistant",
    page_icon="🌾",
    layout="wide"
)

# ============================================================
# LANGUAGE
# ============================================================

TEXT = {
    "English": {
        "login": "Login",
        "register": "Register",
        "dashboard": "Dashboard",
        "logout": "Logout",
        "phone": "Phone Number",
        "password": "Password",
        "name": "Name",
        "district": "District",
        "village": "Village",
        "language": "Language",
        "welcome": "Welcome",
        "menu": "Menu",
        "profile": "Profile",
        "farm": "Farm",
        "chat": "AI Chat",
        "voice": "Voice",
        "history": "History",
        "activities": "Activities",
        "reminders": "Reminders",
        "select_farm": "Select Farm",
        "register_farm": "Register Farm",
        "save_farm": "Save Farm",
        "send": "Send",
        "record": "Start Recording",
        "stop": "Stop Recording"
    },
    "Malayalam": {
        "login": "ലോഗിൻ",
        "register": "രജിസ്റ്റർ",
        "dashboard": "ഡാഷ്ബോർഡ്",
        "logout": "ലോഗ്ഔട്ട്",
        "phone": "ഫോൺ നമ്പർ",
        "password": "പാസ്‌വേഡ്",
        "name": "പേര്",
        "district": "ജില്ല",
        "village": "ഗ്രാമം",
        "language": "ഭാഷ",
        "welcome": "സ്വാഗതം",
        "menu": "മെനു",
        "profile": "പ്രൊഫൈൽ",
        "farm": "ഫാം",
        "chat": "AI ചാറ്റ്",
        "voice": "വോയ്സ്",
        "history": "ഹിസ്റ്ററി",
        "activities": "ആക്റ്റിവിറ്റീസ്",
        "reminders": "റിമൈൻഡേഴ്സ്",
        "select_farm": "ഫാം തിരഞ്ഞെടുക്കുക",
        "register_farm": "ഫാം രജിസ്റ്റർ ചെയ്യുക",
        "save_farm": "ഫാം സേവ് ചെയ്യുക",
        "send": "അയയ്ക്കുക",
        "record": "റെക്കോർഡ് ആരംഭിക്കുക",
        "stop": "റെക്കോർഡ് നിർത്തുക"
    }
}

# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "token": None,
    "logged_in": False,
    "farmer_id": None,
    "farmer_name": "",
    "district": "",
    "village": "",
    "language": "English",
    "selected_farm_id": None,
    "selected_farm_name": "",
    "ui_language": "English"
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

T = TEXT[st.session_state.ui_language]

# ============================================================
# TITLE
# ============================================================

st.title("🌾 AI Farming Assistant")

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🌾 AI Farming")

    st.session_state.ui_language = st.selectbox(
        "UI Language",
        ["English", "Malayalam"],
        index=0 if st.session_state.ui_language == "English" else 1
    )

    T = TEXT[st.session_state.ui_language]

    st.divider()

    if st.session_state.logged_in:

        st.success(
            f"{T['welcome']}\n\n{st.session_state.farmer_name}"
        )

        st.markdown("### 👤 " + T["profile"])

        st.write(f"📍 {st.session_state.district}")
        st.write(f"🏡 {st.session_state.village}")
        st.write(f"🌐 {st.session_state.language}")

        st.divider()

    page = st.radio(
        T["menu"],
        [
            T["login"],
            T["register"],
            T["dashboard"]
        ]
    )

# ============================================================
# LOGIN
# ============================================================

if page == T["login"]:

    if st.session_state.logged_in:

        st.success(
            f"{T['welcome']} {st.session_state.farmer_name}"
        )

        st.warning(
            "You are already logged in.\n\nPlease logout first to login with another account."
        )

        st.stop()

    st.header(T["login"])

    phone = st.text_input(T["phone"])

    password = st.text_input(
        T["password"],
        type="password"
    )

    if st.button(T["login"]):

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

            st.success(f"{T['welcome']} {farmer['name']} 🌾")

            st.rerun()

        else:

            st.error(response.text)

# ============================================================
# REGISTER
# ============================================================

elif page == T["register"]:

    if st.session_state.logged_in:

        st.success(
            f"{T['welcome']} {st.session_state.farmer_name}"
        )

        st.warning(
            "You are already logged in.\n\nPlease logout first to register a new farmer."
        )

        st.stop()

    st.header(T["register"])

    name = st.text_input(T["name"])

    phone = st.text_input(T["phone"])

    password = st.text_input(
        T["password"],
        type="password"
    )

    district = st.text_input(T["district"])

    village = st.text_input(T["village"])

    language = st.selectbox(
        T["language"],
        ["English", "Malayalam"]
    )

    if st.button(T["register"]):

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
            st.success("Registration Successful")
        else:
            st.error(response.text)
            
        # ============================================================
# DASHBOARD
# ============================================================

elif page == T["dashboard"]:

    if not st.session_state.logged_in:
        st.warning("Please login first.")
        st.stop()

    st.header("🌾 Farmer Dashboard")

    # ============================================================
    # LOAD FARMS
    # ============================================================

    farm_response = requests.get(
        f"{API_URL}/farmers/{st.session_state.farmer_id}/farms",
        headers={
            "Authorization": f"Bearer {st.session_state.token}"
        }
    )

    farms = []

    if farm_response.status_code == 200:
        farms = farm_response.json()

    # ============================================================
    # FARM SELECTOR
    # ============================================================

    if len(farms) == 0:

        st.warning(
            "No farms found. Please register your first farm."
        )

    else:

        farm_names = [
            farm["farm_name"]
            for farm in farms
        ]

        default_index = 0

        if st.session_state.selected_farm_name in farm_names:
            default_index = farm_names.index(
                st.session_state.selected_farm_name
            )

        selected_name = st.selectbox(
            T["select_farm"],
            farm_names,
            index=default_index
        )

        selected_farm = next(
            farm
            for farm in farms
            if farm["farm_name"] == selected_name
        )

        st.session_state.selected_farm_id = selected_farm["id"]
        st.session_state.selected_farm_name = selected_farm["farm_name"]

        st.success(
            f"🌱 Active Farm : {selected_name}"
        )

    # ============================================================
    # PROFILE CARD
    # ============================================================

    c1, c2 = st.columns([2, 1])

    with c1:

        st.info(
            f"""
### 👤 {st.session_state.farmer_name}

📍 District : **{st.session_state.district}**

🏡 Village : **{st.session_state.village}**

🌐 Preferred Language : **{st.session_state.language}**
"""
        )

    with c2:

        st.metric(
            "Total Farms",
            len(farms)
        )

        if st.session_state.selected_farm_name:
            st.metric(
                "Current Farm",
                st.session_state.selected_farm_name
            )

    st.divider()

    # ============================================================
    # TABS
    # ============================================================

    (
        tab_farm,
        tab_chat,
        tab_voice,
        tab_history,
        tab_activity,
        tab_reminder
    ) = st.tabs(
        [
            "🌱 Farm",
            "🤖 AI Chat",
            "🎤 Voice",
            "📜 History",
            "📋 Activities",
            "🔔 Reminders"
        ]
    )

    # ============================================================
    # FARM TAB
    # ============================================================

    with tab_farm:

        st.subheader(T["register_farm"])

        col1, col2 = st.columns(2)

        with col1:

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

        with col2:

            soil_type = st.text_input(
                "Soil Type"
            )

            irrigation = st.text_input(
                "Irrigation"
            )

            latitude = st.number_input(
                "Latitude",
                value=0.0,
                format="%.6f"
            )

            longitude = st.number_input(
                "Longitude",
                value=0.0,
                format="%.6f"
            )

        if st.button(T["save_farm"]):

            response = requests.post(
                f"{API_URL}/farms",
                headers={
                    "Authorization": f"Bearer {st.session_state.token}"
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

                st.success("✅ Farm Registered Successfully")

                st.rerun()

            else:

                st.error(response.text)
                
                
                
                
        # ============================================================
    # AI CHAT TAB
    # ============================================================

    with tab_chat:

        st.subheader("🤖 AI Farming Assistant")

        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []

        for msg in st.session_state.chat_messages:

            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        prompt = st.chat_input("Ask anything about your crop...")

        if prompt:

            st.session_state.chat_messages.append(
                {
                    "role": "user",
                    "content": prompt
                }
            )

            with st.chat_message("user"):
                st.markdown(prompt)

            payload = {
                "message": prompt
            }

            if st.session_state.selected_farm_id is not None:
                payload["farm_id"] = st.session_state.selected_farm_id

            response = requests.post(
                f"{API_URL}/chat/",
                headers={
                    "Authorization":
                    f"Bearer {st.session_state.token}"
                },
                json=payload
            )

            if response.status_code == 200:

                answer = response.json()["answer"]

                st.session_state.chat_messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

                with st.chat_message("assistant"):
                    st.markdown(answer)

            else:

                st.error(response.text)

    # ============================================================
    # VOICE TAB
    # ============================================================

    with tab_voice:

        st.subheader("🎤 AI Voice Assistant")

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
            ) as temp_audio:

                temp_audio.write(audio["bytes"])
                audio_path = temp_audio.name

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

                st.success("Recognized Question")

                st.write(result["question"])

                st.success("AI Response")

                st.write(result["answer"])

                if result.get("audio_file"):
                    st.audio(result["audio_file"])

            else:

                st.error(response.text)

    # ============================================================
    # CHAT HISTORY TAB
    # ============================================================

    with tab_history:

        st.subheader("📜 Previous Conversations")

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

                st.info("No previous conversations found.")

            else:

                for chat in reversed(chats):

                    with st.expander(chat["question"]):

                        st.markdown(
                            f"### 👨 Farmer\n{chat['question']}"
                        )

                        st.markdown(
                            f"### 🤖 AI Assistant\n{chat['answer']}"
                        )

        else:

            st.error("Unable to load chat history.")
            
        # ============================================================
    # ACTIVITIES TAB
    # ============================================================

    with tab_activity:

        st.subheader("📋 Farm Activities")

        if st.session_state.selected_farm_id is None:

            st.info("Please select a farm first.")

        else:

            response = requests.get(
                f"{API_URL}/farms/{st.session_state.selected_farm_id}/activities",
                headers={
                    "Authorization":
                    f"Bearer {st.session_state.token}"
                }
            )

            if response.status_code == 200:

                activities = response.json()

                if len(activities) == 0:

                    st.info("No activities found.")

                else:

                    for activity in reversed(activities):

                        with st.container():

                            st.markdown("---")

                            st.markdown(
                                f"### 🌱 {activity.get('title','Activity')}"
                            )

                            if activity.get("description"):
                                st.write(activity["description"])

                            if activity.get("activity_date"):
                                st.caption(
                                    f"📅 {activity['activity_date']}"
                                )

            else:

                st.error(response.text)

    # ============================================================
    # REMINDERS TAB
    # ============================================================

    with tab_reminder:

        st.subheader("🔔 Upcoming Reminders")

        if st.session_state.selected_farm_id is None:

            st.info("Please select a farm first.")

        else:

            response = requests.get(
                f"{API_URL}/farms/{st.session_state.selected_farm_id}/reminders",
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

                        with st.container():

                            st.markdown("---")

                            st.markdown(
                                f"## 📌 {reminder['title']}"
                            )

                            st.write(
                                reminder["description"]
                            )

                            st.info(
                                f"📅 Reminder Date : {reminder['reminder_date']}"
                            )

            else:

                st.error(response.text)

# ============================================================
# LOGOUT
# ============================================================

if st.session_state.logged_in:

    st.sidebar.divider()

    if st.sidebar.button("🚪 Logout", use_container_width=True):

        st.session_state.token = None
        st.session_state.logged_in = False
        st.session_state.farmer_id = None
        st.session_state.farmer_name = ""
        st.session_state.district = ""
        st.session_state.village = ""
        st.session_state.language = "English"
        st.session_state.selected_farm_id = None
        st.session_state.selected_farm_name = ""
        st.session_state.chat_messages = []

        st.rerun()