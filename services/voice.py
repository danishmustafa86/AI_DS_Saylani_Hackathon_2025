import base64
import io
import tempfile
import os
from typing import Optional, Dict, Any
from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
import speech_recognition as sr
from settings import get_settings


class VoiceService:
    """Service for handling voice-to-text and text-to-speech using ElevenLabs"""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = None
        self.recognizer = sr.Recognizer()
        
    def _get_elevenlabs_client(self) -> Optional[ElevenLabs]:
        """Get or create ElevenLabs client"""
        if self.client is None and self.settings.elevenlabs_api_key:
            try:
                self.client = ElevenLabs(api_key=self.settings.elevenlabs_api_key)
            except Exception as e:
                print(f"Error initializing ElevenLabs client: {e}")
                return None
        return self.client
    
    def speech_to_text(self, audio_base64: str) -> Dict[str, Any]:
        """Convert speech to text using speech_recognition library"""
        try:
            # Decode base64 audio data
            audio_data = base64.b64decode(audio_base64)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            try:
                # Use speech recognition to convert audio to text
                with sr.AudioFile(temp_file_path) as source:
                    audio = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio)
                    
                return {
                    "success": True,
                    "text": text,
                    "message": "Speech successfully converted to text"
                }
                    
            except sr.UnknownValueError:
                return {
                    "success": False,
                    "text": "",
                    "error": "Could not understand the audio"
                }
            except sr.RequestError as e:
                return {
                    "success": False,
                    "text": "",
                    "error": f"Speech recognition service error: {e}"
                }
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.unlink(temp_file_path)
                    
        except Exception as e:
            return {
                "success": False,
                "text": "",
                "error": f"Error processing audio: {str(e)}"
            }
    
    def text_to_speech(self, text: str, voice_id: str = "JBFqnCBsd6RMkjVDRZzb") -> Dict[str, Any]:
        """Convert text to speech using ElevenLabs"""
        try:
            client = self._get_elevenlabs_client()
            if not client:
                return {
                    "success": False,
                    "audio_base64": "",
                    "error": "ElevenLabs client not available. Check API key."
                }
            
            # Generate speech
            audio = client.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            
            # Convert audio to base64
            audio_bytes = b"".join(audio)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            return {
                "success": True,
                "audio_base64": audio_base64,
                "voice_id": voice_id,
                "message": "Text successfully converted to speech"
            }
            
        except Exception as e:
            return {
                "success": False,
                "audio_base64": "",
                "error": f"Error generating speech: {str(e)}"
            }
    
    def get_available_voices(self) -> Dict[str, Any]:
        """Get list of available voices from ElevenLabs"""
        try:
            client = self._get_elevenlabs_client()
            if not client:
                return {
                    "success": False,
                    "voices": [],
                    "error": "ElevenLabs client not available. Check API key."
                }
            
            voices = client.voices.get_all()
            voice_list = []
            
            for voice in voices.voices:
                voice_list.append({
                    "voice_id": voice.voice_id,
                    "name": voice.name,
                    "category": voice.category,
                    "description": getattr(voice, 'description', ''),
                })
            
            return {
                "success": True,
                "voices": voice_list,
                "count": len(voice_list)
            }
            
        except Exception as e:
            return {
                "success": False,
                "voices": [],
                "error": f"Error fetching voices: {str(e)}"
            }


# Global voice service instance
voice_service = VoiceService()


def get_voice_service() -> VoiceService:
    """Get the voice service instance"""
    return voice_service
