#!/usr/bin/env python3
"""
Real-time Violation Detection Script
Run this to start detecting violations and automatically notifying drivers!
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.detection.realtime_pipeline import RealtimeViolationPipeline
import argparse


def main():
    """Main function to run real-time detection."""
    parser = argparse.ArgumentParser(
        description='Real-time Traffic Violation Detection System'
    )

    parser.add_argument(
        '--mode',
        type=str,
        choices=['webcam', 'video'],
        default='webcam',
        help='Detection mode: webcam (live camera) or video (file)'
    )

    parser.add_argument(
        '--video',
        type=str,
        help='Path to video file (required if mode=video)'
    )

    parser.add_argument(
        '--output',
        type=str,
        help='Path to save annotated video (optional)'
    )

    parser.add_argument(
        '--camera',
        type=int,
        default=0,
        help='Camera device ID (default: 0)'
    )

    parser.add_argument(
        '--location',
        type=str,
        default='Main Junction',
        help='Camera location description'
    )

    parser.add_argument(
        '--camera-id',
        type=str,
        default='CAM-001',
        help='Camera identifier'
    )

    parser.add_argument(
        '--violation-type',
        type=str,
        default='illegal_parking',
        choices=[
            'illegal_parking',
            'no_parking_zone',
            'blocking_traffic',
            'bus_lane',
            'pedestrian_crossing',
            'double_parking'
        ],
        help='Type of violation to detect'
    )

    parser.add_argument(
        '--confidence',
        type=float,
        default=0.25,
        help='Detection confidence threshold (0.0-1.0)'
    )

    parser.add_argument(
        '--sample-rate',
        type=int,
        default=30,
        help='Process every Nth frame (for video mode)'
    )

    args = parser.parse_args()

    # Validate arguments
    if args.mode == 'video' and not args.video:
        print("❌ Error: --video is required when mode=video")
        return

    print("="*70)
    print("🚦 INTELLIGENT TRAFFIC MANAGEMENT SYSTEM")
    print("   Real-time Violation Detection & Driver Notification")
    print("="*70)
    print()

    # Initialize pipeline
    print(f"📍 Location: {args.location}")
    print(f"📹 Camera ID: {args.camera_id}")
    print(f"⚠️  Violation Type: {args.violation_type}")
    print(f"🎯 Confidence: {args.confidence * 100}%")
    print()

    pipeline = RealtimeViolationPipeline(
        conf_threshold=args.confidence,
        location=args.location,
        camera_id=args.camera_id
    )

    # Run detection
    try:
        if args.mode == 'webcam':
            print("🎥 Starting LIVE webcam detection...")
            print("   • Violations will be detected in real-time")
            print("   • License plates will be recognized")
            print("   • Drivers will be notified automatically")
            print("   • Press 'q' to quit, 's' to save frame, 'r' to reset stats")
            print()

            pipeline.process_webcam(
                camera_id=args.camera,
                violation_type=args.violation_type
            )

        else:  # video mode
            print(f"🎥 Processing video: {args.video}")
            print(f"   • Sample rate: 1/{args.sample_rate} frames")
            if args.output:
                print(f"   • Saving to: {args.output}")
            print()

            stats = pipeline.process_video(
                video_path=args.video,
                output_path=args.output,
                violation_type=args.violation_type,
                sample_rate=args.sample_rate
            )

            print("\n✅ Processing complete!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Detection stopped by user")
        pipeline._print_statistics()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
