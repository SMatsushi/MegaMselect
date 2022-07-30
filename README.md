# MegaMselect
MegaMillion Lottery candidate computation, displaying bought tickets, jackpot above 4th prize.

## Script
Python3 script with following options:
- -c, --chkJp: check jackpot for ticket purchased, which is described in 4th parameter in cr_assoc in the source.
-  -j <NUM>, --jpFind <NUM>: show jackpot combinations. If <NUM> is 1, the script continues until it find jackpot. If <NUM> is 2, end with finding 2nd prize.
** NOTE) ** Regardless -j 1, or -j 2. This script may crash at around 400 milillon candidates with out of memory for assoc list (maybe).

## Customization
1. random seed: variable rnd_seed is given as random seed.
2. ticket candidates: set cr_assoc[n_apper] : n_apper is appearance count for randomly selected combination. A list given to cr_assoc[n_appear] where:
 - 1st elemnt: m_candi: number of candidates shown
 - 2nd, 3rd: internally used.
 - 3rd: Associative list to show purchased tickets.
```
Suppose:
  cr_assoc[K] = [m_candi, 0, [], {M:True, N:True} ]
  where:
    display m_candi candidates for K times appeard conbinations
    In the list, Mth and N the conbinations are purchased.
```

### Example
Uploaded to this repository as result.txt, result-p1.png, result-p2.png

### result-p1.png
![result-p1](https://user-images.githubusercontent.com/11202459/181937780-0c9be39f-9a49-4e0c-826a-2561e3dad393.png)

### result-p2.png
![result-p2](https://user-images.githubusercontent.com/11202459/181937921-29080e1e-4442-4b76-ac07-2836aaaa3d6a.png)
