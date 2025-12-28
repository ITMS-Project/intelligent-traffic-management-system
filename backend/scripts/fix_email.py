
import subprocess
import os

OLD_EMAIL = "it22925572@my.sliit.lk"
CORRECT_NAME = "Ranidu Pramod"
CORRECT_EMAIL = "promoranidu@gmail.com"

# The filter-branch command
cmd = f'''
git filter-branch --force --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "{OLD_EMAIL}" ]; then
    GIT_AUTHOR_NAME="{CORRECT_NAME}"
    GIT_AUTHOR_EMAIL="{CORRECT_EMAIL}"
fi
if [ "$GIT_COMMITTER_EMAIL" = "{OLD_EMAIL}" ]; then
    GIT_COMMITTER_NAME="{CORRECT_NAME}"
    GIT_COMMITTER_EMAIL="{CORRECT_EMAIL}"
fi
' --tag-name-filter cat -- --branches --tags
'''

print(f"Replacing {OLD_EMAIL} with {CORRECT_EMAIL}...")
try:
    subprocess.run(cmd, shell=True, check=True)
    print("History rewrite successful.")
except subprocess.CalledProcessError as e:
    print(f"Error during history rewrite: {e}")
