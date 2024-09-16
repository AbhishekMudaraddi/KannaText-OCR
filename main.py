
import pytesseract
from PIL import Image
import fitz  # PyMuPDF
import os
import cv2
import re

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_images_from_pdf(pdf_path, output_folder):
    pdf_document = fitz.open(pdf_path)
    image_counter = 0

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image_list = page.get_images(full=True)

        if not image_list:
            print(f"No images found on page {page_number} of {pdf_path}")
            continue

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            image_bytes = base_image["image"]
            image_filename = os.path.join(output_folder, f'image_{os.path.basename(pdf_path).replace(".pdf", "")}_page{page_number}_{img_index}.jpeg')
            with open(image_filename, "wb") as img_file:
                img_file.write(image_bytes)
            print(f"Extracted image {image_filename}")
            image_counter += 1

    pdf_document.close()
    return image_counter

def pre_process_image(image_path, processed_image_path):
    """Enhance contrast in a black and white image without altering quality."""
    img = cv2.imread(image_path)

    # Convert to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to enhance contrast
    img_contrast = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 11)
    
    # Save the pre-processed image
    cv2.imwrite(processed_image_path, img_contrast)

def extract_text_from_image(image_path):
    try:
        print(f"Processing {image_path} for text extraction...")
        processed_image_path = image_path.replace('.jpeg', '_processed.png')

        # Pre-process the image
        pre_process_image(image_path, processed_image_path)

        # Open the processed image
        image = Image.open(processed_image_path)

        # OCR with Kannada language model and layout preservation
        custom_config = r'--oem 3 --psm 6'  # Use psm 6 or try others like 3, 11, or 12 for better layout preservation
        text = pytesseract.image_to_string(image, lang='kan', config=custom_config)
        
        # Post-process the text to filter out unwanted content and maintain formatting
        filtered_text = filter_text(text)
        return filtered_text
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def filter_text(text):
    """Filter out unwanted text patterns while preserving main text and layout."""
    # Example regex patterns to remove unwanted text; adjust as needed
    unwanted_patterns = [
        r'\b(?:[0-9]{1,3}\s?)?[\w\-.]+\@(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,6}\b',  # Email addresses
        r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',  # IP addresses
        r'\b(?:https?:\/\/)?(?:www\.)?[\w\-]+\.\w+(?:\/[\w\-]+)*\b',  # URLs
        r'\b\d+\b',  # Isolated digits (if not relevant)
        # Add more patterns here as needed
    ]

    # Remove unwanted text using regex
    for pattern in unwanted_patterns:
        text = re.sub(pattern, '', text)

    # Remove unwanted punctuation
    text = re.sub(r'[“”\'\'"]', '', text)  # Remove double quotes and single quotes
    text = re.sub(r'[;]', '', text)  # Remove semicolons
    text = re.sub(r'[.]', '', text)  # Remove full stops
    
    # Preserve line breaks and spacing
    text = re.sub(r'\n+', '\n', text).strip()
    
    return text

def process_pdf_folder(pdf_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        text_output_path = os.path.join(output_folder, pdf_file.replace('.pdf', '.txt'))

        # Open text file to write extracted content
        with open(text_output_path, "w", encoding="utf-8") as text_file:
            # Extract images from the PDF           
            num_images = extract_images_from_pdf(pdf_path, output_folder)
            print(f"Extracted {num_images} images from {pdf_file}.")

            # Extract text from images and save to text file
            for img_file in os.listdir(output_folder):
                if img_file.startswith(f'image_{os.path.basename(pdf_file).replace(".pdf", "")}') and img_file.endswith('.jpeg'):
                    image_path = os.path.join(output_folder, img_file)
                    text = extract_text_from_image(image_path)
                    if text:
                        text_file.write(f"--- Text from {img_file} ---\n")
                        text_file.write(text)
                        text_file.write("\n\n")
                    else:
                        print(f"No text found in {image_path}")
        
        print(f"Text extracted and saved to {text_output_path}")

def main():
    pdf_folder = r"locationOfYourInputFolder"   #path of input folder that contains the pdf for OCR  
    output_folder = r"locationOfYourOutputFolder" #path of output folder that should be created 
    # Process all PDFs in the folder
    process_pdf_folder(pdf_folder, output_folder)

if __name__ == "__main__":
    main()



