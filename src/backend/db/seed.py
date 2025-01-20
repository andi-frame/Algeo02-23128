import os
import json
import zipfile
import shutil
import requests
from pathlib import Path
import hashlib


def make_safe_filename(filename, max_length=50):
    """Create a safe, shortened filename"""
    name, ext = os.path.splitext(filename)
    if len(name) > max_length:
        hash_obj = hashlib.md5(name.encode())
        name = hash_obj.hexdigest()[:max_length]
    return name + ext


def list_directory_contents(path, indent=0):
    """Print directory contents for debugging"""
    print(" " * indent + f"Listing contents of: {path}")
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                print(" " * (indent + 2) + f"DIR: {item}")
                list_directory_contents(item_path, indent + 4)
            else:
                print(" " * (indent + 2) + f"FILE: {item}")
    except Exception as e:
        print(" " * (indent + 2) + f"Error listing directory: {str(e)}")


def extract_zip_safely(zip_path, extract_path):
    """Extract a zip file safely, handling long filenames"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # List zip contents for debugging
        print(f"\nContents of {os.path.basename(zip_path)}:")
        for name in zip_ref.namelist():
            print(f"  {name}")
       
        for file_info in zip_ref.infolist():
            filename = file_info.filename
            if '/' in filename:
                parts = filename.split('/')
                parts[-1] = make_safe_filename(parts[-1])
                target_path = os.path.join(extract_path, *parts)
            else:
                target_path = os.path.join(extract_path, make_safe_filename(filename))


            parent_dir = os.path.dirname(target_path)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)


            if not filename.endswith('/'):
                try:
                    with zip_ref.open(file_info) as source, open(target_path, 'wb') as target:
                        shutil.copyfileobj(source, target)
                except Exception as e:
                    print(f"Error extracting {filename}: {str(e)}")


def find_midi_folders(base_path):
    """Find directories containing MIDI files"""
    midi_folders = []
    for root, dirs, files in os.walk(base_path):
        if any(f.endswith('.mid') for f in files):
            midi_folders.append(root)
    return midi_folders


def create_playlist_files(midi_zip_path, images_zip_path, output_path):
    """Create necessary files for each playlist from the zipped datasets"""
    midi_zip_path = get_absolute_path(midi_zip_path)
    images_zip_path = get_absolute_path(images_zip_path)
    output_path = get_absolute_path(output_path)
   
    print(f"Processing:\nMIDI zip: {midi_zip_path}\nImages zip: {images_zip_path}\nOutput path: {output_path}")
   
    temp_dir = get_absolute_path("./temp")
    midi_extract_path = os.path.join(temp_dir, "midi")
    images_extract_path = os.path.join(temp_dir, "images")
   
    try:
        os.makedirs(temp_dir, exist_ok=True)
        os.makedirs(midi_extract_path, exist_ok=True)
        os.makedirs(images_extract_path, exist_ok=True)
        os.makedirs(output_path, exist_ok=True)
       
        print("Extracting zip files...")
        extract_zip_safely(midi_zip_path, midi_extract_path)
        extract_zip_safely(images_zip_path, images_extract_path)
       
        print("\nExamining extracted directory structure:")
        list_directory_contents(temp_dir)
       
        # Find all folders containing MIDI files
        midi_folders = find_midi_folders(midi_extract_path)
        if not midi_folders:
            raise Exception(f"No folders containing MIDI files found in {midi_extract_path}")
        print(f"\nFound MIDI folders: {midi_folders}")
       
        # Find images folder
        image_folders = []
        for root, dirs, files in os.walk(images_extract_path):
            if any(f.lower().endswith(('.png', '.jpg', '.jpeg')) for f in files):
                image_folders.append(root)
       
        if not image_folders:
            raise Exception(f"No folders containing images found in {images_extract_path}")
        images_folder_path = image_folders[0]
        print(f"Using images from: {images_folder_path}")
       
        # Get all available images
        images = [f for f in os.listdir(images_folder_path)
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
       
        if not images:
            raise Exception(f"No images found in {images_folder_path}")
        print(f"Found {len(images)} images")
       
        # Track the index of the next image to use
        next_image_index = 0
       
        for folder_path in midi_folders:
            folder_name = os.path.basename(folder_path)
            midi_files = [f for f in os.listdir(folder_path) if f.endswith('.mid')]
           
            if not midi_files:
                print(f"Skipping empty folder: {folder_name}")
                continue
               
            print(f"\nProcessing playlist: {folder_name}")
            print(f"Found {len(midi_files)} MIDI files")
           
            playlist_temp_dir = os.path.join(output_path, make_safe_filename(folder_name))
            os.makedirs(playlist_temp_dir, exist_ok=True)
           
            # Select images for this folder
            selected_images = []
            for midi_file in midi_files:
                # Use the next image in the list
                selected_images.append(images[next_image_index])
                # Move to the next image, cycling back to the start if necessary
                next_image_index = (next_image_index + 1) % len(images)
           
            mapper_data = []
            for midi_file, image_file in zip(midi_files, selected_images):
                name = os.path.splitext(midi_file)[0].replace('_', ' ').title()
                mapper_data.append({
                    "audio_name": name,
                    "audio_file": make_safe_filename(midi_file),
                    "pic_name": image_file
                })
           
            mapper_path = os.path.join(playlist_temp_dir, 'mapper.json')
            with open(mapper_path, 'w') as f:
                json.dump(mapper_data, f, indent=4)
           
            images_zip_path = os.path.join(playlist_temp_dir, 'images.zip')
            with zipfile.ZipFile(images_zip_path, 'w') as zipf:
                for image in selected_images:
                    image_path = os.path.join(images_folder_path, image)
                    zipf.write(image_path, image)
           
            audios_zip_path = os.path.join(playlist_temp_dir, 'audios.zip')
            with zipfile.ZipFile(audios_zip_path, 'w') as zipf:
                for midi_file in midi_files:
                    midi_path = os.path.join(folder_path, midi_file)
                    safe_name = make_safe_filename(midi_file)
                    zipf.write(midi_path, safe_name)
           
            first_image_path = os.path.join(images_folder_path, selected_images[0])
            playlist_image_path = os.path.join(playlist_temp_dir, 'playlist_image.png')
            shutil.copy2(first_image_path, playlist_image_path)
         
    finally:
        # Cleanup temporary extraction directories
        print("\nCleaning up temporary files...")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


def upload_playlist(api_url, playlist_dir):
    """Upload a single playlist to the API"""
    playlist_name = os.path.basename(playlist_dir)
   
    files = {
        'playlistName': (None, playlist_name),
        'images': ('images.zip', open(os.path.join(playlist_dir, 'images.zip'), 'rb')),
        'playlistImage': ('playlist_image.png', open(os.path.join(playlist_dir, 'playlist_image.png'), 'rb')),
        'audios': ('audios.zip', open(os.path.join(playlist_dir, 'audios.zip'), 'rb')),
        'mapper': ('mapper.json', open(os.path.join(playlist_dir, 'mapper.json'), 'rb'))
    }
   
    try:
        response = requests.post(f"{api_url}/upload", files=files)
        response.raise_for_status()
        print(f"Successfully uploaded playlist: {playlist_name}")
        return True
    except Exception as e:
        print(f"Error uploading playlist {playlist_name}: {str(e)}")
        return False
    finally:
        for file_obj in files.values():
            if isinstance(file_obj, tuple) and hasattr(file_obj[1], 'close'):
                file_obj[1].close()


def get_absolute_path(relative_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(script_dir, relative_path))


def main():
    API_URL = "http://127.0.0.1:8000"
    MIDI_ZIP_PATH = "../../../test/dataset_midi_demo.zip"
    IMAGES_ZIP_PATH = "../../../test/dataset_image_demo.zip"
    OUTPUT_PATH = "./prepared_playlists"
   
    try:
        print("Preparing playlist files...")
        create_playlist_files(MIDI_ZIP_PATH, IMAGES_ZIP_PATH, OUTPUT_PATH)
       
        print("\nUploading playlists...")
        output_abs_path = get_absolute_path(OUTPUT_PATH)
        playlist_dirs = [os.path.join(output_abs_path, d) for d in os.listdir(output_abs_path)]
       
        for playlist_dir in playlist_dirs:
            if os.path.isdir(playlist_dir):
                upload_playlist(API_URL, playlist_dir)
       
        print("\nProcess completed!")
       
    except Exception as e:
        print(f"Error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
