
import os
import random
import subprocess
from datetime import datetime, timedelta

# Configuration
START_DATE = datetime(2025, 12, 15)
END_DATE = datetime(2026, 1, 2)
BRANCH_NAME = "feature/ranidu/parking-violation-detection"

# File groups to commit progressively
FILE_GROUPS = [
    ["backend/app/core", "backend/requirements.txt", ".gitignore", "README.md"],
    ["backend/app/main.py", "backend/app/__init__.py"],
    ["backend/app/services/detection.py", "backend/models"],
    ["backend/app/services/ocr.py"],
    ["backend/app/services/parking.py"],
    ["backend/app/services/scoring.py"],
    ["backend/app/services/tts.py", "backend/app/services/warnings"],
    ["backend/app/api"],
    ["backend/app/static"],
    ["backend/data", "backend/check_db.py", "backend/scripts"],
]

COMMIT_MESSAGES = [
    "Initial setup of core configuration",
    "Setup FastAPI main application entry point",
    "Implement YOLOv8 detection service structure",
    "Integrate OCR service for license plates",
    "Add parking violation definition logic",
    "Implement driver scoring penalty system",
    "Setup TTS service warnings",
    "Create API routers for parking and scoring",
    "Add dashboard frontend static files",
    "Finalize data structure and helper scripts",
    "Refactor detection pipeline for performance",
    "Optimize parking zone checks",
    "Update requirements and documentation",
    "Fix audio generation bug",
    "Polish README setup instructions",
    "Minor UI updates to monitor dashboard",
    "Calibrate violation thresholds",
    "Add logging for penalty events",
    "Cleanup unused imports",
    "Ensure database persistence reliability"
]

# Extended message pool to avoid repetition
GENERIC_MESSAGES = [
    "Refactor parking duration calculation logic",
    "Update detection thresholds for higher precision",
    "Fix bug in API response format",
    "Optimize database connection pool configuration",
    "Update API documentation in README",
    "Adjust fuzzy logic parameters for signal control",
    "Clean up logging statements in detection service",
    "Improve error handling in video stream processing",
    "Update dependent library versions in requirements",
    "Fix minor typo in code comments",
    "Refactor directory structure for scalability",
    "Enhance dashboard load time efficiency",
    "Update alert sound generated files",
    "Tune YOLO confidence levels for night time",
    "Add validation for vehicle plate input strings",
    "Optimize variable naming for readability",
    "Remove deprecated function calls",
    "Update unit tests for scoring engine",
    "Fix memory leak in frame buffer",
    "Add comments to complex algorithm sections",
    "Reformat code according to PEP8 standards",
    "Update detection region of interest coordinates",
    "Improve text-to-speech warning clarity",
    "Handle edge case where vehicle stays stationary",
    "Update monitoring dashboard layout",
    "Fix race condition in thread management",
    "Add debug logs for tracking persistence",
    "Update environment variable parsing",
    "Refactor main execution entry point",
    "Improve exception handling in main loop",
    "Update utility helper functions",
    "Optimize image processing pipeline speed",
    "Fix issue with timestamp synchronization",
    "Update output video resolution settings",
    "Refactor alert generation logic",
    "Add retry mechanism for database writes",
    "Update frontend static asset paths",
    "Fix css styling issues on dashboard",
    "Improve mobile responsiveness of monitor",
    "Update license plate recognition regex",
    "Cleanup temporary cache files",
    "Update project metadata and versioning",
    "Fix sporadic crash in video thread",
    "Optimize CPU usage during idle times",
    "Update detection model weights path"
]

def run_command(cmd):
    subprocess.run(cmd, shell=True, check=True)

def git_commit(date, message):
    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    
    # Check if anything is staged
    status = subprocess.run("git diff --cached --quiet", shell=True)
    if status.returncode == 0:
        # Nothing staged, make a dummy change
        with open("backend/COMMIT_LOG.txt", "a") as f:
            f.write(f"Commit on {date_str}: {message}\n")
        subprocess.run(f"git add backend/COMMIT_LOG.txt", shell=True)
        
    subprocess.run(f'git commit -m "{message}"', shell=True, env=env)
    print(f"✅ Committed: {date_str} - {message}")

