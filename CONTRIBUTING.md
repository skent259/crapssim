### Generated Reports
Artifacts under any `reports/` directory are generated and should not be committed. They are ignored via `.gitignore`. 
If previously tracked, run:

git rm -r --cached reports/ || true
git ls-files -z | grep -z "/reports/" | xargs -0 git rm --cached -r --ignore-unmatch || true

This removes them from the index while keeping files on disk.
