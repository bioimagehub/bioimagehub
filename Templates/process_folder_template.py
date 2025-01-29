import os
import sys
import yaml # pip install pyyaml
from tqdm import tqdm  # conda install tqdm
from imaris_ims_file_reader import ims # pip install imaris-ims-file-reader==0.1.8
import napari # pip install napari
import numpy as np
# import cv2  # conda install conda-forge::opencv
from cellpose import models

DEFAULT_SETTINGS = {
    'main': {
        'folder_to_search': './images',
        'file_extension': '.jpg',
        'search_subfolders': True,
        're_analyse_images': False
    },
    'processed_files': [],
    'channel_info': ["protein 1", "protein 2", "protein 3", "nucleus"],
}

def load_settings(settings_path):
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as file:
            settings = yaml.safe_load(file)
    else:
        settings = DEFAULT_SETTINGS
        with open(settings_path, 'w') as file:
            yaml.safe_dump(settings, file)
    return settings

def save_settings(settings, settings_path):
    with open(settings_path, 'w') as file:
        yaml.safe_dump(settings, file)

def process_folder(settings):
    folder_to_search = settings['main']['folder_to_search']
    file_extension = settings['main']['file_extension']
    search_subfolders = settings['main']['search_subfolders']
    processed_files = []

    for root, dirs, files in os.walk(folder_to_search):
        for file in files:
            if file.endswith(file_extension):
                processed_files.append(os.path.join(root, file))
        if not search_subfolders:
            break

    settings['processed_files'] = processed_files
    return processed_files

def open_ims(file_path):
    file = ims(file_path)  # Initialize the ims_reader
    
    image_data = file[0, :, :, :, :] # [resolution, channel, z, y, x] # not sure about x and y order
    # Access image data; accessors may vary depending on your needs
    #image_data = file.data[0]  # Adjust this line to fit your data access pattern

    file.close()  # Manually close the file

    return image_data

def segment_nuclei(nucleus_3d):
    """
    Segment the nuclei in a 3D image stack using Cellpose.

    Parameters:
    - nucleus_3d: 3D numpy array representing the nucleus channel.
    
    Returns:
    - masks: 3D numpy array of segmented mask labels by Cellpose.
    """
    # Initialize Cellpose model for nucleus segmentation
    model = models.Cellpose(gpu=True, model_type='nuclei')  # Set gpu=True if you have a CUDA-compatible GPU
    
    # Cellpose evaluation to generate masks
    masks, flows, styles, diams = model.eval(nucleus_3d, diameter=None, channels=[0, 0], do_3D=True)
    
    return masks

def process_image(file_path, settings):
    print(f"Processing image: {file_path}")

    if file_path in settings['processed_files'] and not settings['main'].get('re_analyse_images', False):
        print("Already processed")
        return

    # Open image if ends with .ims
    if file_path.endswith('.ims'):
        img = open_ims(file_path)
        print("Opened .ims file")
    elif file_path.endswith('.tif'):
        print("Opening image file")
        # Example placeholder: replace with real loading method from an actual library
        img = np.random.random((4, 50, 512, 512))  # Random data as placeholder (channels, z, y, x)
    else:
        print("Unsupported file format")
        return

    print(f"Image shape: {img.shape}")

    # Segment nucleus from 3D stack
    nucleus_channel = settings['channel_info'].index('nucleus')
    nucleus_3d = img[nucleus_channel, :, :, :]

    # Call the_nuclei function
    masks = segment_nuclei(nucleus_3d)

    # Visualize using Napari
    with napari.gui_qt():
        viewer = napari.Viewer()
        viewer.add_image(img, name='original_image', channel_axis=0)
        viewer.add_image(nucleus_3d, name='nucleus_channel')
        viewer.add_labels(masks, name='cellpose_mask')

    return


def main():
    
    # Input
    settings_path = 'processing_settings.yaml'
    if len(sys.argv) > 1:
        settings_path = sys.argv[1]

    settings = load_settings(settings_path)
    print("Processing settings:")
    print(yaml.dump(settings, default_flow_style=False))

    # Processing folder
    files_to_process = process_folder(settings)
    save_settings(settings, settings_path) # TODO do this one file at a time after processing it

    # Processing images with progress bar
    for file_path in tqdm(files_to_process, desc="Processing images"):
        process_image(file_path, settings)

if __name__ == "__main__":
    main()