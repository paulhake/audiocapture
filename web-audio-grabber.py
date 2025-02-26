import os
import argparse
import yt_dlp
import subprocess
import tempfile

def extract_audio(url, output_file=None, audio_format="mp3", audio_quality="192"):
    """
    Extract audio from a web video stream
    
    Args:
        url (str): URL of the web video
        output_file (str, optional): Path to save the audio file. If None, uses the video title.
        audio_format (str, optional): Audio format (mp3, m4a, wav, etc.)
        audio_quality (str, optional): Audio quality in kbps
        
    Returns:
        str: Path to the saved audio file
    """
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    # Configure yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'quiet': False,
        'no_warnings': False,
    }
    
    # Download the video/audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info)
    
    # Determine output filename
    if not output_file:
        output_file = f"{info['title']}.{audio_format}"
    
    # Make sure the output filename has the correct extension
    if not output_file.endswith(f'.{audio_format}'):
        output_file = f"{output_file}.{audio_format}"
    
    # Convert to desired audio format using ffmpeg
    subprocess.run([
        'ffmpeg',
        '-i', downloaded_file,
        '-vn',  # No video
        '-ar', '44100',  # Audio sampling rate
        '-ac', '2',  # Stereo
        '-b:a', f'{audio_quality}k',  # Bitrate
        '-f', audio_format,  # Format
        output_file
    ], check=True)
    
    # Clean up temporary files
    os.remove(downloaded_file)
    os.rmdir(temp_dir)
    
    print(f"Audio successfully extracted to: {output_file}")
    return output_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract audio from web video streams")
    parser.add_argument("url", help="URL of the web video")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-f", "--format", default="mp3", help="Audio format (mp3, m4a, wav, etc.)")
    parser.add_argument("-q", "--quality", default="192", help="Audio quality in kbps")
    
    args = parser.parse_args()
    extract_audio(args.url, args.output, args.format, args.quality)
