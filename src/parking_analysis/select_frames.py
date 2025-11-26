"""
Frame Selection Helper
Helps select diverse frames for annotation
"""

import os
import shutil
from pathlib import Path
import random

def select_frames_for_annotation(
    input_dir, 
    output_dir, 
    frames_per_video=None,
    total_target=1500
):
    """
    Select frames for annotation from extracted frames
    
    Args:
        input_dir: Directory containing extracted frames
        output_dir: Directory to copy selected frames
        frames_per_video: Number of frames per video (if None, auto-calculate)
        total_target: Target total frames to select
    """
    
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find all video folders
    video_folders = [f for f in input_path.iterdir() if f.is_dir()]
    
    print(f"📂 Found {len(video_folders)} video folders")
    
    if frames_per_video is None:
        # Auto-calculate frames per video
        frames_per_video = total_target // len(video_folders)
    
    print(f"🎯 Target: {frames_per_video} frames per video")
    print(f"📊 Total target: {frames_per_video * len(video_folders)} frames")
    print("=" * 60)
    
    total_selected = 0
    
    for video_folder in video_folders:
        # Get all frames from this video
        frames = list(video_folder.glob("*.jpg"))
        
        if len(frames) == 0:
            print(f"⚠️  No frames in {video_folder.name}")
            continue
        
        # Select frames evenly spaced
        if len(frames) <= frames_per_video:
            # Take all frames if we have fewer than target
            selected_frames = frames
        else:
            # Select evenly spaced frames
            step = len(frames) // frames_per_video
            selected_frames = frames[::step][:frames_per_video]
        
        # Copy selected frames
        for frame in selected_frames:
            # Create new filename with video name prefix
            new_name = f"{video_folder.name}_{frame.name}"
            dest = output_path / new_name
            shutil.copy2(frame, dest)
        
        total_selected += len(selected_frames)
        
        print(f"✅ {video_folder.name}")
        print(f"   Available: {len(frames)} frames")
        print(f"   Selected: {len(selected_frames)} frames")
        print("-" * 60)
    
    print(f"\n🎉 Selection complete!")
    print(f"   Total selected: {total_selected} frames")
    print(f"   Saved to: {output_path}")
    
    return total_selected


if __name__ == "__main__":
    # Pettah Market - Select 800 frames
    print("\n🏪 PETTAH MARKET SELECTION:")
    print("=" * 60)
    pettah_selected = select_frames_for_annotation(
        input_dir="data/extracted_frames/parking_violations/pettah_market",
        output_dir="data/annotation_ready/pettah_market",
        total_target=800
    )
    
    # Borella Junction - Select 400 frames
    print("\n\n🚦 BORELLA JUNCTION SELECTION:")
    print("=" * 60)
    borella_selected = select_frames_for_annotation(
        input_dir="data/extracted_frames/parking_violations/borella_junction",
        output_dir="data/annotation_ready/borella_junction",
        total_target=400
    )
    
    print("\n\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    print(f"Pettah Market: {pettah_selected} frames")
    print(f"Borella Junction: {borella_selected} frames")
    print(f"TOTAL: {pettah_selected + borella_selected} frames ready for annotation! 🎯")
    print("\nNext step: Upload to Roboflow and start annotating!")