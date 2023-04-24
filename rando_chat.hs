#!/usr/bin/runhaskell

--cabal install random --lib
import System.Random

noun :: Int -> String
noun i = ["I","you","he","she","it","them"]!!i

verb :: Int -> String
verb i = ["be","have","do","say","get","make","go","know","take","see","come","think","look","want","give","use","find","tell","ask","work","seem","feel","try","leave","call"]!!i

adjective :: Int -> String
adjective i = ["good","new","first","last","long","great","little","own","other","old","right","big","high","different","small","large","next","early","young","important","few","public","bad","same","able"]!!i

adverb :: Int -> String
adverb i = ["up","so","out","just","now","how","then","more","also","here","well","only","very","even","back","there","down","still","in","as","too","when","never","really","most"]!!i

preposition :: Int -> String
preposition i = ["of","in","to","for","with","on","at","from","by","about","as","into","like","through","after","over","between","out","against","during","without","before","under","around","among"]!!i

conjunction :: Int -> String
conjunction i = ["and","that","but","or","as","if","when","than","because","while","where","after","so","though","since","until","whether","before","although","nor","like","once","unless","now","except"]!!i

output :: IO()
output = do
  rando <- randomIO :: IO Int
--let num_words = mod 32 ((take 1 (randomList rando))!!0) + 5
  let nums_list = take 5 (randomList rando)
  let noun1 = noun (mod (nums_list!!0) 6)
  let verb1 = verb (mod (nums_list!!1) 25)
  let adjective1 = adjective (mod (nums_list!!2) 25)
  let adverb1 = adverb (mod (nums_list!!3) 25)
  let noun2 = noun (mod (nums_list!!4) 6)
  print (noun1 ++ " " ++ adverb1 ++ " " ++ verb1 ++ " " ++ adjective1 ++ " " ++ noun2)

randomList :: Int -> [Int]
randomList seed = randoms (mkStdGen seed) :: [Int]

readUserInput :: IO()
readUserInput = do
  user_input <- getLine
  output
  readUserInput

main :: IO()
main = do
  putStrLn "Hello."
  readUserInput
