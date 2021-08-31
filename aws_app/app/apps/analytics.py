import plotly.express as px
import ast
import json
import pandas as pd
import streamlit as st
import boto3

def app():
    with st.form("Annotator's name"):
        ann_name = st.text_input("Annotator's name")
        submitted_name = st.form_submit_button('Submit name')

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('pog-dataset')

    try:
        my_bucket.download_file(ann_name+'_annotations.txt', ann_name+'_annotations.txt')

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The "+ann_name+'_annotations.txt'+" file was not found.")
        else:
            raise

    with open(ann_name+'_annotations.txt', 'r') as f:
        ann = f.readlines()

    ann = [ast.literal_eval(i) for i in ann]

    with open('all_categories_and_tags.json', encoding="utf8") as f:
        std_categories = json.load(f)

    all_occurrences_list = [next(iter(list(annotation.values())[0])) for annotation in ann]

    level_1_categories = [k for k, v in std_categories.items()]

    level_1_count_dict = {}

    for i in level_1_categories:
        level_1_count_dict[i] = all_occurrences_list.count(i)

    data = pd.DataFrame.from_dict(level_1_count_dict.items())
    data.columns=['Level 1 Categories', 'Number of values annotated for the category']

    fig = px.bar(data, x='Level 1 Categories', y='Number of values annotated for the category')
    #fig.show()
    st.plotly_chart(fig)

    #---------------------------------------------------------------------------

    with st.form('Level 1'):
        level_2_category = st.selectbox('Level 2 Category', level_1_categories)
        s = st.form_submit_button('Submit')

    if True:
        if True:
            std_categories_level_2 = [k for k, v in std_categories[level_2_category].items()]

            level_2_dicts = [list(annotation.values())[0] for annotation in ann if next(iter(list(annotation.values())[0])) == level_2_category]
            all_occurrences_list_level_2 = [next(iter(list(level_2_dict.values())[0])) for level_2_dict in level_2_dicts]

            level_2_count_dict = {}

            std_categories_level_2 = std_categories[level_2_category]

            level_2_categories = [k for k, v in std_categories_level_2.items()]

    with st.form('Level 2'):
        level_3_category = st.selectbox('Level 3 category', level_2_categories)
        s = st.form_submit_button('Submit')

        if True:

            for i in level_2_categories:
                level_2_count_dict[i] = all_occurrences_list_level_2.count(i)

            data_level_2 = pd.DataFrame.from_dict(level_2_count_dict.items())#, index=0

            data_level_2.columns=['Level 2 Categories', 'Number of values annotated for the category']

            fig_level_2 = px.bar(data_level_2, x='Level 2 Categories', y='Number of values annotated for the category')
            #fig_level_2.show()
            st.plotly_chart(fig_level_2)

    with st.form('Level 3'):
        std_categories_level_3 = [k for k, v in std_categories_level_2[level_3_category].items()]

        level_4_category = st.selectbox('Level 4 category', std_categories_level_3)
        s = st.form_submit_button('Submit')

        if True:

            std_categories_level_4 = std_categories[level_2_category][level_3_category][level_4_category]
            std_categories_level_4 = [k for k, v in std_categories_level_4.items()]

            level_3_dicts = [list(annotation.values())[0] for annotation in level_2_dicts if next(iter(list(annotation.values())[0])) == level_3_category]

            all_occurrences_list_level_4 = [list(annotation.values())[0][level_4_category] for annotation in level_3_dicts]

            level_4_count_dict = {}

            for i in std_categories_level_4:
                level_4_count_dict[i] = all_occurrences_list_level_4.count(i)

            data_level_4 = pd.DataFrame.from_dict(level_4_count_dict.items())#, index=0

            data_level_4.columns=['Level 4 Categories', 'Number of values annotated for the category']

            fig_level_4 = px.bar(data_level_4, x='Level 4 Categories', y='Number of values annotated for the category')
            st.plotly_chart(fig_level_4)
