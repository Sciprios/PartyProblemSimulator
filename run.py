from equation.BoolTree import Equation
from solvers.FlipGA import FlipGA
from solvers.BlindGA import BlindGA

# Define problem
vars = '(A+B+D).(A+B+D).(A+E+C).(F+B+C).(D+I+H).(A+H+G).(G+J+C).(G+B+I).(E+H+J).(I+J+F).'
vars = vars + '(¬A+¬B+¬D).(¬A+¬B+¬D).(¬A+¬E+¬C).(¬F+¬B+¬C).(¬D+¬I+¬H).(¬A+¬H+¬G).(¬G+¬J+¬C).(¬G+¬B+¬I).(¬E+¬H+¬J).(¬I+¬J+¬F)'

# Define equation and algorithm
eq = Equation(vars)
#ga = BlindGA(eq, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
ga = FlipGA(eq, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
ga.run()

# eq = Equation('(A).(B).(C).(D).(E).(F).(G).(H).(I).(J).(K).(L).(M).(N).(O).(P).(Q).(R).(S).(T).(U).(V).(W).(X).(Y).(Z)')
# ga = FlipGA(eq, ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
# ga.run()

#eq = Equation('(A).(B).(C).(D).(E).(F)')
#ga = FlipGA(eq, ['A', 'B', 'C', 'D', 'E', 'F'])
#ga.run().0