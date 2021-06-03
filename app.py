#Import necessary libraries
from flask import Flask, render_template, request
 
import numpy as np
import os
 
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
 
#load model
model =load_model("my_model1.h5")
 
print('@@ Model loaded')
 
 
def pred_waste(waste):
  test_image = load_img(waste, target_size = (200, 200)) # load image 
  print("@@ Got Image for prediction")
   
  X = img_to_array(test_image) # convert image to np array and normalize
  X = np.expand_dims(X, axis = 0) # change dimention 3D to 4D
  images = np.vstack([X])
  result = model.predict(images) # predict waste class
  print('@@ Raw result = ', result)
   
  if result == 0:
    print("organic")
    return "Organic", 'portfolio-details.html' # if index 0 organic
  else:
      print("recyclic")
      return "Recyclic", 'portfolio-details -1.html' # # else recyclic
 
#------------>>pred_waste<<--end
     
 
# Create flask instance
app = Flask(__name__)
 
# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')
     
  
# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] # fet input
        filename = file.filename        
        print("@@ Input posted = ", filename)
         
        file_path = os.path.join('static/user uploaded', filename)
        file.save(file_path)
 
        print("@@ Predicting class......")
        pred, output_page = pred_waste(waste=file_path)
               
        return render_template(output_page, pred_output = pred, user_image = file_path)
     
# For local system &amp; cloud
if __name__ == "__main__":
    app.run(threaded=False)