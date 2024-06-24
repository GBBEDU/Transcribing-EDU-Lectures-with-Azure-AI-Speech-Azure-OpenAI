# Transcribing-EDU-Lectures-with-Azure-AI-Speech-Azure-OpenAI

Description: Courses are transcribed and stored in text files in Blob Storage using Azure Speech Services. Utilize Azure OpenAI models to chat with the transcribed text data.

How to Use the Speech Services Batch Transcription API from Python

Step-by-Step Guide
1. Download and Install the API Client Library

To execute the sample, you need to generate the Python library for the REST API through Swagger. Follow these steps for installation:

Go to Swagger Editor.
Click File, then Import URL.
Enter the Swagger URL for the Speech Services API: https://raw.githubusercontent.com/Azure/azure-rest-api-specs/main/specification/cognitiveservices/data-plane/Speech/SpeechToText/stable/v3.1/speechtotext.json.
Click Generate Client and select Python.
Save the client library.
Extract the downloaded python-client-generated.zip somewhere on your file system.
Install the extracted Python client module in your Python environment using pip install path/to/package/python-client.
Verify the installation with python -c "import swagger_client".
2. Install Other Dependencies

The sample uses the requests library. You can install it with the command:

sh
Copy code
pip install requests
3. Run the Sample Code

The sample code (main.py) can be run using Python 3.7 or higher. You need to adapt the following information:

Cognitive Services subscription key and region:

Get the subscription key from the "Keys and Endpoint" tab on your Cognitive Services or Speech resource in the Azure Portal.
Batch transcription is available only for paid subscriptions.
Refer to the region identifiers in the expected format.
URI of an audio recording in Blob Storage:

Refer to the Azure Storage documentation for information on authorizing access against Blob Storage.
Optional: The model ID of an adapted model for custom models.

Optional: The URI of a container with audio files to transcribe all of them with a single request.

4. Development Environment

Use an environment like Visual Studio Code to edit, debug, and execute the sample.

Benefits for EDU ISV Accounts
1. Automate Repetitive Tasks

Use Azure Speech Services to transcribe lectures and store them in Blob Storage.
Employ Azure OpenAI models to enable interactive Q&A sessions with the transcribed text data, providing quick answers to students’ questions.
2. Scalable AI Solutions

Develop products that can be replicated and scaled across different educational institutions.
Use Azure AI models to enhance the educational experience by providing real-time answers and insights.
3. Tools and Upgrades

Utilize tools like Postman to verify API endpoints and ensure they receive the expected JSON payloads.
Educate customers on the necessary tools and steps for upgrading their systems to leverage Azure AI capabilities effectively.
4. AI-Driven Learning

Leverage the power of Azure OpenAI to create intelligent educational tools that can assist both teachers and students.
Enable seamless integration of transcribed data into interactive learning modules, enhancing the overall educational experience.
