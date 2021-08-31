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
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('pog-dataset')

    #Clearing out any excess images
    filelist = [f for f in os.listdir() if (f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png"))]
    for f in filelist:
        os.remove(f)


    with st.sidebar:
        with st.form("Annotator's name"):
            ann_name = st.text_input("Annotator's name")
            submitted_name = st.form_submit_button('Submit name')

        main_path = 'data'

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
                #outfits = os.listdir(path)
                #outfits = [object_summary.key[7:] for object_summary in my_bucket.objects.filter(Prefix=outfit_path)]

                #with open(ratings_file_path) as f:
                #  content = f.readlines()
                #  content = [x.strip() for x in content]
                #  rated_outfits = [str(ast.literal_eval(i)["outfit"]) for i in content]
                #  outfits_list = [x for x in outfits if x not in rated_outfits]

                #outfits_list = [x[0] for x in os.walk(path)]
    col0, col1, col2, col3 = st.beta_columns(4)
    try:
        col0.write("Pick outfit number")#+str(len(outfits_list)))
    except UnboundLocalError:
        pass
        a = """# Steps to start:

                    1. In the left sidebar, submit your name,

                    2. the brand,

                    3. and the outfit type.

                    4. Then press the 'Start annotating' button."""

    ind = col0.number_input('Outfit number', step=1)

    #true_ind = outfits_list[ind]
    outfit_path = 'data/'+brand+'/'+outfit_type+'/'+str(ind)

    files = [object_summary.key.replace(outfit_path+'/', "") for object_summary in my_bucket.objects.filter(Prefix=outfit_path)]

    for file in files:
        try:
            my_bucket.download_file(outfit_path+'/'+file, file)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise

    images = files
    for i in range(0, len(images)):
        try:
            p = Image.open(images[i])
            if i%3 == 0:
                col1.image(p)
            if i%3 == 1:
                col2.image(p)
            if i%3 == 2:
                col3.image(p)

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

    with st.form('Rate this outfit out of 10:'):
        outfit_types_list = ["Dress", "Jeans-top"]
        rating = col0.selectbox("Rating", range(1, 6))
        submitted_rating = st.form_submit_button('Submit')
        if submitted_rating == True:
            ratings_file_path = ann_name+"_"+brand+"_"+outfit_type+"_ratings.txt"
            with open(ratings_file_path, "a") as f:
                f.write(str({"outfit": ind,
                         "rating": rating})+'\n')
            st.success("Rating saved successfully for the outfit. The "+ann_name+"_"+brand+"_"+outfit_type+"_ratings.txt file has been updated.")
            for image in images:
                os.remove(image)
