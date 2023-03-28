{-# LANGUAGE TemplateHaskell #-}

import Control.Monad
import Test.QuickCheck
import Test.QuickCheck.Test
import System.Exit
import Data.List
import Qsort

prop_idemp xs = qsort xs == qsort ( qsort xs )
prop_sorted xs = sort ( qsort xs ) == (qsort xs)

return []
runTests = $quickCheckAll

main :: IO ()
main = do
  result <- runTests
  unless result exitFailure
