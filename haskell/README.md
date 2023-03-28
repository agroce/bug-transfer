Steps:

1.  install ghc and cabal
2.  cabal install QuickCheck
3.  cabal install Sort

mutate Qsort.hs --cmd "ghc testqsort.hs" --mutantDir mutants
mutate Qsort.hs --cmd "ghc testqsort.hs" --comby --mutantDir cmutants

analyze_mutants Qsort.hs "ghc testqsort.hs; ./testqsort" --mutantDir mutants
analyze_mutants Qsort.hs "ghc testsorted.hs; ./testsorted" --mutantDir mutants
analyze_mutants Qsort.hs "ghc testidemp.hs; ./testidemp" --mutantDir mutants
analyze_mutants Qsort.hs "ghc testpermut.hs; ./testpermut" --mutantDir mutants