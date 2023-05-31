#coding=utf8
#import argparse

import grpc
import yaml, json

import yandex.cloud.ai.stt.v2.stt_service_pb2 as stt_service_pb2
import yandex.cloud.ai.stt.v2.stt_service_pb2_grpc as stt_service_pb2_grpc

CHUNK_SIZE = 3333

def gen(folder_id, audio_file_name):
    # Specify recognition settings.
    specification = stt_service_pb2.RecognitionSpec(
        language_code='auto',
        profanity_filter=True,
        model='general',
        partial_results=True,
        #audio_format='container_audio', # added
        #container_audio_type='OGG_OPUS', # added
        audio_encoding='OGG_OPUS',
        #audio_encoding='LINEAR16_PCM',
        sample_rate_hertz=8000
    )
    streaming_config = stt_service_pb2.RecognitionConfig(specification=specification, folder_id=folder_id)

    # Send the message with the recognition settings.
    yield stt_service_pb2.StreamingRecognitionRequest(config=streaming_config)

    # Read the audio file and send its contents in chunks.
    with open(audio_file_name, 'rb') as f:
        data = f.read(CHUNK_SIZE)
        while data != b'':
            yield stt_service_pb2.StreamingRecognitionRequest(audio_content=data)
            data = f.read(CHUNK_SIZE)

#def run(folder_id, iam_token, audio_file_name):
def transcribe_file(audio_file_name):
    # Establish a connection with the server.
    cred = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel('stt.api.cloud.yandex.net:443', cred)
    stub = stt_service_pb2_grpc.SttServiceStub(channel)

    with open('/home/pavel/cfg/elis-yandex-api-key.yaml', 'r') as f:
        data = yaml.safe_load(f)
        f.close()

    with open('/home/pavel/cfg/yandex_config.json', 'r') as f:
        config = json.load(f)
        folder_id = config['yandex_service_catalog_id']
        f.close()

    # Send data for recognition.
    #it = stub.StreamingRecognize(gen(folder_id, audio_file_name), metadata=(('authorization', 'Bearer %s' % iam_token),))
    it = stub.StreamingRecognize(gen(folder_id, audio_file_name), metadata=(('authorization', 'Api-Key %s' % data['secret']),))

    # Process server responses and output the result to the console.
    try:
        for r in it:
            try:
                #print('Start chunk: ')
                for alternative in r.chunks[0].alternatives:
                    #print('alternative: ', alternative.text)
                #print('Is final: ', r.chunks[0].final)
                #print('')
                    if r.chunks[0].final : 
                        #print('confidence: ', alternative.confidence)
                        #print('words: ', len(alternative.words))
                        return alternative
            except LookupError:
                # print('Not available chunks')
                return 'Not available chunks'
    except grpc._channel._Rendezvous as err:
        print('Error code %s, message: %s' % (err._state.code, err._state.details))

if __name__ == '__main__':
    
    file_name = '/home/pavel/github/AudioTelega/voices/333.ogg'
    print('Run answer: ', transcribe_file(file_name))
    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', required=True, help='IAM token')
    parser.add_argument('--folder_id', required=True, help='folder ID')
    parser.add_argument('--path', required=True, help='audio file path')
    args = parser.parse_args()
    
    run(args.folder_id, args.token, args.path)
    run(args.folder_id, args.path)
    """