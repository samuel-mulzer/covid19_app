import pandas as pd
import numpy as np
import streamlit as st

from covid19_model.models import sirs_vs
from covid19_model.solver import solve
from covid19_model.visualizer import visualize

st.set_page_config(
    page_title="streamlit · covid19 simulation",
    layout="wide",
    menu_items={
        'Report a bug': "mailto:samuel.mulzer@icloud.com?subject=Bug report: Covid-19 streamlit",
        'About': """
            # Covid19 simulation
            Epidemiologic simulation of Covid-19 using an compartmental SIRS-model with vaccinations and seasonality 
            
            © Samuel Mulzer, 2022
        """
    }
)


model = sirs_vs

st.write("# Covid-19 simulation")

st.write("## Settings")
col1, col2, col3 = st.columns(3)

col1.write("#### Start")
s0 = col1.number_input("s0", 0.0, 1.0, value=0.313, step=0.1, format="%.4f")
i0 = col1.number_input("i0", 0.0, 1.0, value=0.0136, step=0.1, format="%.4f")
r0 = col1.number_input("r0", 0.0, 1.0, value=0.673, step=0.1, format="%.4f")
n = col1.number_input("n", 0.0, 100e6, value=1.0, step=1e6)

x0 = np.array([s0, i0, r0], dtype=float)
labels = ["s", "i", "r"]

col2.write("#### Time")
t = col2.number_input("start", 0, 10000, value=0, step=100)
d = col2.number_input("duration", 1, 10000, value=1000, step=100)
h = col2.number_input("precision", 0.0, 10.0, value=1.0, step=0.1)
tspan = np.arange(t, t+d, h)

col3.write("#### Params")

beta = col3.number_input("beta", 0.0, 5.0, value=0.95, step=0.1, format="%.2f")
gamma = col3.number_input(
    "gamma", 0.01, 1.0, value=1/10, step=0.1, format="%.2f")
alpha = col3.number_input("alpha", 0.0, 1.0, value=1/90,
                          step=0.01, format="%.3f")
zeta = col3.number_input("zeta", 0.0, 1.0, value=0.0014,
                         step=0.001, format="%.4f")
xi = col3.number_input("xi", 0.0, 1.0, value=0.46, step=0.1, format="%.2f")

args = (beta, gamma, alpha, zeta, xi)


st.write("## Results")

solution = solve(model, x0, tspan, h, args)
time_series = solution.transpose()

data = pd.DataFrame(
    solution * n,
    index=tspan,
    columns=['S', 'I', 'R']
)

index_max = time_series[1].argmax()
i_max = time_series[1][index_max]

fig, loc = visualize(time_series, n, tspan, args, labels)


st.line_chart(data)

st.latex(r"t = 60:" + r"i_{max}=" +
         rf"{i_max:.2g}" + r", I_{max}=" + rf"{i_max*n:.3g}")
st.markdown("---")

st.pyplot(fig)
