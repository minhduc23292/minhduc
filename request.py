import requests, os
from io import BytesIO
from PIL import Image
current_directory = os.path.dirname(os.path.realpath(__file__))
def send_file(url, file_path):
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Prepare the files dictionary for the multipart form data
            files = {'file': file}

            # Send the POST request with the file
            response = requests.post(url, files=files)

            # Check the response status
            if response.status_code == 200:
                print("File uploaded successfully.")
                print(response.text)
            else:
                print(f"Failed to upload file. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Read the image data from the response content
            image_data = BytesIO(response.content)
            # Open the image using PIL (Python Imaging Library)
            image = Image.open(image_data)
            return image
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

image_url = 'https://icdn.dantri.com.vn/2023/07/29/cover-pc-1690627578830.jpg'
url = 'http://httpbin.org/post'
file_path = f"{current_directory}/image/test.py"
send_file(url, file_path)
downloaded_image = download_image(image_url)
if downloaded_image:
    # Do something with the downloaded image here
    # downloaded_image.show()  # Display the image using th
    downloaded_image.save(f"{current_directory}/storage/" + 'MyQRCode2.jpg')
    print("hahaha")