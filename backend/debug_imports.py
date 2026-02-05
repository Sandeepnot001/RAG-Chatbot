
print("Start imports...")
import os
print("os imported")
from dotenv import load_dotenv
print("dotenv imported")
import google.generativeai as genai
print("genai imported")
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
print("langchain genai imported")
from langchain_community.vectorstores import Chroma
print("chroma imported")
print("All imports done.")
