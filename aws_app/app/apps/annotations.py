import os.path
import streamlit as st
import json
import boto3
from PIL import Image
import glob
#import botocore

def app():
    with open('all_categories_and_tags.json', encoding="utf8") as f:
        data = json.load(f)

    #THE SIDEBAR
    with st.sidebar:
        with st.form('Category'):
            categories_list = []
            for i in data:
                categories_list.append(i)
            category = st.selectbox('Category', categories_list)
            submitted_cat = st.form_submit_button('Submit')
            if submitted_cat:
                pass
        with st.form('Index'):
            indices = []
            for i in data[category]:
                indices.append(i)
            index = st.selectbox('Index', indices)
            submitted_ind = st.form_submit_button('Submit')
            if submitted_ind:
                pass

    #DATA CLEANING
    if 'editable' in data[category][index]:
        del data[category][index]['editable']
    if 'alias' in data[category][index]:
        del data[category][index]['alias']


    #THE MAIN PAGE

    #Dividing into three columns
    image_view_col, attributes_and_tags_col1, attributes_and_tags_col2, attributes_and_tags_col3 = st.beta_columns(4)

    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('pog-dataset')
    images = [object_summary.key[7:] for object_summary in my_bucket.objects.filter(Prefix="images/")]


    ind = image_view_col.number_input('Index of image', step=1)

    try:
        my_bucket.download_file('images/'+images[int(ind)], images[int(ind)])

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

    image = Image.open(images[int(ind)])

    image_filename = os.path.basename(image.filename)
    image_view_col.write("Showing image " + image_filename + " at index " + str(ind))
    image_view_col.image(image, use_column_width=True)


    tags_temp_list = []
    count = 0
    with st.form('Attributes and tags'):
        for attribute in data[category][index]:
            options = list(data[category][index][attribute])[:-2]
            if count < 7: #write in column 2
                tag = attributes_and_tags_col1.selectbox(attribute, options, key=str(count))
            elif 7 < count < 15: #write in column 3
                tag = attributes_and_tags_col2.selectbox(attribute, options, key=str(count))
            else: #write in column 4
                tag = attributes_and_tags_col3.selectbox(attribute, options, key=str(count))
            tags_temp_list.append(tag)
            count += 1


        submitted = st.form_submit_button('Submit')
        if submitted:
            att_tag_dict = {}
            for attribute, tag in zip(data[category][index], tags_temp_list):
                att_tag_dict[attribute] = tag
                
            penultimate_result = {index: att_tag_dict}
            final_result = {category: penultimate_result}
            st.header("Result:")
            st.write(final_result)
            j_filename = image_filename + ".json"
            with open('annotations.txt', 'a') as f:
                f.write(str({j_filename:final_result})+'\n')
                st.success('Annotations for '+ j_filename + ' have been saved successfully in annotations.txt')

    if st.button('Corrupted or invalid image'):
        with open('annotations.txt', 'a') as f:
            f.write(str({j_filename:'invalid_img'})+'\n')
            st.success('The product '+ j_filename + ' has been marked as invalid in annotations.txt')
