Here are all the detailed steps for getting your exercise from GitHub into Colab, then committing it back to GitHub and making a pull request to submit.

It looks complicated, and there are a few places where the details matter. But once you do it several times it will feel natural and make a lot more sense.

#### Part 0: Fork the course repo (you'll only have to do this once)
0. Fork the [`ncsg/ursp688y_sp2024`](https://github.com/ncsg/ursp688y_sp2024) repo to your own account.

#### Part 1: Save your own version of the exercise notebook in Colab
2. Open on the exercise you want to work on in Github.
3. Click on the Colab badge to open it in Colab.
4. Save a working copy of the notebook in your Google Drive. This is where your changes will save while you're working.
   - Go to `File -> Save a copy in Drive`.
   - It will automatically save in a folder called Colab Notebooks in the root Drive directory for whatever account is currently signed into Google.
   - Please remove `Copy of ` from the beginning of the filename and add your last name as an underscored suffix (e.g., `exercise01_harvey.ipynb`)
   - You are welcome to move the file elsewhere in your Drive for your own organization.

#### Part 2: Do the exercise in Colab—save early and often

#### Part 3: Commit the exercise notebook to your own fork
5. Make sure your notebook is named with the convention above (e.g., `exercise01_harvey.ipynb`).
6. Use one of two methods to "commit" the file to your fork of the repository.
   1. **OPTION A: Commit to GitHub by dragging and dropping a downloaded file (Easier)**
        -  Download your notebook from Colab (`File -> Download -> Download .ipynb`).
        -  Go to your fork of the course repo on the GitHub website (https://github.com/insert_your_username/ursp688y_sp2024).
        -  Navigate into the appropriate exercise folder.
        -  Click `Add file` in the upper-right, then `Upload files`.
        -  Drag your _**appropriately named**_ file into the `Drag files here...` space.
        -  Add a short but meaningful commit message (e.g. "completed exercise 1").
        -  Click `Commit changes` (Commit directly to your `main` branch).
   2. **OPTION B: Commit to GitHub directly from Colab (Slightly more advanced, but also more convenient)**
        - Make sure your notebook is appropriately named (e.g., `exercise01_harvey.ipynb`).
        - In Colab, go to `File -> Save a Copy in GitHub`.
        - _**BE CAREFUL WITH THE DETAILS IN THIS PART**_
        - Select your fork of the course repo in the `Repository` dropdown. The branch should be `master`.
        - Change the `File path` to include the folder in the repo where you want the file to be committed (e.g., `exercises/exercise01/exercise01_harvey.ipynb`)
            - If you don't use the right path, your file will end up in the wrong place in the repo and I'll return your pull request for edits.
        - Change the `Commit message` to something short but meaningful (e.g. "completed exercise 1"). It's fine to include a link to Colab. 

#### Part 4: Make a pull request to the course repo

7. Finally, make a "pull request" so that I can see your new file and add it to the course repository (right now it's just on your fork).
8. In your fork on the GitHub website, navigate to the root directory
9. `Sync fork` to make sure your file is the only difference between your fork and the course repo.
    - If prompted, DON'T click the red `Discard commits` button to delete the file you just added; click the green `Update branch` button to sync everything else that might have changed.
10. `Contribute` (to the left of `Sync Fork`), and `Open pull request`.
11. Make sure you are requesting a pull to the `ncsg/ursp688y_sp2024` base repository from your fork. Scroll through to make sure everything looks in order. There are probably one or two commits as part of your pull request, one to `Add files via upload`, and potentially a second to `Merge branch 'ncsg:main' into main`.
12. Click `Create pull request` at the top.
13. Add a short but meaningful title for your pull request (e.g., submitting exercise 1).
14. (optional) Add a description if there's something additional you'd like me (and others) to know about your submission.
15. Click `Create pull request` at the bottom.

#### 🙌 Congrats!
