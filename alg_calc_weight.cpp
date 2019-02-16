double CalcNewFactor( double oldFactor, Answer::T answer )
{
  return answer == Answer::Correct?
    oldFactor - 0.5 * ( oldFactor - 1 ):
    oldFactor + ( MaxWeight - oldFactor ) * 0.5;
}

minWeight = 1
maxWeight = N (100)
defWeight = (N+1)/2 (50)

correct 1 - oldFactor 50 -> 25,5
correct 2 - oldFactor 25,5 -> 13,25
incorrect 2 - oldFactor 25,5 -> 62,75