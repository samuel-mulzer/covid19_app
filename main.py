from covid19_model import simulate
from covid19_model.models import sirs_vs, sir

model = sirs_vs

t = 0
d = 1000
h = 0.5

labels = ['S', 'I', 'R']
s0, i0, r0 = 0.313, 0.0014, 0.673
n = 83e6
x0 = [s0, i0, r0]

beta = 0.95
gamma = 1/10
alpha = 1/90
zeta = 0.0014
xi = 0.46

args = (beta, gamma, alpha, zeta, xi)

print('SIRS_VS model | default scenario')
simulate(model, x0, n, t, d, h, args, labels)
