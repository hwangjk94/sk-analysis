import pandas as pd
import streamlit as st

def show_strategy_analysis(sheet):
    st.header("📊 상대 덱별 파훼법 분석")
    
    # 1. 데이터 불러오기
    raw_data = sheet.get_all_records()
    if not raw_data:
        st.info("아직 분석할 데이터가 없습니다. 기록을 먼저 입력해주세요.")
        return
        
    df = pd.DataFrame(raw_data)

    # 2. 분석 대상 선택 (상대 방어 덱 기준)
    all_opp_decks = df['상대 덱'].unique().tolist()
    target_opp = st.selectbox("🎯 공략법을 확인할 상대 방어 덱 선택", all_opp_decks)

    if target_opp:
        # 해당 방어 덱을 상대한 기록만 필터링
        filtered_df = df[df['상대 덱'] == target_opp]
        
        # 3. 통계 계산
        total_battles = len(filtered_df)
        wins = len(filtered_df[filtered_df['결과'] == '승리'])
        win_rate = (wins / total_battles) * 100
        
        st.subheader(f"[{target_opp}] 공략 현황")
        st.write(f"📈 전체 승률: **{win_rate:.1f}%** ({total_battles}전 {wins}승)")

        # 4. 가장 성적이 좋은 아군 조합 찾기
        # 승리한 기록만 추출
        victory_df = filtered_df[filtered_df['결과'] == '승리']
        
        if not victory_df.empty:
            st.success("✅ 추천 공략 조합")
            
            # 아군 덱+펫 조합별 승리 횟수 카운트
            best_decks = victory_df.groupby(['내 덱', '아군 펫']).size().reset_index(name='승리횟수')
            best_decks = best_decks.sort_values(by='승리횟수', ascending=False)
            
            for index, row in best_decks.iterrows():
                with st.expander(f"추천 {index+1}: {row['내 덱']} (+{row['아군 펫']}) - {row['승리횟수']}회 성공"):
                    # 해당 조합의 메모(장비 세팅)들만 모아서 보여주기
                    notes = victory_df[(victory_df['내 덱'] == row['내 덱']) & 
                                     (victory_df['아군 펫'] == row['아군 펫'])]['메모'].unique()
                    st.write("**📝 수집된 세팅 정보:**")
                    for n in notes:
                        if n: st.write(f"- {n}")
        else:
            st.error("❌ 아직 이 덱을 상대로 승리한 기록이 없습니다. 새로운 파훼법이 필요합니다!")

# 메인 실행부에서 호출 (예시)
# show_strategy_analysis(sheet)