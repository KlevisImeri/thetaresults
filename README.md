# thetaresults

Generating the index.html
```bash
tree -H '.' -L 3 --noreport --dirsfirst ./results | sed '/<p class="VERSION">/,/<\/p>/d' > ./results/index.html
```

2:Expl(100,true) -> PredCart() | 1:Expl() | 1:PredCart()
