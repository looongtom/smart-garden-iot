import cloudinary
import requests
from PIL import Image
from io import BytesIO
from tensorflow.keras.preprocessing.image import load_img

# Configure Cloudinary with your account details
cloudinary.config(
    cloud_name="dsjuckdxu",
    api_key="973371356842627",
    api_secret="zJ5bMJgfkw3XBdyBocwO8Kgs1us"
)

# Specify the public ID of the image you want to download
public_id = "fgawmdwzvs4nkfs8vzql"



# Construct the URL of the image based on the public ID
image_url = cloudinary.utils.cloudinary_url(public_id)[0]

# Download the image from Cloudinary
response = requests.get(image_url)
image_content = response.content

# Open the image using PIL (Python Imaging Library)
image_pil = Image.open(BytesIO(image_content))

target_size = (128, 128)
image_tensor = load_img(BytesIO(image_content), target_size=target_size)

# Now you can work with the 'image_tensor' variable
# For example, you can convert it to a NumPy array
image_array = image_tensor

# Display the image using Matplotlib or any other method if needed
# For example:
import matplotlib.pyplot as plt
plt.imshow(image_array)
plt.show()