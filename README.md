# KannaText-OCR
This project extracts handwritten Kannada text from PDF images using PyMuPDF and Tesseract OCR. It processes images for better contrast using OpenCV, improving text recognition accuracy. The script also filters out unwanted patterns like URLs and digits, ensuring clean output. This tool is ideal for digitizing Kannada handwritten documents.


# Kannada Handwritten Text Extraction

This repository contains a Python code for extracting handwritten Kannada text from images embedded in PDF files. The code uses PyMuPDF for extracting images and Tesseract OCR for recognizing the text. The text is pre-processed to enhance contrast for better OCR results.

## Features
- Extracts images from PDFs.
- Pre-processes images to enhance contrast and improve OCR accuracy.
- Extracts handwritten Kannada text using Tesseract OCR.
- Filters out unwanted patterns (emails, URLs, IP addresses) from the extracted text.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.x
- Tesseract-OCR: Download and install from [here](https://github.com/tesseract-ocr/tesseract).
  - Ensure to set the `pytesseract.pytesseract.tesseract_cmd` path correctly in the code.
- Required Python libraries:
  - `pytesseract`
  - `Pillow`
  - `PyMuPDF` (fitz)
  - `opencv-python`
  - `re`
## Remember
- The quality and of the text extrated depends on the scanned images. 
- The accuracy of the extracted text increased for good and clear scanned images.
- Problem may arise if the images are not clear.

To install the required libraries, run the following command:

```bash
pip install pytesseract Pillow PyMuPDF opencv-python



