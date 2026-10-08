"""Render the DRT definition as an image (used in article.md / PDF)."""
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
plt.rcParams["mathtext.fontset"] = "cm"
lines = [
 (r"$\mathrm{(1)\ Downside\ regime:}\quad \sigma^{2}_{\downarrow,t}=\lambda\,\sigma^{2}_{\downarrow,t-1}+(1-\lambda)\cdot 2\,\min(r_t,0)^{2},\qquad \lambda=0.97$", 15),
 (r"$\mathrm{(2)\ Standardized\ shocks:}\quad z_s=\dfrac{r_s}{\sigma_{\downarrow,s-1}}$", 15),
 (r"$\mathrm{(3)\ Tail\ multiplier:}\quad \kappa_t=-\,\mathbb{E}\left[\,z_s \mid z_s\leq q_{2.5\%}(z)\,\right],\quad s\in\{t-755,\dots,t\}$", 15),
 (r"$\mathrm{(4)\ DRT:}\quad \mathrm{DRT}_t=\sigma_{\downarrow,t}\times\kappa_t\qquad(\mathrm{if\ returns\ were\ normal:}\ \mathrm{DRT}=2.34\,\sigma)$", 15),
]
fig = plt.figure(figsize=(10, 3.0))
for i, (t, fs) in enumerate(lines):
    fig.text(0.02, 0.84 - i * 0.24, t, fontsize=fs, va="center")
fig.savefig("charts/00_drt_formula.png", dpi=200, bbox_inches="tight", facecolor="white"); print("ok")
