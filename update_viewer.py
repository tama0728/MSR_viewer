import os
import json
import re

SCENES_DIR = 'scenes'
ROOT_INDEX = 'index.html'

def get_image_files(directory):
    valid_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp'}
    images = []
    if not os.path.exists(directory):
        return images
    for f in os.listdir(directory):
        if os.path.splitext(f)[1].lower() in valid_extensions:
            images.append(f)
    return images

def update_scene_data(scene_name):
    scene_path = os.path.join(SCENES_DIR, scene_name)
    categories = [d for d in os.listdir(scene_path) if os.path.isdir(os.path.join(scene_path, d))]
    # Custom sort order
    priority = ['LR', 'HR', 'CLASSICAL', 'REAL', 'PFT-SR', 'PFT', 'adcSR', 'ADC', 'FINAL', 'Final', 'OUR1', 'OUR2']
    
    def sort_key(name):
        if name in priority:
            return (0, priority.index(name))
        return (1, name)
        
    categories.sort(key=sort_key)

    # Collect all unique image basenames across all categories
    image_map = {} # basename -> {category: filename}
    
    for cat in categories:
        cat_path = os.path.join(scene_path, cat)
        images = get_image_files(cat_path)
        for img in images:
            basename = os.path.splitext(img)[0] # e.g. "38082" from "38082.png"
            if basename not in image_map:
                image_map[basename] = {}
            image_map[basename][cat] = img

    # Construct data object
    image_boxes = []
    sorted_basenames = sorted(image_map.keys())
    
    for basename in sorted_basenames:
        elements = []
        # We want to ensure a specific order if possible, or just alphabetical
        # The original data.js had HR, LR, CLASSICAL, REAL, OUR1, OUR2
        # We'll just use the sorted categories
        
        for cat in categories:
            if cat in image_map[basename]:
                elements.append({
                    "title": cat,
                    "version": "-",
                    "image": f"{cat}/{image_map[basename][cat]}"
                })
        
        if elements:
            image_boxes.append({
                "title": basename,
                "elements": elements
            })

    data_content = f"const data = \n{json.dumps({'imageBoxes': image_boxes}, indent=4)}\n"
    
    with open(os.path.join(scene_path, 'data.js'), 'w') as f:
        f.write(data_content)
    
    print(f"Updated {scene_name}/data.js with {len(image_boxes)} images.")
    
    # Return a representative image for the scene (first image of first category)
    if image_boxes and image_boxes[0]['elements']:
        first_element = image_boxes[0]['elements'][0]
        return first_element['image']
    return None

def update_root_index(scenes_data):
    with open(ROOT_INDEX, 'r') as f:
        lines = f.readlines()

    start_index = -1
    end_index = -1
    
    for i, line in enumerate(lines):
        if '<div class="element-container">' in line:
            start_index = i
        if start_index != -1 and 'The interactive viewer template' in line:
            # The closing div should be a few lines before this
            # We'll look backwards from here to find the closing div of the container
            for j in range(i - 1, start_index, -1):
                if '</div>' in lines[j]:
                    end_index = j
                    break
            break
            
    if start_index == -1 or end_index == -1:
        print("Could not find element-container in index.html")
        return

    # Generate HTML for scenes
    new_lines = [lines[start_index]]
    
    for scene_name, thumb_path in scenes_data.items():
        if not thumb_path:
            continue
            
        # Fix path separators for HTML
        thumb_path = thumb_path.replace(os.sep, '/')
        scene_link = f"scenes/{scene_name}/index.html"
        thumb_full_path = f"scenes/{scene_name}/{thumb_path}"
        
        new_lines.append(f'                <div class="report-preview">\n')
        new_lines.append(f'                    <a href="{scene_link}">\n')
        new_lines.append(f'                        <img class="report-thumb" src="{thumb_full_path}" height="256" width="auto" />\n')
        new_lines.append(f'                    </a>\n')
        new_lines.append(f'                    <br/>\n')
        new_lines.append(f'                    {scene_name}\n')
        new_lines.append(f'                </div>\n')

    new_lines.append(lines[end_index])
    
    # Reconstruct the file content
    final_lines = lines[:start_index] + new_lines + lines[end_index+1:]
    
    with open(ROOT_INDEX, 'w') as f:
        f.writelines(final_lines)
    print(f"Updated {ROOT_INDEX} with {len(scenes_data)} scenes.")

def main():
    if not os.path.exists(SCENES_DIR):
        print(f"Directory {SCENES_DIR} not found.")
        return

    scenes = [d for d in os.listdir(SCENES_DIR) if os.path.isdir(os.path.join(SCENES_DIR, d))]
    scenes.sort()
    
    scenes_data = {} # scene_name -> thumbnail_path
    
    for scene in scenes:
        thumb = update_scene_data(scene)
        scenes_data[scene] = thumb
        
    update_root_index(scenes_data)

if __name__ == "__main__":
    main()
