import streamlit as st
import requests
import json
import fitz  
import os
from imgurpython import ImgurClient

# Define the endpoint URL
API_ENDPOINT = "https://54c7-34-139-251-107.ngrok-free.app/chat"


# Cấu hình Imgur
CLIENT_ID = 'fd01c7acf682570'  # Thay bằng Client ID của bạn
CLIENT_SECRET = '6b098a76e7c8ee0172fb61fb5730a11d9b82f33c'  # Thay bằng Client Secret của bạn
client = ImgurClient(CLIENT_ID, CLIENT_SECRET)

def pdf_to_images_and_upload(pdf_path):
    doc = fitz.open(pdf_path)
    image_links = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        image_filename = f"page_{page_num + 1}.png"
        pix.save(image_filename)

        # Tải hình ảnh lên Imgur
        image = client.upload_from_path(image_filename)
        image_links.append(image['link'])

        # Xóa hình ảnh sau khi tải lên
        os.remove(image_filename)

    return image_links


# Đường dẫn đến file PDF
pdf_path = r"C:\Users\PC\Desktop\Slide\data\data\41 2018 Quy che CTP trong nuoc.pdf"  # Thay bằng đường dẫn đến file PDF của bạn

# Tạo list các link hình ảnh từ PDF
image_url_list = pdf_to_images_and_upload(pdf_path)

# Streamlit UI setup
st.title("LLAMA 3.2 Multimodal")
st.write("Extract text from predefined image URLs with a predefined prompt")

# Fixed prompt: "Trích xuất văn bản từ hình ảnh. Chỉ trả về văn bản, không cần giải thích."
prompt = "Trích xuất văn bản từ hình ảnh. Chỉ trả về văn bản, không cần giải thích."

# Create columns for output
col1, col2 = st.columns(2)

# Extract text for each image when the button is clicked
with col2:
    if st.button("Extract Text"):
        for idx, image_url in enumerate(image_url_list):
            # Display each image in the left column
            with col1:
                st.image(image_url, caption=f"Image {idx + 1}", use_column_width=True)

            # Prepare the API request payload
            payload = {
                "image_url": image_url,
                "prompt": prompt  # Use the fixed prompt for all images
            }

            try:
                # Make the POST request to the Flask API
                response = requests.post(API_ENDPOINT, json=payload)

                if response.status_code == 200:
                    data = response.json()
                    
                    # Display the extracted content
                    st.markdown(f"### Extracted Content for Image {idx + 1}")
                    st.markdown(data["content"])

                    # Create a unique file name for each image's extracted text
                    file_name = f"C:/Users/PC/Desktop/Chatbot/pdf_chat/data/extracted_content_image_{idx + 1}.txt"
                    
                    # Save only the extracted content to a separate file for each image
                    with open(file_name, "w", encoding="utf-8") as file:
                        file.write(f"{data['content']}\n")

                    st.success(f"Text content saved to {file_name}")

                else:
                    st.error(f"Error for Image {idx + 1}: " + response.json().get("error", "Unable to extract text"))

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API for Image {idx + 1}: {e}")
