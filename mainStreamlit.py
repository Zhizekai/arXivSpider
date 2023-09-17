import streamlit as st
import url as _url

import datetime
"""
streamlit run ./mainStreamlit.py 
"""
st.title('订阅arxiv最新文章')
query_params = {}

title = st.text_input('标题', placeholder='请输入标题')

col1, col2 = st.columns(2)

with col1:
    abstract = st.text_input('摘要', placeholder='请输入摘要')

with col2:
    authors = st.text_input('作者', placeholder='请输入作者')

# classification_computer_science = st.text_input('类型', placeholder='请输入标题')
st.subheader('Subject')
cs = st.checkbox(':rainbow[Computer Science (cs)]')
math = st.checkbox('***Mathematics (math)***')
eess = st.checkbox('***Electrical Engineering and Systems Science (eess)***')
st.subheader('Date')
col1, col2 = st.columns(2)

with col1:
    date_from_date = st.date_input("From", datetime.date(2021, 7, 6))
    st.write('开始日期是:', date_from_date.strftime('%Y-%m-%d'))

with col2:
    date_to_date = st.date_input("To", datetime.date(2022, 7, 6))
    st.write('结束日期是:', date_to_date.strftime('%Y-%m-%d'))

sender = st.text_input('SMTP邮箱', '1310248516@qq.com')
st.write('smtpserver:', sender)


# title = st.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)
# title = st.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)
# title = st.text_input('Movie title', 'Life of Brian')
# st.write('The current movie title is', title)

def main_test():
    if title:
        query_params['title'] = title
    if abstract:
        query_params['abstract'] = abstract
    if authors:
        query_params['authors'] = authors
    query_params['subject'] = []
    if cs:
        query_params['subject'].append('cs')
    if math:
        query_params['subject'].append('math')
    if eess:
        query_params['subject'].append('eess')

    if date_from_date and date_to_date:
        query_params['date-from_date'] = date_from_date.strftime('%Y-%m-%d')
        query_params['date-to_date'] = date_to_date.strftime('%Y-%m-%d')

    print(_url.get_url('bcai',query_params))


st.button("就是现在，开始获取最新文章", type="primary", use_container_width=True, on_click=main_test)
