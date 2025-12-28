# How to Remove Unwanted Contributors from GitHub

## Your Situation

You have **3 contributors** showing on GitHub:
1. **RP1999** ✅ (Your main account - KEEP)
2. **Ranidu1999** ❌ (Your personal account - REMOVE)
3. **chala-nii** ❌ (Unknown account - REMOVE)

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

### Step 2: Check Ranidu1999 Account
1. Log out of RP1999
2. Log in with your **Ranidu1999** account
3. Go to: https://github.com/settings/emails
4. **Remove these emails if present:**
   - `it22925572@my.sliit.lk`
   - `promoranidu@gmail.com`
5. Save changes

### Step 3: Check chala-nii Account (if you have access)
1. If `chala-nii` is your account:
   - Log in to that account
   - Go to: https://github.com/settings/emails
   - **Remove this email if present:**
     - `hansikachalani875@gmail.com`
   - Save changes

2. If `chala-nii` is NOT your account:
   - This person should not be a contributor (no commits from them)
   - They might have accidentally pushed something, or have one of your emails linked
   - Contact them to unlink your email if they have it

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

## Why Your .mailmap is Perfect

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

**Keep this file as-is!** ✅

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

- **Q: Will this affect my commit history?**
  - A: No! Your git history is already perfect and won't change.

- **Q: Will I lose any work?**
  - A: No! You're just unlinking emails, not deleting anything.

- **Q: Do I need to update the `.mailmap`?**
  - A: No! It's already correct and should be left as-is.

- **Q: What if I can't access chala-nii account?**
  - A: If no commits were made by them (which is true), they shouldn't appear after GitHub syncs. If they persist, contact GitHub support.
