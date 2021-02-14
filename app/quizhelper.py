from google.cloud import speech

# [START speech_transcribe_async_gcs]
def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
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

        #print(u"Transcript: {}".format(result.alternatives[0].transcript))
        #print("Confidence: {}".format(result.alternatives[0].confidence))


    print(full_transcript)
# [END speech_transcribe_async_gcs]