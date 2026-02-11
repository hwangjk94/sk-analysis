import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import analytics

# [필독] 1. 가장 먼저 실행되어야 하는 설정
st.set_page_config(page_title="세나 리버스 관리자 센터", layout="wide")

# 2. 구글 시트 및 API 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_file = "skrb-db-e7d51b9f990a.json" 
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
client = gspread.authorize(creds)
sheet = client.open("세나리버스_데이터").sheet1

# 3. 리스트 정의 (페이지 공통 사용)
HERO_LIST = sorted(list(set([
    "팔라누스", "플라튼", "아라곤", "프레이야", "바네사", "키리엘", "멜키르", "쥬리", 
    "밀리아", "트루드", "스파이크", "아멜리아", "손오공", "엘리시아", "겔리두스", "연희", 
    "카일", "파이", "카론", "챈슬러", "여포", "브란즈&브란셀", "카구라", "린", "루디", 
    "엘리스", "로지", "녹스", "크리스", "태오", "풍연", "에이스", "콜트", "제이브", 
    "룩", "리나", "니아", "초선", "유신", "라니아", "발리스타", "실베스타", "클라한", 
    "델론즈", "카르마", "라이언", "아일린", "레이첼", "아킬라"
])))

PET_LIST = sorted(list(set([
    "이린", "연지", "루", "파이크", "유", "카람", "크리", "델로", "리첼", "멜패로", "헬레핀"
])))

# 4. 사이드바 메뉴
st.sidebar.title("🎮 메뉴")
page = st.sidebar.radio("이동할 페이지", ["데이터 입력", "공략 분석"])

# 5. 페이지별 화면 구성
if page == "데이터 입력":
    # --- [데이터 입력 페이지] ---
    st.title("⚔️ 길드전 데이터 통합 입력 시스템")
    st.info("관리자 모드: 오늘 발생한 전투 기록을 차례대로 입력하세요.")

    with st.form("guild_war_entry", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🛡️ 아군 (공격/방어)")
            my_heroes = st.multiselect("아군 영웅 (3명)", HERO_LIST)
            my_pet = st.selectbox("아군 펫", ["선택 안함"] + PET_LIST)
            
        with col2:
            st.subheader("💀 상대군 (방어/공격)")
            opp_heroes = st.multiselect("상대 영웅 (3명)", HERO_LIST)
            opp_pet = st.selectbox("상대 펫", ["선택 안함"] + PET_LIST)

        st.divider()
        
        col3, col4 = st.columns(2)
        with col3:
            result = st.radio("전투 결과", ["승리", "패배"], horizontal=True)
        with col4:
            note = st.text_input("상세 세팅 및 메모", placeholder="예: 속공 285, 불사 장신구 등")

        submit_button = st.form_submit_button("🔥 기록 저장 및 다음 입력")

    # 데이터 저장 로직 (입력 페이지 안에서만 작동해야 함)
    if submit_button:
        if len(my_heroes) == 3 and len(opp_heroes) == 3:
            my_deck_str = ", ".join(sorted(my_heroes))
            opp_deck_str = ", ".join(sorted(opp_heroes))
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_row = [now, my_deck_str, my_pet, opp_deck_str, opp_pet, result, note]
            
            try:
                sheet.append_row(new_row)
                st.success(f"✅ 저장 완료: {my_deck_str} vs {opp_deck_str} ({result})")
                st.balloons()
            except Exception as e:
                st.error(f"⚠️ 저장 실패: {e}")
        else:
            st.warning("⚠️ 영웅을 반드시 3명씩 선택해야 기록이 가능합니다.")

else:
    # --- [공략 분석 페이지] ---
    # analytics.py에서 가져온 제목이 겹칠 수 있으므로 main에서는 제목을 생략하거나 다르게 줍니다.
    analytics.show_strategy_analysis(sheet)