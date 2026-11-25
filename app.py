import streamlit as st

# 1. 데이터(리스트) 구조 설계 - snake_case 준수
season_list = ["봄", "여름", "가을", "겨울"]

# 각 계절별로 추천하는 대표 의상 소재 리스트
spring_materials = ["면", "데님", "트위드", "니트"]
summer_materials = ["린넨", "면", "인견", "시어서커", "메쉬"]
fall_materials = ["니트", "가죽", "스웨이드", "면", "코듀로이"]
winter_materials = ["울", "캐시미어", "패딩", "플리스", "기모"]

# 소재의 성질별 분류 리스트 (이유 판별용)
cool_materials = ["린넨", "인견", "시어서커", "메쉬"]  # 통풍이 잘되는 시원한 소재
warm_materials = ["울", "캐시미어", "패딩", "플리스", "기모", "가죽", "스웨이드", "코듀로이"]  # 보온성이 높은 따뜻한 소재


# 2. 함수(def) 정의: 계절과 소재 리스트를 매개변수로 받아 추천 여부 및 이유 판별
def check_clothing_fit(current_season, selected_materials):
    # 선택구조(if-elif-else)로 현재 계절에 맞는 추천 소재 리스트 연결
    if current_season == "봄":
        good_materials = spring_materials
    elif current_season == "여름":
        good_materials = summer_materials
    elif current_season == "가을":
        good_materials = fall_materials
    else:
        good_materials = winter_materials

    # 반복구조(for)를 활용해 사용자가 고른 소재 중 계절에 맞는 소재 개수 세기
    match_count = 0
    for mat in selected_materials:
        if mat in good_materials:
            match_count += 1

    # 소재의 차지 비율(%) 계산
    total_count = len(selected_materials)
    fit_ratio = (match_count / total_count) * 100

    # 비율에 따라 추천/비추천 판별 (50% 이상이면 추천)
    if fit_ratio >= 50:
        result = "추천 👍"
    else:
        result = "비추천 👎"

    return result, fit_ratio, good_materials


# 소재별 구체적인 적합/부적합 이유를 알려주는 보조 함수
def get_material_reason(current_season, material, good_materials):
    if material in good_materials:
        return f"O ({current_season} 날씨에 딱 알맞은 소재)"
    else:
        # 계절과 소재의 성질을 비교해 구체적인 이유 반환
        if current_season == "여름" and material in warm_materials:
            return "X (보온성이 높아 여름엔 너무 더움 🥵)"
        elif current_season == "겨울" and material in cool_materials:
            return "X (통풍이 잘되어 겨울엔 너무 추움 🥶)"
        elif current_season == "겨울":
            return "X (한겨울에 입기엔 보온성이 부족해 추움 🥶)"
        elif current_season == "여름":
            return "X (한여름에 입기엔 통기성이 부족해 더움 🥵)"
        elif current_season in ["봄", "가을"] and material in ["패딩", "기모", "플리스"]:
            return "X (간절기에 입기엔 과하게 더움 🥵)"
        else:
            return "X (간절기에 입기엔 다소 얇아 추움 🥶)"


# --- 여기서부터 Streamlit 웹 화면 구성 ---
st.title("👕 계절별 맞춤 의류 소재 판별기")
st.write("사려는 옷의 소재가 현재 계절에 적합한지, 덥거나 춥진 않을지 분석해 드립니다!")

# 사용자 입력 받기
current_season = st.selectbox("1. 현재 계절을 선택하세요:", season_list)
cloth_name = st.text_input("2. 구매하려는 옷의 이름을 입력하세요:", placeholder="예: 기모 후드티")

# 중복 없이 모든 소재를 하나의 리스트로 합쳐서 선택지로 제공
all_materials = list(
    set(spring_materials + summer_materials + fall_materials + winter_materials)
)
selected_materials = st.multiselect(
    "3. 옷에 포함된 주요 소재를 모두 선택하세요 (비율 계산용):", all_materials
)

# 실행 버튼
if st.button("계절 적합도 분석하기"):
    if cloth_name == "" or len(selected_materials) == 0:
        st.warning("옷 이름과 소재를 모두 입력해 주세요!")
    else:
        # 메인 판별 함수 호출
        status, ratio, recommended_list = check_clothing_fit(
            current_season, selected_materials
        )

        st.divider()
        st.subheader(f"분석 결과: [{cloth_name}]은(는) {current_season}에 '{status}' 합니다!")
        st.write(f"📊 계절 적합 소재 비율: **{ratio:.1f}%**")

        # 3. 반복구조(for)를 활용하여 테이블(표) 형식으로 결과 도출
        st.write("### 📋 소재별 상세 분석표")
        table_data = []

        for mat in selected_materials:
            # 이유 판별 함수 호출
            reason_text = get_material_reason(current_season, mat, recommended_list)
            table_data.append({"선택한 소재": mat, "분석 결과 및 이유": reason_text})

        st.table(table_data)
