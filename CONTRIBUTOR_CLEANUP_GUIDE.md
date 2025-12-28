# How to Remove Unwanted Contributors from GitHub

## QUICK START: Steps to Unlink Ranidu1999

**If you just want the steps to unlink your Ranidu1999 account, jump to [Step 2: Detailed Instructions](#step-2-unlink-emails-from-ranidu1999-account-detailed-steps)**

---

## Your Situation

You have **3 contributors** showing on GitHub:
1. **RP1999** ✅ (Your main account - KEEP)
2. **Ranidu1999** ❌ (Your personal account - REMOVE from contributors)
3. **chala-nii** ❌ (Chalani's account - contact her to unlink)

## Investigation Results

After analyzing your repository's complete git history (115 commits):
- ✅ **ALL commits are clean** - every commit uses only: `163238777+RP1999@users.noreply.github.com`
- ✅ **Your `.mailmap` file is correctly configured**
- ✅ **No commits were made with the email addresses** that could be linked to `Ranidu1999` or `chala-nii`

## Why Are They Showing as Contributors?

GitHub's contributor detection is based on:
1. **Email address linking**: GitHub accounts can have multiple email addresses
2. **Account associations**: If an email in a commit is linked to a GitHub account, that account shows as a contributor

Since your `.mailmap` mentions these emails:
- `hansikachalani875@gmail.com` (possibly linked to `chala-nii`)
- `it22925572@my.sliit.lk` (possibly linked to `Ranidu1999`)
- `promoranidu@gmail.com` (possibly linked to `Ranidu1999`)

If these emails are linked to those GitHub accounts in their settings, GitHub shows them as contributors **even though no commits were made with those emails**.

## Solution: Unlink Email Addresses

### Step 1: Check Your RP1999 Account
1. Go to: https://github.com/settings/emails
2. Log in with your **RP1999** account
3. Note which emails are linked

### Step 2: Unlink Emails from Ranidu1999 Account (DETAILED STEPS)

**Follow these steps carefully:**

1. **Log out of your current GitHub account (RP1999)**
   - Click your profile picture in the top-right corner of GitHub
   - Click "Sign out" at the bottom of the menu

2. **Log in to your Ranidu1999 account**
   - Go to https://github.com/login
   - Enter your Ranidu1999 username and password
   - Complete any 2FA if required

3. **Navigate to Email Settings**
   - Click your profile picture in the top-right corner
   - Click "Settings" from the dropdown menu
   - In the left sidebar, click "Emails"
   - OR directly visit: https://github.com/settings/emails

4. **Find and Remove the Problematic Emails**
   
   Look for these two email addresses in your email list:
   - `it22925572@my.sliit.lk`
   - `promoranidu@gmail.com`
   
   For EACH email you find:
   - Look for a "Remove" or "Delete" button/link next to the email
   - Click the "Remove" button
   - Confirm the removal if prompted
   
   **Note:** If you don't see these emails listed, they're not linked to this account (which is good - nothing to do!)

5. **Verify the Removal**
   - Check that the emails are no longer listed on the page
   - You should only see emails you want associated with Ranidu1999

6. **Log out of Ranidu1999**
   - Click your profile picture
   - Click "Sign out"

7. **Log back into your RP1999 account**
   - Go to https://github.com/login
   - Enter your RP1999 credentials

### Step 3: Check chala-nii Account (if you have access)
1. If `chala-nii` is your account:
   - Log in to that account
   - Go to: https://github.com/settings/emails
   - **Remove this email if present:**
     - `hansikachalani875@gmail.com`
   - Save changes

2. **If `chala-nii` is NOT your account:**
   - **Good news**: Since no commits were made with their account, they should NOT appear as contributors
   - If they still appear, it's likely because:
     - They have `hansikachalani875@gmail.com` linked to their GitHub account in their settings
     - GitHub is incorrectly associating them due to email overlap
   - **What you can do:**
     - Check if `hansikachalani875@gmail.com` is YOUR email address
     - If YES: Contact the `chala-nii` account owner and ask them to remove `hansikachalani875@gmail.com` from their GitHub email settings
     - If NO: This email doesn't belong to you, so you can remove the mapping from your `.mailmap` file
     - Wait 24-48 hours after any email changes for GitHub to recalculate contributors
     - If they persist after 48 hours with no email links, contact GitHub Support to report the issue

### Step 4: Optionally Add Emails to RP1999
If you want to consolidate all your emails under RP1999:
1. Log in to **RP1999** account
2. Go to: https://github.com/settings/emails
3. Add these emails:
   - `it22925572@my.sliit.lk`
   - `promoranidu@gmail.com`
   - `hansikachalani875@gmail.com` (if it's yours)
4. Verify them through email confirmation

### Step 5: Wait for GitHub to Update
- GitHub recalculates contributors periodically (can take minutes to hours)
- You can trigger recalculation by:
  - Making a small commit to the repository
  - Waiting for GitHub's next sync

## Alternative: Remove Collaborator Access

If `Ranidu1999` or `chala-nii` have push access to your repository:

1. Go to your repository Settings → Collaborators and teams
   (URL format: `https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/settings/access`)
2. Remove any collaborators you don't want
3. This prevents them from making future contributions

## Verification

After making changes, verify your git history is still clean:

```bash
# Check all contributors
git shortlog -sne --all

# Should show only entries for:
# Gunarathna RP <163238777+RP1999@users.noreply.github.com>
# (and possibly bot accounts like copilot-swe-agent[bot])
```

## What NOT to Do

❌ **Don't delete the `.mailmap` file** - it's correctly configured and prevents future issues
❌ **Don't rewrite git history** - your commits are already correct
❌ **Don't transfer the repository** - unnecessary since git history is clean

## Why Your .mailmap is Perfect (Or May Need Adjustment)

Your current `.mailmap` file:
```
Gunarathna RP <163238777+RP1999@users.noreply.github.com> <hansikachalani875@gmail.com>
Gunarathna RP <163238777+RP1999@users.noreply.github.com> <it22925572@my.sliit.lk>
Gunarathna RP <163238777+RP1999@users.noreply.github.com> <promoranidu@gmail.com>
Gunarathna RP <163238777+RP1999@users.noreply.github.com> Chala-ni <hansikachalani875@gmail.com>
Gunarathna RP <163238777+RP1999@users.noreply.github.com> Ranidu Pramod <it22925572@my.sliit.lk>
Gunarathna RP <163238777+RP1999@users.noreply.github.com> Ranidu Pramod <promoranidu@gmail.com>
```

This ensures that IF any future commits are made with those emails or names, they'll be attributed to your canonical identity (RP1999).

**Keep this file as-is IF** all these emails belong to you. ✅

**Remove lines related to `hansikachalani875@gmail.com` IF** this email does NOT belong to you and was added by mistake. This would be lines mentioning "Chala-ni" or "hansikachalani875@gmail.com".

## Summary

1. ✅ Your git repository is **perfectly clean**
2. ✅ Your `.mailmap` is **correctly configured**
3. ⚠️ The issue is **GitHub account email linking**, not your code
4. 🔧 **Solution**: Unlink emails from `Ranidu1999` and `chala-nii` accounts
5. ⏱️ **Wait**: GitHub will recalculate contributors after changes

## Need Help?

If after following these steps the contributors still show:
1. Wait 24 hours for GitHub to sync
2. Make a small commit to trigger recalculation
3. Contact GitHub Support if the issue persists

## Questions?

- **Q: I logged into Ranidu1999 but don't see those emails. What now?**
  - A: Great! That means they're not linked to that account. The contributor issue might resolve itself after 24-48 hours, or the emails might be linked elsewhere.

- **Q: I see the emails in Ranidu1999 but can't find the Remove button?**
  - A: Look for a "Delete" link or trash icon next to each email. If it's your primary email, you might need to make another email primary first before removing it.

- **Q: How do I make another email primary in Ranidu1999?**
  - A: In GitHub Settings → Emails, find another email in the list and click "Make primary" next to it. Then you can remove the old one.

- **Q: Will this affect my commit history?**
  - A: No! Your git history is already perfect and won't change.

- **Q: Will I lose any work?**
  - A: No! You're just unlinking emails from GitHub account settings, not deleting anything from the repository.

- **Q: Do I need to update the `.mailmap`?**
  - A: No! It's already correct and should be left as-is (unless the email doesn't belong to you).

- **Q: What if I can't access chala-nii account?**
  - A: If no commits were made by them (which is confirmed), they shouldn't appear once GitHub syncs. If `hansikachalani875@gmail.com` is YOUR email, contact the chala-nii account owner (Chalani) to remove it from their settings. If it's NOT your email, you can remove the mapping from `.mailmap`. Wait 24-48 hours for GitHub to recalculate. If they still appear, contact GitHub support.
