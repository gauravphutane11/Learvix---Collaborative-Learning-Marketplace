# Learvix Feature Upgrade — SkillProof + Member Photos

This upgrade adds a working SkillProof assessment flow and profile photos while retaining the existing Learvix login, matching, exchanges, progress, notifications and navigation.

## New SkillProof functionality

- Five assessment tracks: Python, JavaScript, SQL, React and UI/UX Design.
- Ten advanced multiple-choice questions per track (50 questions total).
- Questions are delivered by the Flask API without answer keys.
- The backend grades submitted answers and stores every attempt.
- Score is out of 100; 80% or higher verifies that skill.
- Passing a new skill creates a SkillProof notification and adds the badge to the member profile.
- Passing at least one skill unlocks the Learvix Trusted Member marker.
- Members can review attempt history and answer explanations.

The badge means the member passed this in-app knowledge assessment. It is not a third-party certification or a guarantee of real-world job performance.

## Profile photo functionality

- JPG, PNG and WEBP uploads up to 450 KB.
- Photo preview before saving.
- Image is saved to the authenticated member's profile.
- Profile photo appears in the navbar, matching cards, home suggestions and profile page.
- The API validates the data URL and enforces a size limit.

## Apply the patch to an existing Learvix folder

1. Stop the Flask server with `Ctrl+C`.
2. Make a backup copy of `backend/instance/learvix.db` (or the SQLite file configured by `DATABASE_URL`).
3. Extract `Learvix_Feature_Upgrade_Patch.zip` into the root of your existing Learvix project folder and allow files to be overwritten.
4. Do not delete or replace `backend/.env`, `backend/.venv`, your database, or your frontend `.env` files.
5. Start Flask again from `backend` using the same virtual environment: `python app.py`.
6. The app creates the new SkillProof table and adds the two new user columns to an existing SQLite database automatically.
7. Keep the frontend dev server running, or restart it with `npm run dev` from `frontend`.
8. Refresh the browser, open SkillProof and start an assessment.

No new npm or Python packages are required by this feature upgrade.

## SkillProof flow

1. Open SkillProof from the top navigation.
2. Choose one of the five skill tracks.
3. Answer all ten questions; move between questions with Previous/Next.
4. Submit the assessment.
5. Review score, correct answers and explanations.
6. At 80% or above, the skill is added to Verified Skills and Trusted Member status is unlocked after the first passed track.
7. Visit Profile to see the photo, verified skill badges and member status.

## Verification performed for this package

- Python source compilation: passed.
- Frontend JS/JSX syntax parsing: passed for all 13 source files.
- Question bank validation: five tracks, ten questions each; all answer keys and grading paths checked.
- Full live Flask/API and browser integration test: not run in the packaging environment because Flask dependencies were not installed here.
- `npm install` timed out in the packaging environment; no dependency was added by this upgrade.
