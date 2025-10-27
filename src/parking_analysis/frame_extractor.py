"""
Frame Extraction Script for Traffic Video Dataset
Extracts frames from video files at specified intervals
"""

import cv2
import os
from pathlib import Path
from tqdm import tqdm
import argparse


class FrameExtractor:
    def __init__(self, video_path, output_dir, frame_interval=30):
        """
        Initialize Frame Extractor
        
        Args:
            video_path: Path to video file
            output_dir: Directory to save extracted frames
            frame_interval: Extract 1 frame every N frames (default: 30 = 1 frame/sec at 30fps)
        """
        self.video_path = Path(video_path)
        self.output_dir = Path(output_dir)
        self.frame_interval = frame_interval
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_frames(self):
        """Extract frames from video"""
        
        # Open video file
        cap = cv2.VideoCapture(str(self.video_path))
        
        if not cap.isOpened():
            print(f"❌ Error: Could not open video file: {self.video_path}")
            return 0
        
        # Get video properties
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        duration = total_frames / fps if fps > 0 else 0
        
        print(f"\n📹 Video Info:")
        print(f"   File: {self.video_path.name}")
        print(f"   Total Frames: {total_frames}")
        print(f"   FPS: {fps}")
        print(f"   Duration: {duration:.2f} seconds ({duration/60:.2f} minutes)")
        print(f"   Will extract: ~{total_frames // self.frame_interval} frames")
        
        frame_count = 0
        saved_count = 0
        
        # Progress bar
        with tqdm(total=total_frames, desc="Extracting frames") as pbar:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Save frame at specified intervals
                if frame_count % self.frame_interval == 0:
                    # Create filename: video-name_frame-000001.jpg
                    frame_filename = f"{self.video_path.stem}_frame_{saved_count:06d}.jpg"
                    frame_path = self.output_dir / frame_filename
                    
                    # Save frame
                    cv2.imwrite(str(frame_path), frame)
                    saved_count += 1
                
                frame_count += 1
                pbar.update(1)
        
        cap.release()
        
        print(f"\n✅ Extraction complete!")
        print(f"   Saved {saved_count} frames to: {self.output_dir}")
        print(f"   Average: 1 frame every {self.frame_interval/fps:.2f} seconds")
        
        return saved_count


def extract_from_directory(video_dir, output_base_dir, frame_interval=30, video_extensions=['.mp4', '.avi', '.mov', '.MP4', '.MOV', '.AVI', '.mkv', '.MKV']):
    """
    Extract frames from all videos in a directory
    
    Args:
        video_dir: Directory containing video files
        output_base_dir: Base directory for extracted frames
        frame_interval: Extract 1 frame every N frames
        video_extensions: List of video file extensions to process
    """
    video_dir = Path(video_dir)
    output_base_dir = Path(output_base_dir)
    
    # Find all video files
    video_files = []
    for ext in video_extensions:
        video_files.extend(video_dir.glob(f"**/*{ext}"))
    
    if not video_files:
        print(f"❌ No video files found in: {video_dir}")
        return
    
    print(f"\n🎬 Found {len(video_files)} video files")
    print("=" * 60)
    
    total_frames_extracted = 0
    
    for i, video_path in enumerate(video_files, 1):
        print(f"\n[{i}/{len(video_files)}] Processing: {video_path.name}")
        
        # Create output directory for this video
        output_dir = output_base_dir / video_path.stem
        
        # Extract frames
        extractor = FrameExtractor(video_path, output_dir, frame_interval)
        frames_saved = extractor.extract_frames()
        total_frames_extracted += frames_saved
        
        print("-" * 60)
    
    print(f"\n🎉 ALL DONE!")
    print(f"   Processed {len(video_files)} videos")
    print(f"   Extracted {total_frames_extracted} total frames")
    print(f"   Saved to: {output_base_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract frames from traffic videos")
    parser.add_argument("--video", type=str, help="Path to single video file")
    parser.add_argument("--video-dir", type=str, help="Path to directory containing videos")
    parser.add_argument("--output", type=str, required=True, help="Output directory for frames")
    parser.add_argument("--interval", type=int, default=30, 
                       help="Extract 1 frame every N frames (default: 30)")
    
    args = parser.parse_args()
    
    if args.video:
        # Extract from single video
        extractor = FrameExtractor(args.video, args.output, args.interval)
        extractor.extract_frames()
    
    elif args.video_dir:
        # Extract from all videos in directory
        extract_from_directory(args.video_dir, args.output, args.interval)
    
    else:
        print("❌ Error: Please provide either --video or --video-dir")
        parser.print_help()