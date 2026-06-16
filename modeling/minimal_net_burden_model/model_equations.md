# Minimal NET Burden Model Equations

dB/dt = F(A, M, S) - [D + C] * B + P
Y(t) = K_R(R) * B(t) + epsilon

## Definitions:
- `B`: true NET burden, latent.
- `Y`: observed biomarker, observable.
- `F`: formation rate, latent unless direct formation assay.
- `D`: degradation capacity, partially observable only with degradation assay.
- `C`: systemic clearance, latent unless clearance assay.
- `P`: spatial persistence, latent.
- `K_R`: composition/detectability factor.
- `A`, `M`, `S`: upstream potential/constraint variables, not executed function.

This model is an identifiability demonstration, not a disease simulator.
