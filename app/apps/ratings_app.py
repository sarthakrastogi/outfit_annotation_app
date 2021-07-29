import streamlit as st
import boto3
from PIL import Image
from PIL import UnidentifiedImageError
import os
import glob
import PIL
import ast

#docker run -t -i -v C:\\Users\\hp\\Downloads\\:app\data

def app():
    with st.sidebar:
        with st.form("Annotator's name"):
            ann_name = st.text_input("Annotator's name")
            submitted_name = st.form_submit_button('Submit name')
            
        main_path = '/content/drive/MyDrive/data'
        main_dl_path = '/content/drive/MyDrive'
        #with st.form("Main path"):
            #main_dl_path = st.text_input("Downloads folder path")
            #submitted_path = st.form_submit_button('Submit')

        with st.form('Brand'):
            brands_list = ["Ballantynes", "Myers", "David Jones", "Farfetch"]
            brand = st.selectbox('Brand', brands_list)
            submitted_brand = st.form_submit_button('Submit')

        with st.form('Type of outfit: Dress or Jeans-top?'):
            outfit_types_list = ["dress", "jeans-top"]
            outfit_type = st.selectbox('Type of outfit', outfit_types_list)
            submitted_outfit_type = st.form_submit_button('Submit')
            
        with st.form('Load indices'):
            if st.form_submit_button('Start annotating'):
                path = os.path.join(main_path, brand, outfit_type)
                outfits = os.listdir(path)
                with open('/content/drive/MyDrive/_Ballantynes_dress_ratings.txt') as f:
                  content = f.readlines()
                  content = [x.strip() for x in content]
                  rated_outfits = [str(ast.literal_eval(i)["outfit"]) for i in content]
                  outfits_list = [x for x in outfits if x not in rated_outfits]

    #outfits_list = [x[0] for x in os.walk(path)]
    col0, col1, col2, col3 = st.beta_columns(4)
    try:
        col0.write("Pick outfit number from 0 to "+str(len(outfits_list)))
    except UnboundLocalError:
        st.header('Submit the neceessary details and press the "Start annotating" button.')
        st.header('---')
        st.header('---')
        st.header('---')
        st.header('---')
        st.header('---')
        st.header('---')
        st.header('---')
        st.header('---')
        st.header('---')
        #return
    ind = col0.number_input('Outfit number', step=1)
    #ind = col0.
    #with open('/content/drive/MyDrive/rated_outfits_list.txt', 'r') as f:
        
    true_ind = outfits_list[ind]
    path = os.path.join(path, str(true_ind))
    #images = glob.glob(path + '\*')
    images = os.listdir(path)
    st.write(images)
    for i in range(0, len(images)):
        try:
            p = Image.open(os.path.join(path, images[i]))
            if i%3 == 0:
                col1.image(p)
                #col1.write(1)
            if i%3 == 1:
                col2.image(p)
                #col2.write(2)
            if i%3 == 2:
                col3.image(p)
                #col3.write(3)

        except UnidentifiedImageError:
            pass
            if i%3 == 0:
                col1.write('Corrupted image!')
            if i%3 == 1:
                col2.write('Corrupted image!')
            if i%3 == 2:
                col3.write('Corrupted image!')
        except IndexError:
            pass
    ratings_file_path = main_dl_path+"/"+ann_name+"_"+brand+"_"+outfit_type+"_ratings.txt"
    with st.form('Rate this outfit out of 10:'):
        outfit_types_list = ["Dress", "Jeans-top"]
        rating = col0.selectbox("Rating", range(1, 11))
        submitted_rating = st.form_submit_button('Submit')
        if submitted_rating == True:
            with open(ratings_file_path, "a") as f:
                f.write(str({"outfit": true_ind,
                         "rating": rating})+'\n')
            st.success("Rating saved successfully for the outfit. The"+ann_name+"_"+brand+"_"+outfit_type+"_ratings.txt file is saved in "+main_dl_path)

    with st.form('Upload the current ratings file'):
        if st.form_submit_button('Upload Files'):
            s3 = boto3.client('s3')
            s3.upload_file(ratings_file_path, "pog-dataset", ann_name+"_"+brand+"_"+outfit_type+"_ratings.txt")
            st.success('File uploaded successfully.')

    with st.form('Download the ratings.txt file from the bucket'):
        if st.form_submit_button('Download'):
            s3 = boto3.resource('s3')

            try:
                s3.Bucket('pog-dataset').download_file(ratings_file_path, main_dl_path+ann_name+"_"+brand+"_"+outfit_type+"_ratings.txt")
                st.success(ann_name+"_"+brand+"_"+outfit_type+"_ratings.txt"+" downloaded to Downloads successfully")
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == "404":
                    print("The object does not exist.")
                else:
                    raise