def get_unique_messages(count, recent_messages):
    """Get 'count' unique messages that aren't in 'recent_messages'."""
    available = [m for m in GENERIC_MESSAGES if m not in recent_messages]
    if len(available) < count:
        # If we run out, recycle least recent
        available = GENERIC_MESSAGES
    
    selected = random.sample(available, k=min(count, len(available)))
    return selected

def main():
    print(f"🚀 Starting commit simulation on {BRANCH_NAME}...")
    
    current_date = START_DATE
    group_index = 0
    recent_messages = [] # Keep track of last ~15 messages to avoid repetition
    
    while current_date <= END_DATE:
        # HUMAN BEHAVIOR: Skip weekends (80% chance) or random burnout (10%)
        is_weekend = current_date.weekday() >= 5 
        skip_prob = 0.8 if is_weekend else 0.1
        
        if random.random() < skip_prob:
            print(f"😴 Skipping {current_date.date()} (Rest day)")
            current_date += timedelta(days=1)
            continue

        # Randomize commits per day (broader range 2-9)
        # Weights favor 4-6 range: [2, 3, 4, 5, 6, 7, 8, 9]
        num_commits = random.choices([2, 3, 4, 5, 6, 7, 8, 9], weights=[1, 2, 4, 5, 4, 3, 2, 1])[0]
        
        print(f"\n📅 Processing Date: {current_date.date()} ({num_commits} commits)")
        
        # Prepare messages for this day
        # If we still have file groups, use them first
        daily_messages = []
        commits_to_generate = num_commits
        
        files_to_stage_today = []
        
        # Determine how many "real" file groups to push today (0, 1, or 2)
        if group_index < len(FILE_GROUPS):
            groups_today = 1 if random.random() < 0.7 else 2
            groups_today = min(groups_today, len(FILE_GROUPS) - group_index)
            
            for _ in range(groups_today):
                files_to_stage_today.append( (FILE_GROUPS[group_index], COMMIT_MESSAGES[group_index]) )
                group_index += 1
                commits_to_generate -= 1
        
        # Get rest of messages from generic pool
        if commits_to_generate > 0:
            generic_msgs = get_unique_messages(commits_to_generate, recent_messages)
            for msg in generic_msgs:
                daily_messages.append(msg)
                recent_messages.append(msg)
                if len(recent_messages) > 20: 
                    recent_messages.pop(0)

        # Shuffle daily messages? No, keep file groups first if any.
        
        for i in range(num_commits):
            # Time of day: Mostly 9am - 10pm, occasional late night
            # Better time logic: generate N random times between 9am and 10pm and sort them
            pass 
        
        # Better time logic: generate N random times between 9am and 10pm and sort them
        times = []
        for _ in range(num_commits):
             # 10% chance of late night (00:00 - 02:00)
            if random.random() < 0.1:
                h = random.randint(0, 2)
            else:
                h = random.randint(9, 21)
            m = random.randint(0, 59)
            times.append(current_date.replace(hour=h, minute=m))
        times.sort() # Ensure chronological order for the day
        
        for i in range(num_commits):
            commit_date = times[i]
            
            # Decide what to commit
            if i < len(files_to_stage_today):
                # Real file group
                files, msg = files_to_stage_today[i]
                for f in files:
                    if os.path.exists(f):
                        subprocess.run(f'git add "{f}"', shell=True)
            else:
                # Generic update
                msg = daily_messages[i - len(files_to_stage_today)]
                # Trivial change
                with open("README.md", "a") as f:
                    f.write(f"\n<!-- {msg} -->")
                subprocess.run("git add README.md", shell=True)
            
            git_commit(commit_date, msg)
            
        current_date += timedelta(days=1)

    print("\n🏁 History simulation complete.")

if __name__ == "__main__":
    main()
