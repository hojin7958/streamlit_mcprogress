import streamlit as st
import pandas as pd
import pandas as pd
import dataframe_image as dfi
import matplotlib as mpl
import matplotlib.font_manager as fm


mpl.font_manager.fontManager.addfont('malgun.ttf')

mpl.rcParams['font.family'] = 'Malgun Gothic'
mpl.rcParams['font.size'] = 25
import streamlit_ext as ste

def on_button_click():
    if "downloaded" not in st.session_state:
        st.session_state.downloaded = True
    st.session_state.downloaded = True



uploaded_file = st.file_uploader("엑셀 파일 업로드를 해주세요")

if uploaded_file is not None:
    ## SessionState 를 먼저 정의함
    if "downloaded" not in st.session_state:
        st.session_state.downloaded = False

    print("1", st.session_state.downloaded)

    df = pd.read_excel(uploaded_file)
    columns = df.columns.tolist()

    with st.form("m1"):
        options = st.selectbox(
            '실적주차를 선택해주세요',
            ('실적_1주차', '실적_2주차','실적_3주차','실적_4주차',"실적_5주차")
        )
    
        submitted = st.form_submit_button("실행하기")
        st.session_state.downloaded = False

    if submitted and st.session_state.downloaded == False:
        print("폼제출되고난뒤 세션스테이트")
        # st.write(columns)
        지점명s = ['GA2-3지점']

        df_columns = ['매니저명','현재대리점지사명','현재대리점설계사조직명','인보험실적','인정실적','이전월인정실적','전전월인정실적','이전월연속가동','현재지점조직명','매니저코드']
        df_columns.insert(3,options)
        print(df_columns)

        df2 = df[df_columns]
        for 지점 in 지점명s:
            df3 = df2[df2['현재지점조직명']==지점].copy()
            df3.sort_values('인정실적',ascending=False,inplace=True)
            df3['매니저코드'] = df3['매니저코드'].astype(object)
            managers = df3.매니저코드.unique()
            for manager in managers:
                df_manager = df3[(df3['매니저코드']==manager) & ((df3['이전월인정실적']>=200000) |(df3['전전월인정실적']>=200000) |(df3['인정실적']>=1)) ]
        #         print(df_manager.head())
                left_columns = ['매니저명','현재대리점지사명','현재대리점설계사조직명','인보험실적','인정실적','이전월인정실적','이전월연속가동','전전월인정실적']
                left_columns.insert(3,options)
                df_manager = df_manager[left_columns]
                try:
                    manager_name = df_manager.매니저명.unique()[0]
                except:
                    manager_name = "없음"
                    print("에러")
                file_name = str(지점)+"_"+str(manager)+"_"+str(manager_name)+'.PNG'
                dfi.export(df_manager.style.hide(axis='index'), file_name, max_cols=-1, max_rows=-1, table_conversion='matplotlib')
                with open(file_name, "rb") as file:
                    btn = ste.download_button(
                            label=str(manager)+"_"+str(manager_name),
                            data=file,
                            file_name=file_name,
                            mime="image/png",
                        )


