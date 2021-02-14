from google.cloud import storage, speech
from app.utils import generate_name, get_gsc_uri
from app.constants import STORAGE_BUCKET


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


# [START speech_transcribe_async_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    full_transcript = ''
    for result in response.results:

        # The first alternative is the most likely one for this portion.

        full_transcript += result.alternatives[0].transcript

        print("Transcript: {}".format(result.alternatives[0].transcript))
        print("Confidence: {}".format(result.alternatives[0].confidence))

    print("Full transcript: ", full_transcript)
    return full_transcript


def transcribe_file(file, file_name):
    # Write file

    dst_name = generate_name(file_name)
    upload_blob(STORAGE_BUCKET, file_name, dst_name)

    # Delete file

    uri = get_gsc_uri(dst_name)
    transcript = transcribe_gcs(uri)
    return transcript

