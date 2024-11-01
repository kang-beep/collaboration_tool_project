from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import speech_recognition as sr
from pydub import AudioSegment
import os

def speech_to_text(request):
    text = None
    error = None
    supported_formats = ['.m4a', '.wav', '.flac']

    if request.method == 'POST' and request.FILES['audio_file']:
        audio_file = request.FILES['audio_file']
        fs = FileSystemStorage()
        filename = fs.save(audio_file.name, audio_file)
        file_url = fs.url(filename)
        audio_path = fs.path(filename)

        # 파일 확장자 확인
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension not in supported_formats:
            error = "지원하는 확장자 파일이 아닙니다.\n.m4a / .wav / .flac 확장자 파일을 업로드 해주세요."
            error = error.replace('\n', '<br>')
            return render(request, 'stt.html', {'error': error})


        # 파일 형식을 WAV로 변환 및 샘플링 레이트 확인
        try:
            audio = AudioSegment.from_file(audio_path)
            audio = audio.set_frame_rate(16000).set_channels(1)  # 16kHz, mono로 변환
            wav_path = audio_path.rsplit('.', 1)[0] + '.wav'
            audio.export(wav_path, format='wav')
        except Exception as e:
            error = f'오디오 파일 변환 중 오류가 발생했습니다: {str(e)}'
            return render(request, 'stt.html', {'error': error})
        
        # 음성 파일을 텍스트로 변환
        recognizer = sr.Recognizer()
        try:
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language='ko-KR')
        except sr.UnknownValueError:
            text = "음성을 인식할 수 없습니다."
        except sr.RequestError as e:
            error = f"Google Web Speech API 서비스에 문제가 발생했습니다: {e}"
        except ValueError as e:
            error = f"오디오 파일을 처리할 수 없습니다: {e}"
        except Exception as e:
            error = f"예기치 않은 오류가 발생했습니다: {e}"

        return render(request, 'stt.html', {'file_url': file_url, 'text': text, 'error': error})
    
    return render(request, 'stt.html', {'text': text, 'error': error})
