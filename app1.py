#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Microsoft. All rights reserved.
# Licensed under the MIT license. See LICENSE.md file in the project root for full license information.

import logging
import sys
import requests
import time
import os
import swagger_client
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
        format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p %Z")

# Your subscription key and region for the speech service
SUBSCRIPTION_KEY = "XXX"
SERVICE_REGION = "eastus"
BLOB_STORAGE_CONNECTION_STRING = "xxx"
CONTAINER_NAME = "edu"

NAME = "Simple transcription"
DESCRIPTION = "Simple transcription description"

LOCALE = "en-US"
RECORDINGS_BLOB_URI = "xx"

# Extract the base name of the audio file to use it for naming the transcription file
audio_file_name = os.path.basename(RECORDINGS_BLOB_URI).split('?')[0]
transcription_file_name = f"{audio_file_name}_transcript.out"

# Provide the uri of a container with audio files for transcribing all of them
# with a single request. At least 'read' and 'list' (rl) permissions are required.
RECORDINGS_CONTAINER_URI = "xxx"

# Set model information when doing transcription with custom models
MODEL_REFERENCE = None  # guid of a custom model


def transcribe_from_single_blob(uri, properties):
    """
    Transcribe a single audio file located at `uri` using the settings specified in `properties`
    using the base model for the specified locale.
    """
    transcription_definition = swagger_client.Transcription(
        display_name=NAME,
        description=DESCRIPTION,
        locale=LOCALE,
        content_urls=[uri],
        properties=properties
    )

    return transcription_definition


def transcribe():
    logging.info("Starting transcription client...")

    # configure API key authorization: subscription_key
    configuration = swagger_client.Configuration()
    configuration.api_key["Ocp-Apim-Subscription-Key"] = SUBSCRIPTION_KEY
    configuration.host = f"https://{SERVICE_REGION}.api.cognitive.microsoft.com/speechtotext/v3.1"

    # create the client object and authenticate
    client = swagger_client.ApiClient(configuration)

    # create an instance of the transcription api class
    api = swagger_client.CustomSpeechTranscriptionsApi(api_client=client)

    # Specify transcription properties by passing a dict to the properties parameter. See
    # https://learn.microsoft.com/azure/cognitive-services/speech-service/batch-transcription-create?pivots=rest-api#request-configuration-options
    # for supported parameters.
    properties = swagger_client.TranscriptionProperties()

    # Use base models for transcription. Comment this block if you are using a custom model.
    transcription_definition = transcribe_from_single_blob(RECORDINGS_BLOB_URI, properties)

    created_transcription, status, headers = api.transcriptions_create_with_http_info(transcription=transcription_definition)

    # get the transcription Id from the location URI
    transcription_id = headers["location"].split("/")[-1]

    # Log information about the created transcription. If you should ask for support, please
    # include this information.
    logging.info(f"Created new transcription with id '{transcription_id}' in region {SERVICE_REGION}")

    logging.info("Checking status.")

    completed = False
    transcription_results = ""

    while not completed:
        # wait for 5 seconds before refreshing the transcription status
        time.sleep(5)

        transcription = api.transcriptions_get(transcription_id)
        logging.info(f"Transcriptions status: {transcription.status}")

        if transcription.status in ("Failed", "Succeeded"):
            completed = True

        if transcription.status == "Succeeded":
            pag_files = api.transcriptions_list_files(transcription_id)
            for file_data in _paginate(api, pag_files):
                if file_data.kind != "Transcription":
                    continue

                audiofilename = file_data.name
                results_url = file_data.links.content_url
                results = requests.get(results_url)
                transcription_results = results.content.decode('utf-8')
                logging.info(f"Results for {audiofilename}:\n{transcription_results}")
        elif transcription.status == "Failed":
            logging.info(f"Transcription failed: {transcription.properties.error.message}")

    # Save the transcription results to a file with the audio file's base name
    with open(transcription_file_name, "w") as file:
        file.write(transcription_results)

    # Upload the file to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(BLOB_STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=transcription_file_name)

    with open(transcription_file_name, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
        logging.info(f"Transcription saved to Azure Blob Storage as '{transcription_file_name}'")


def _paginate(api, paginated_object):
    """
    The autogenerated client does not support pagination. This function returns a generator over
    all items of the array that the paginated object `paginated_object` is part of.
    """
    yield from paginated_object.values
    typename = type(paginated_object).__name__
    auth_settings = ["api_key"]
    while paginated_object.next_link:
        link = paginated_object.next_link[len(api.api_client.configuration.host):]
        paginated_object, status, headers = api.api_client.call_api(link, "GET",
            response_type=typename, auth_settings=auth_settings)

        if status == 200:
            yield from paginated_object.values
        else:
            raise Exception(f"could not receive paginated data: status {status}")


if __name__ == "__main__":
    transcribe()
