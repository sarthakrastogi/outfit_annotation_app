import os.path
import streamlit as st
import json
import boto3
#if True:

def app():
    with open('all_categories_and_tags.json', encoding="utf8") as f:
        data = json.load(f)

    #THE SIDEBAR
    st.sidebar.header("Step 1")
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
            #if st.sidebar.button('Load data'):
                #pass #load_data()


    #DATA CLEANING
    if 'editable' in data[category][index]:
        del data[category][index]['editable']
    if 'alias' in data[category][index]:
        del data[category][index]['alias']


    #THE MAIN PAGE

    #Dividing into three columns
    image_view_col, attributes_and_tags_col1, attributes_and_tags_col2, attributes_and_tags_col3 = st.beta_columns(4)

    #FIRST COLUMN: FOR IMPORTING AND DISPLAYING IMAGE



    from PIL import Image
    import glob
    path = '/content/drive/MyDrive/images'
    images = glob.glob(path + '/*')
    #index = int(st.number_input('Index'))
    #st.write(images[0])


    ind = image_view_col.number_input('Index of image', step=1)


    image = Image.open(images[int(ind)])

    image_filename = os.path.basename(image.filename)
    image_view_col.write("Showing image " + image_filename + " at index " + str(ind))
    image_view_col.image(image, use_column_width=True)



    #SECOND COLUMN: FOR ATTRIBUTES
    #THIRD COLUMN: FOR TAGS
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
            #st.write(att_tag_dict)

            penultimate_result = {index: att_tag_dict}
            #st.write(penultimate_result)

            final_result = {category: penultimate_result}
            st.header("Result:")
            st.write(final_result)
            #image_filename = "xyz" #later find a way to get image filename
            j_filename = image_filename + ".json"
            with open('/content/drive/MyDrive/annotations.txt', 'a') as f:
                f.write(str({j_filename:final_result}))
                #json.dump(final_result, f)
            if st.button('Upload to Bucket'):
                s3 = boto3.resource('s3')
                s3.create_bucket(Bucket= 'pog-dataset')
                s3.Object('pog-dataset','annotations.txt').upload_file(Filename='annotations.txt')
                st.success("Saved annotations for the image " + image_filename + " as corresponding to " + j_filename)
