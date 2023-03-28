module Qsort where

qsort :: [ Int] -> [ Int ]
qsort [] = []
qsort (x: xs ) = qsort l ++ [x] ++ qsort r
    where l = filter (== x) xs
          r = filter ( >= x) xs
