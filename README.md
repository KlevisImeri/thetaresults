# thetaresults

Generating the index.html
```bash
tree -H '.' -L 3 --noreport --dirsfirst ./results | sed '/<p class="VERSION">/,/<\/p>/d' > ./results/index.html
```
