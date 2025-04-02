from pydub import AudioSegment, silence
import os
import shutil


# ---------------- CONFIGURABLE PARAMETERS ----------------

MIN_SILENCE_LEN = 1000
SILENCE_THRESH = -60
KEEP_SILENCE = 800
SEEK_STEP = 2
MIN_CHUNK_LENGTH = 180


def load_audio(file_path):
    """Load an audio file and return an AudioSegment object."""
    audio = AudioSegment.from_file(file_path)
    duration_sec = len(audio) * 1e-3
    print(f"Loaded audio: {file_path} ({duration_sec:.2f} sec)")
    return audio, duration_sec


def split_audio_on_silence(audio):
    """Split the audio into chunks based on silence detection."""
    chunks = silence.split_on_silence(
        audio,
        min_silence_len=MIN_SILENCE_LEN,
        silence_thresh=SILENCE_THRESH,
        keep_silence=KEEP_SILENCE,
        seek_step=SEEK_STEP,
    )
    print(f"Total chunks detected: {len(chunks)}")
    return chunks


def clean_output_directory(output_dir):
    """Delete existing output directory and recreate it."""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    print(f"Created output directory: {output_dir}")


def process_chunks(chunks, min_chunk_size):
    """Combine smaller chunks into larger chunks of at least min_chunk_size seconds."""
    sec_in_chunk, combined_chunk, final_chunks = 0, AudioSegment.empty(), []

    for chunk in chunks:

        # sec_in_chunk hold the chunk_duration in secs whereas combined_chunk hold chunk in ms of type pydub
        if sec_in_chunk < min_chunk_size:
            sec_in_chunk += len(chunk) / 1000
            combined_chunk += chunk

        else:
            final_chunks.append(combined_chunk)
            sec_in_chunk = 0
            combined_chunk = AudioSegment.empty()

    # Append the last chunk if not empty
    if len(combined_chunk) > 0:
        final_chunks.append(combined_chunk)

    print(f"Final number of processed chunks: {len(final_chunks)}")
    return final_chunks


def save_chunks(chunks, output_dir):
    """Save processed audio chunks to the specified output directory."""
    combined_audio = AudioSegment.empty()

    for i, chunk in enumerate(chunks):
        chunk_path = os.path.join(output_dir, f"{i+1}.wav")
        chunk.export(chunk_path, format="wav")
        combined_audio += chunk
        print(f"Saved chunk {i+1} ({len(chunk) / 1000:.2f} sec)")

    combined_audio.export("combined_audio.wav", format="wav")
    print("Combined audio file saved as 'combined_audio.wav'.")


# ---------------- MAIN EXECUTION ----------------
if __name__ == "__main__":
    FILE_PATH = "/home/muhammad-faizan/Downloads/12101.wav"
    OUTPUT_DIR = "chunks"

    # Load audio file
    clip, clip_duration_sec = load_audio(FILE_PATH)

    # Split audio into chunks
    chunks = split_audio_on_silence(clip)

    # Prepare output directory
    clean_output_directory(OUTPUT_DIR)

    # Process and merge small chunks
    final_chunks = process_chunks(chunks, MIN_CHUNK_LENGTH)

    # Save the processed chunks
    save_chunks(final_chunks, OUTPUT_DIR)


from pydub import AudioSegment, silence
import os
import shutil


# ---------------- CONFIGURABLE PARAMETERS ----------------

MIN_SILENCE_LEN = 1000
SILENCE_THRESH = -60
KEEP_SILENCE = 800
SEEK_STEP = 2
MAX_CHUNK_LENGTH = 180


def load_audio(file_path):
    """Load an audio file and return an AudioSegment object."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: File '{file_path}' not found.")

    try:
        audio = AudioSegment.from_file(file_path)
        duration_sec = len(audio) * 1e-3
        print(f"Loaded audio: {file_path} ({duration_sec:.2f} sec)")
        return audio, duration_sec

    except Exception as e:
        print(f"Error loading audio file: {e}")
        return None, 0


def split_audio_on_silence(audio):
    """Split the audio into chunks based on silence detection."""
    if audio is None:
        raise ValueError("Error: Audio file is not loaded properly.")
    try:
        chunks = silence.split_on_silence(
            audio,
            min_silence_len=MIN_SILENCE_LEN,
            silence_thresh=SILENCE_THRESH,
            keep_silence=KEEP_SILENCE,
            seek_step=SEEK_STEP,
        )
        if not chunks:
            raise ValueError(
                "Error: No valid chunks detected. Check silence threshold settings."
            )
        print(f"Total chunks detected: {len(chunks)}")

    except Exception as e:
        print(f"Error during silence splitting: {e}")
        return []
    return chunks


def clean_output_directory(output_dir):
    """Delete existing output directory and recreate it."""
    try:
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    except Exception as e:
        print(f"Error creating output directory: {e}")


def process_chunks(chunks, min_chunk_size):
    """Combine smaller chunks into larger chunks of at least min_chunk_size seconds."""
    try:
        if not chunks:
            raise ValueError("Error: No chunks available for processing.")
        sec_in_chunk, combined_chunk, final_chunks = 0, AudioSegment.empty(), []

        for chunk in chunks:

            # sec_in_chunk hold the chunk_duration in secs whereas combined_chunk hold chunk in ms of type pydub
            if sec_in_chunk < min_chunk_size:
                sec_in_chunk += len(chunk) / 1000
                combined_chunk += chunk

            else:
                final_chunks.append(combined_chunk)
                sec_in_chunk = 0
                combined_chunk = AudioSegment.empty()

        # Append the last chunk if not empty
        if len(combined_chunk) > 0:
            final_chunks.append(combined_chunk)

        print(f"Final number of processed chunks: {len(final_chunks)}")
        return final_chunks
    except Exception as e:
        print(f"Error processing chunks: {e}")
        return []


def save_chunks(chunks, output_dir):
    """Save processed audio chunks to the specified output directory."""
    try:
        if not chunks:
            raise ValueError("Error: No chunks to save.")

        combined_audio = AudioSegment.empty()
        for i, chunk in enumerate(chunks):
            chunk_path = os.path.join(output_dir, f"{i+1}.wav")
            chunk.export(chunk_path, format="wav")
            combined_audio += chunk
            print(f"Saved chunk {i+1} ({len(chunk) / 1000:.2f} sec)")

        combined_audio.export("combined_audio.wav", format="wav")
        print("Combined audio file saved as 'combined_audio.wav'.")

    except Exception as e:
        print(f"Error in Saving chunks: {e}")


# ---------------- MAIN EXECUTION ----------------
if __name__ == "__main__":
    FILE_PATH = "audio.mp3"
    OUTPUT_DIR = "chunks"

    # Load audio file
    clip, clip_duration_sec = load_audio(FILE_PATH)

    # Split audio into chunks
    chunks = split_audio_on_silence(clip)

    # Prepare output directory
    clean_output_directory(OUTPUT_DIR)

    # Process and merge small chunks
    final_chunks = process_chunks(chunks, MAX_CHUNK_LENGTH, OUTPUT_DIR)

    # Save the processed chunks
    save_chunks(final_chunks, OUTPUT_DIR)
