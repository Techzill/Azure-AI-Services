# 📄 Document Processing & Retrieval Projects

This repository contains three main projects demonstrating the use of Flask web applications, Azure Cognitive Services, and Azure OpenAI for RAG. These projects handle document processing, table extraction, invoice field extraction, and question answering from custom data sources.

# 🏷️ Project 1: Table Extraction from Documents

O## bjective:
Build a web application that extracts tables from uploaded documents using Azure Form Recognizer.

## Workflow:

Created a Flask web app with routes to upload documents.

Configured Azure Form Recognizer with endpoint, key, and custom model ID.

Implemented table extraction logic that captures cell content and organizes rows and columns.

Returned extracted tables in structured JSON format for downstream use.

Error handling for invalid or missing files.

## Outcome:

Users can upload documents via a web interface.

Extracted tables are returned as structured JSON.

Suitable for automated processing of forms, invoices, or reports.

# 🧾 Project 2: Invoice Field Extraction

## Objective:
Extract key fields from invoices using Azure Form Recognizer via a Flask web app.

## Workflow:

Created a Flask app with file upload capability.

Integrated Azure Form Recognizer with a pre-trained invoice model.

Saved uploaded files securely on the server.

Extracted fields such as Amount Due, Invoice No, Bill To, Subtotal, Total, and tax information.

Returned extracted data as formatted JSON responses.

Implemented logging and error handling for robust operation.

## Outcome:

Enables automated extraction of structured data from invoices.

Provides JSON output ready for further processing or database storage.

# 🤖 Project 3: RAG (Retrieval-Augmented Generation) with Azure OpenAI

## Objective:
Build a system that answers user questions using custom knowledge bases via Azure Cognitive Search and Azure OpenAI.

## Workflow:

Configured environment variables for Azure OpenAI and Azure Cognitive Search.

Created a Python script to send user queries to an Azure OpenAI model.

Integrated external knowledge sources via Azure Cognitive Search as a data retrieval layer.

Configured the system to return responses with optional citations.

Demonstrated end-to-end workflow for question-answering using custom data.

## Outcome:

Users can query domain-specific knowledge with context-aware answers.

Combines retrieval of relevant documents with AI-generated responses.

Supports enhanced decision-making and information discovery.

# 🔑 Key Features

End-to-end document processing pipelines.

Web-based file upload interface using Flask.

Integration with Azure Form Recognizer for table and invoice extraction.

RAG setup with Azure Cognitive Search and Azure OpenAI for Q&A.

JSON outputs suitable for further processing or analytics.

# 🧰 Technologies Used

Python 3.13

Flask 2.3.4

Azure Form Recognizer

Azure OpenAI / Cognitive Search

JSON, Logging, OS modules

HTML templates for file upload interfaces
