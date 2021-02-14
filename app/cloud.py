from google.cloud import storage, speech
from app.utils import generate_name
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
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=16000,
        language_code="en-US",
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

        #print("Transcript: {}".format(result.alternatives[0].transcript))
        #print("Confidence: {}".format(result.alternatives[0].confidence))


    print(full_transcript)
# [END speech_transcribe_async_gcs]


test_file = 'test-lec.mp3'

test_file_gcs_uri = generate_name(test_file)

upload_blob(STORAGE_BUCKET, test_file, test_file_gcs_uri)
transcribe_gcs(test_file_gcs_uri, STORAGE_BUCKET)
