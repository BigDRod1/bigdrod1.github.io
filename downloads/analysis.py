"""
Is standard deviation a good measure of risk?  Reproducible analysis for
"The Tyranny of the Bell Curve" (Diego Rodriguez).

Data: Yahoo Finance daily adjusted closes via yfinance (see download_data.py),
cut at 2026-09-30.  All numbers in the article come from this script.

Sections
  A. Stylised facts: normality tests, tails, clustering, -100% bound
  B. Risk measures, incl. the proposed DRT (Downside Regime-Tail) measure
  C. Out-of-sample prediction of future tail risk (panel of 48 assets)
  D. VaR / ES backtests (Kupiec, Christoffersen, ES ratio test)
  E. Portfolio test (min-risk portfolios, monthly rebalance) + bootstrap
"""
import warnings, json
import numpy as np, pandas as pd
from scipy import stats, optimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import sliding_window_view as swv

warnings.filterwarnings("ignore")
np.random.seed(42)
END = "2026-09-30"
CH = "charts/"
RES = []          # long-format results -> results.csv
def rec(section, item, method, metric, value):
    RES.append(dict(section=section, item=item, method=method, metric=metric, value=value))

plt.rcParams.update({"figure.dpi": 130, "savefig.bbox": "tight", "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 10, "axes.titlesize": 12,
                     "axes.titleweight": "bold"})
NAVY, RED, GREEN, GREY, GOLD = "#0B2545", "#C8102E", "#2E8B57", "#8D99AE", "#E0A100"

px = pd.read_csv("data/prices_daily.csv", index_col=0, parse_dates=True).loc[:END]
irx = pd.read_csv("data/irx_daily.csv", index_col=0, parse_dates=True).squeeze().loc[:END]
RET = {t: px[t].dropna().pct_change().dropna() for t in px.columns}
RET = {t: r[r.index >= r.index[0]] for t, r in RET.items()}

# ---------------------------------------------------------------- helpers
LAM, LAM_DN, ZWIN, ALPHA = 0.94, 0.97, 756, 0.975

def ewma_var(r, lam, downside=False):
    x = np.minimum(r, 0.0) if downside else r
    x2 = (2.0 * x**2) if downside else x**2
    out = np.empty_like(x2); v = np.mean(x2[:30])
    for i, e in enumerate(x2):
        v = lam * v + (1 - lam) * e
        out[i] = v                                 # uses info up to and incl. i
    return out

def es_left(x, a=0.05):
    """Expected shortfall (positive loss) of the left a-tail."""
    q = np.quantile(x, a); return -x[x <= q].mean()

def mdd(r):
    w = np.cumprod(1 + np.asarray(r)); peak = np.maximum.accumulate(np.r_[1.0, w])[1:]
    return -(w / peak - 1).min()

def cf_var(x, a=0.05):
    mu, sd = x.mean(), x.std(ddof=1); S = stats.skew(x); K = stats.kurtosis(x)
    z = stats.norm.ppf(a)
    zc = z + (z**2 - 1) * S / 6 + (z**3 - 3 * z) * K / 24 - (2 * z**3 - 5 * z) * S**2 / 36
    return -(mu + zc * sd)

def components(r):
    """Return DataFrame of daily risk state for one asset (all known at close of day)."""
    a = r.values
    sig = np.sqrt(ewma_var(a, LAM)); sdn = np.sqrt(ewma_var(a, LAM_DN, True))
    df = pd.DataFrame({"r": a, "sig": sig, "sdn": sdn}, index=r.index)
    df["z_sym"] = df.r / df.sig.shift(1).clip(lower=1e-4)           # standardised by yesterday's forecast
    df["z_dn"] = df.r / df.sdn.shift(1).clip(lower=1e-4)
    return df

# ======================================================== A. STYLISED FACTS
print("A. stylised facts")
facts = {}
g = RET["^GSPC"]; s = RET["SPY"]
for name, r in [("^GSPC", g), ("SPY", s)]:
    jb = stats.jarque_bera(r)
    facts[name] = dict(start=str(r.index[0].date()), n=len(r), mean=r.mean(), sd=r.std(),
                       skew=stats.skew(r), exkurt=stats.kurtosis(r), jb=jb.statistic, jb_p=jb.pvalue)
# normality across assets, daily and monthly
rows = []
for t, r in RET.items():
    m = (1 + r).resample("ME").prod() - 1
    m = m.iloc[1:-0 or None]
    y = (1 + r).resample("YE").prod() - 1
    for freq, x in [("daily", r), ("monthly", m)]:
        jb = stats.jarque_bera(x); sw = stats.shapiro(x.sample(min(len(x), 4999), random_state=1))
        rows.append(dict(ticker=t, freq=freq, n=len(x), start=str(r.index[0].date()),
                         ann_vol=x.std() * np.sqrt((365 if t == "BTC-USD" else 252) if freq == "daily" else 12),
                         skew=stats.skew(x), exkurt=stats.kurtosis(x), jb=jb.statistic, jb_p=jb.pvalue,
                         shapiro_p=sw.pvalue, min=x.min(), max=x.max(),
                         dd_over_sd=np.sqrt(np.mean(np.minimum(x, 0)**2)) / x.std()))
norm_tab = pd.DataFrame(rows); norm_tab.to_csv("results/normality_tests.csv", index=False)
for _, rw in norm_tab.iterrows():
    for k in ["skew", "exkurt", "jb", "jb_p"]:
        rec("A_normality", rw.ticker, rw.freq, k, rw[k])
d_ = norm_tab[norm_tab.freq == "daily"]; m_ = norm_tab[norm_tab.freq == "monthly"]
facts["n_assets"] = len(d_); facts["jb_reject_daily"] = int((d_.jb_p < 0.01).sum())
facts["jb_reject_monthly"] = int((m_.jb_p < 0.01).sum())
facts["median_exkurt_daily"] = d_.exkurt.median(); facts["median_exkurt_monthly"] = m_.exkurt.median()

# tail counts for S&P 500 since 1928
z = (g - g.mean()) / g.std(); n = len(g)
tail = {}
for k in [3, 4, 5, 6, 7, 10]:
    obs = int((z < -k).sum()); exp = n * stats.norm.cdf(-k)
    tail[k] = dict(observed_down=obs, expected_normal=exp, obs_up=int((z > k).sum()),
                   years_between_under_normal=1 / (stats.norm.cdf(-k) * 252))
    rec("A_tails", "^GSPC", f"<-{k}sd", "observed", obs); rec("A_tails", "^GSPC", f"<-{k}sd", "expected_normal", exp)
facts["tails"] = tail
# famous days: z-score vs full-sample and vs trailing-1y sd
famous = {"1987-10-19": "Black Monday", "2008-10-15": "GFC", "2008-09-29": "Lehman/TARP vote",
          "2020-03-16": "COVID", "2020-03-12": "COVID 2", "1929-10-28": "1929", "2025-04-04": "Tariff shock",
          "2025-04-03": "Tariff shock 1", "2025-04-09": "Tariff rally", "2008-10-13": "GFC rally"}
fam = []
gsd_trail = g.rolling(252).std().shift(1)
for d, lab in famous.items():
    if pd.Timestamp(d) in g.index:
        r_ = g.loc[d]; zf = r_ / g.std(); zt = r_ / gsd_trail.loc[d]
        p = stats.norm.sf(abs(zf)) if abs(zf) < 37 else 0.0
        fam.append(dict(date=d, event=lab, ret=r_, z_full=zf, z_trailing=zt, normal_prob=p,
                        log10_years=np.log10(1 / (p * 252)) if p > 0 else np.inf))
fam = pd.DataFrame(fam); fam.to_csv("results/famous_days.csv", index=False)
facts["famous"] = fam.to_dict("records")
# best/worst ever days
facts["gspc_worst5"] = g.nsmallest(5).to_dict(); facts["gspc_best5"] = g.nlargest(5).to_dict()
facts["gspc_worst5"] = {str(k.date()): v for k, v in facts["gspc_worst5"].items()}
facts["gspc_best5"] = {str(k.date()): v for k, v in facts["gspc_best5"].items()}
# share of total log growth from best days
lg = np.log1p(g)
facts["gspc_total_logret"] = lg.sum()
for k in [10, 20, 50]:
    facts[f"gspc_logret_ex_best{k}"] = lg.sum() - lg.nlargest(k).sum()
    facts[f"gspc_logret_ex_worst{k}"] = lg.sum() - lg.nsmallest(k).sum()
facts["gspc_best10_within_2w_of_worst"] = None
worst = g.nsmallest(20).index; best = g.nlargest(20).index
gap = [min(abs((b - w).days) for w in worst) for b in best]
facts["best20_within_30d_of_a_worst20"] = int(np.sum(np.array(gap) <= 30))

# volatility clustering: ACF of r and |r|, Ljung-Box, ARCH-LM, GARCH fits
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.tsa.stattools import acf
from arch import arch_model
acf_r = acf(s, nlags=100, fft=True); acf_a = acf(s.abs(), nlags=100, fft=True)
facts["spy_acf_r_lag1"] = acf_r[1]; facts["spy_acf_abs_lag1"] = acf_a[1]
facts["spy_acf_abs_lag50"] = acf_a[50]; facts["spy_acf_abs_lag100"] = acf_a[100]
facts["spy_acf_abs_positive_lags_of_100"] = int((acf_a[1:] > 1.96 / np.sqrt(len(s))).sum())
lb = acorr_ljungbox(s, lags=[10]); lba = acorr_ljungbox(s.abs(), lags=[10])
facts["spy_LB10_r"] = float(lb.lb_stat.iloc[0]); facts["spy_LB10_r_p"] = float(lb.lb_pvalue.iloc[0])
facts["spy_LB10_abs"] = float(lba.lb_stat.iloc[0]); facts["spy_LB10_abs_p"] = float(lba.lb_pvalue.iloc[0])
al = het_arch(s - s.mean(), nlags=5); facts["spy_archLM5"] = al[0]; facts["spy_archLM5_p"] = al[1]
garch = arch_model(s * 100, vol="GARCH", p=1, q=1, dist="t", mean="Constant").fit(disp="off")
gjr = arch_model(s * 100, vol="GARCH", p=1, o=1, q=1, dist="t", mean="Constant").fit(disp="off")
facts["garch"] = {k: float(v) for k, v in garch.params.items()}
facts["gjr"] = {k: float(v) for k, v in gjr.params.items()}
facts["garch_persistence"] = garch.params["alpha[1]"] + garch.params["beta[1]"]
facts["garch_halflife_days"] = np.log(0.5) / np.log(facts["garch_persistence"])
facts["gjr_bic"] = gjr.bic; facts["garch_bic"] = garch.bic
facts["gjr_tstat_gamma"] = float(gjr.tvalues["gamma[1]"])
# rolling vol range
rv = s.rolling(21).std() * np.sqrt(252)
facts["spy_rv21_min"] = rv.min(); facts["spy_rv21_min_date"] = str(rv.idxmin().date())
facts["spy_rv21_max"] = rv.max(); facts["spy_rv21_max_date"] = str(rv.idxmax().date())
facts["spy_rv21_median"] = rv.median()
# leverage: correlation of return with next-month change in vol
# -100% bound: 1-year returns of individual stocks and annual returns
stocks = ["AAPL","MSFT","AMZN","JPM","XOM","JNJ","KO","GE","IBM","PG","WMT","CVX","INTC","CSCO","PFE",
          "BAC","C","NVDA","T","DIS","HD","MRK","F","BA","CAT","MMM"]
yr = []
for t in stocks:
    p = px[t].dropna(); a = (p.resample("YE").last().pct_change().dropna())
    a = a[a.index.year < 2026]; yr += list(a.values)
yr = np.array(yr)
_yl = []
for t in stocks:
    p = px[t].dropna(); a = p.resample("YE").last().pct_change().dropna(); a = a[a.index.year < 2026]
    _yl += [(t, int(k.year), float(v)) for k, v in a.items()]
_yl = sorted(_yl, key=lambda z: z[2]); facts["stock_year_worst3"] = _yl[:3]; facts["stock_year_best5"] = _yl[-5:]
facts["stock_years_n"] = len(yr); facts["stock_year_skew"] = stats.skew(yr)
facts["stock_year_max"] = yr.max(); facts["stock_year_min"] = yr.min()
facts["stock_year_mean"] = yr.mean(); facts["stock_year_median"] = np.median(yr)
facts["stock_year_max_who"] = None
facts["stock_year_gt100"] = int((yr > 1.0).sum()); facts["stock_year_lt_m50"] = int((yr < -0.5).sum())
mu_y, sd_y = yr.mean(), yr.std(ddof=1)
facts["stock_year_normal_prob_below_m100"] = stats.norm.cdf(-1, mu_y, sd_y)
facts["stock_year_mean_minus_2sd"] = mu_y - 2 * sd_y; facts["stock_year_sd"] = sd_y
btc = RET["BTC-USD"]; by = (px["BTC-USD"].dropna().resample("YE").last().pct_change().dropna())
facts["btc_annual"] = {str(k.year): v for k, v in by.items()}
facts["spy_days_below_m5pct"] = int((s < -0.05).sum()); facts["spy_days_above_p5pct"] = int((s > 0.05).sum())
facts["spy_expected_below_m5pct_normal"] = len(s) * stats.norm.cdf(-0.05, s.mean(), s.std())
facts["spy_aug2008_sd_ann"] = None
facts["btc_daily_skew"] = stats.skew(btc); facts["btc_daily_exkurt"] = stats.kurtosis(btc)

# ---- charts A
# A1 histogram vs normal (SPY)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
x = s.values; mu, sd = x.mean(), x.std()
bins = np.linspace(-0.12, 0.12, 241)
ax[0].hist(x, bins=bins, density=True, color=NAVY, alpha=.8, label="SPY daily returns")
xx = np.linspace(-.12, .12, 1000)
ax[0].plot(xx, stats.norm.pdf(xx, mu, sd), color=RED, lw=2, label="Normal, same mean & SD")
ax[0].set_xlim(-.06, .06); ax[0].set_title("SPY daily returns vs. the bell curve")
ax[0].legend(frameon=False, loc="upper left", fontsize=8); ax[0].set_xlabel("Daily return")
ax[1].hist(x, bins=bins, density=True, color=NAVY, alpha=.8)
ax[1].plot(xx, stats.norm.pdf(xx, mu, sd), color=RED, lw=2)
ax[1].set_yscale("log"); ax[1].set_ylim(1e-3, 100); ax[1].set_xlim(-.12, .12)
ax[1].set_title("Same chart, log scale: look at the tails"); ax[1].set_xlabel("Daily return")
fig.text(0.01, -0.03, f"Data: Yahoo Finance, SPY {s.index[0].date()} to {s.index[-1].date()}, n={len(s):,}. "
         f"Skew {stats.skew(x):.2f}, excess kurtosis {stats.kurtosis(x):.1f}.", fontsize=8, color=GREY)
fig.savefig(CH + "01_spy_hist_vs_normal.png"); plt.close()
# A2 QQ plots
fig, ax = plt.subplots(1, 3, figsize=(13, 4.2))
for a_, (lab, r) in zip(ax, [("S&P 500 daily, 1928-2026", g), ("SPY monthly", (1 + s).resample("ME").prod() - 1),
                             ("Bitcoin daily", btc)]):
    zz = np.sort((r - r.mean()) / r.std()); th = stats.norm.ppf((np.arange(1, len(zz) + 1) - .5) / len(zz))
    a_.scatter(th, zz, s=4, color=NAVY); lim = max(abs(zz).max(), 4)
    a_.plot([-lim, lim], [-lim, lim], color=RED, lw=1.5); a_.set_title(lab)
    a_.set_xlabel("Normal quantile (SDs)"); a_.set_ylabel("Observed quantile (SDs)")
fig.suptitle("QQ plots: if returns were normal, every dot would sit on the red line", y=1.03, fontweight="bold")
fig.savefig(CH + "02_qq_plots.png"); plt.close()
# A3 tails bar chart
fig, ax = plt.subplots(figsize=(8, 4))
ks = [3, 4, 5, 6, 7]; o = [tail[k]["observed_down"] for k in ks]; e = [tail[k]["expected_normal"] for k in ks]
xi = np.arange(len(ks)); ax.bar(xi - .2, o, .4, color=NAVY, label="Observed"); ax.bar(xi + .2, e, .4, color=RED, label="Expected if normal")
ax.set_yscale("log"); ax.set_xticks(xi); ax.set_xticklabels([f"< -{k} SD" for k in ks])
for i in range(len(ks)):
    ax.text(xi[i] - .2, o[i] * 1.15, f"{o[i]}", ha="center", fontsize=8)
    ax.text(xi[i] + .2, max(e[i], 1e-6) * 1.15, f"{e[i]:.2g}", ha="center", fontsize=8)
ax.set_ylim(1e-6, 2000)
ax.set_title(f"S&P 500 down days by size, {g.index[0].year}-2026 ({n:,} days)"); ax.legend(frameon=False)
fig.savefig(CH + "03_tail_counts.png"); plt.close()
# A4 rolling vol + ACF
fig, ax = plt.subplots(1, 2, figsize=(13, 4.2), gridspec_kw={"width_ratios": [2, 1]})
ax[0].plot(rv.index, rv, color=NAVY, lw=.8); ax[0].axhline(s.std() * np.sqrt(252), color=RED, ls="--", lw=1.2,
                                                            label=f"Full-sample SD: {s.std()*np.sqrt(252):.0%}")
ax[0].set_title("SPY 21-day realized volatility (annualized)"); ax[0].legend(frameon=False)
ax[0].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
ax[1].bar(range(1, 101), acf_a[1:], color=NAVY, width=1, label="|returns|")
ax[1].bar(range(1, 101), acf_r[1:], color=GOLD, width=1, alpha=.9, label="returns")
ax[1].axhline(1.96 / np.sqrt(len(s)), color=RED, lw=.8, ls="--"); ax[1].axhline(-1.96 / np.sqrt(len(s)), color=RED, lw=.8, ls="--")
ax[1].set_title("Autocorrelation, lags 1-100 days"); ax[1].legend(frameon=False); ax[1].set_xlabel("Lag (days)")
fig.savefig(CH + "04_vol_clustering.png"); plt.close()
# A5 annual stock returns distribution (the -100% wall)
fig, ax = plt.subplots(figsize=(8, 4))
ax.hist(yr, bins=np.arange(-1, max(3.2, yr.max() + .1), .05), color=NAVY, density=True, label="Observed calendar-year returns")
xx = np.linspace(-1.6, 3.2, 500); ax.plot(xx, stats.norm.pdf(xx, mu_y, sd_y), color=RED, lw=2, label="Normal fit")
ax.fill_between(xx[xx < -1], stats.norm.pdf(xx[xx < -1], mu_y, sd_y), color=RED, alpha=.3)
ax.axvline(-1, color="k", lw=1); ax.text(-1.65, ax.get_ylim()[1] * .62, "Impossible:\nloss > 100%", color=RED, fontsize=9)
ax.set_xlim(-1.7, 4.6)
ax.annotate(f"Off chart: best year +{yr.max():.0%}", xy=(4.5, .05), ha="right", fontsize=8, color=GREY)
ax.set_title(f"{len(stocks)} large-cap stocks, {len(yr):,} stock-years: the -100% wall")
ax.set_xlabel("Calendar-year return"); ax.legend(frameon=False); ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
fig.savefig(CH + "05_annual_stock_returns.png"); plt.close()

# ======================================================== B. RISK STATES
print("B. risk states")
COMP = {t: components(r) for t, r in RET.items()}

def measures_at(t, end_idx):
    """All trailing risk measures for asset t using data up to and including position end_idx."""
    c = COMP[t]; r = c.r.values
    w = r[end_idx - 251:end_idx + 1]
    zd = c.z_dn.values[end_idx - ZWIN + 1:end_idx + 1]; zs = c.z_sym.values[end_idx - ZWIN + 1:end_idx + 1]
    kap_dn = es_left(zd, 1 - ALPHA); kap_sym = es_left(zs, 1 - ALPHA)
    return dict(SD=w.std(ddof=1), DD=np.sqrt(np.mean(np.minimum(w, 0)**2)), CVaR=es_left(w, 0.05),
                mVaR=cf_var(w, 0.05), EWMA=c.sig.values[end_idx], FHS=c.sig.values[end_idx] * kap_sym,
                DRT=c.sdn.values[end_idx] * kap_dn, kappa=kap_dn, sdn=c.sdn.values[end_idx])

# ======================================================== C. PREDICTION PANEL
print("C. prediction panel")
PANEL_ASSETS = [t for t in RET if t != "^GSPC"]
rows = []
for t in PANEL_ASSETS:
    c = COMP[t]; idx = c.index; r = c.r.values
    me = pd.Series(np.arange(len(idx)), index=idx).groupby(idx.to_period("M")).max()
    for per, i in me.items():
        if i < ZWIN + 5 or i + 252 >= len(r): 
            if i < ZWIN + 5 or i + 63 >= len(r): continue
        m = measures_at(t, i)
        f63 = r[i + 1:i + 64]; f21 = r[i + 1:i + 22]
        row = dict(ticker=t, period=per, date=idx[i], **m,
                   fwd_ES63=es_left(f63, 0.05), fwd_MDD63=mdd(f63), fwd_worst21=-f21.min(),
                   fwd_SD63=f63.std(ddof=1), fwd_DD63=np.sqrt(np.mean(np.minimum(f63, 0)**2)))
        if i + 252 < len(r):
            f252 = r[i + 1:i + 253]; row["fwd_MDD252"] = mdd(f252); row["fwd_ES252"] = es_left(f252, 0.025)
        rows.append(row)
P = pd.DataFrame(rows); P.to_csv("results/prediction_panel.csv", index=False)
print("panel", P.shape, P.period.min(), P.period.max())
METH = ["SD", "DD", "CVaR", "mVaR", "EWMA", "FHS", "DRT"]
TARGETS = ["fwd_ES63", "fwd_MDD63", "fwd_worst21", "fwd_MDD252", "fwd_ES252", "fwd_SD63", "fwd_DD63"]
HLAG = {"fwd_ES63": 3, "fwd_MDD63": 3, "fwd_worst21": 1, "fwd_MDD252": 12, "fwd_ES252": 12, "fwd_SD63": 3, "fwd_DD63": 3}

def nw_t(x, lags):
    x = np.asarray(x); x = x[~np.isnan(x)]; T = len(x); u = x - x.mean()
    v = u @ u / T
    for L in range(1, lags + 1):
        v += 2 * (1 - L / (lags + 1)) * (u[L:] @ u[:-L]) / T
    return x.mean() / np.sqrt(v / T), T

pred_rows = []; cs_series = {}
for tg in TARGETS:
    D = P.dropna(subset=[tg]).copy()
    lt = np.log(D[tg].clip(lower=1e-6))
    # (1) pooled Spearman
    for mth in METH:
        rec("C_pred", tg, mth, "pooled_spearman", stats.spearmanr(D[mth], D[tg])[0])
    # (2) cross-sectional Spearman per month (needs >= 15 assets)
    cs = {}
    for per, Gp in D.groupby("period"):
        if len(Gp) >= 15:
            cs[per] = {m: stats.spearmanr(Gp[m], Gp[tg])[0] for m in METH}
    cs = pd.DataFrame(cs).T; cs_series[tg] = cs
    # (3) time-series (within-asset) Spearman, averaged over assets
    ts = D.groupby("ticker").apply(lambda Gp: pd.Series({m: stats.spearmanr(Gp[m], Gp[tg])[0] for m in METH}))
    # (4) in-sample log-log R2 pooled and within-asset (demeaned)
    # (5) out-of-sample: expanding pooled regression of log target on log predictor
    D["ly"] = lt.values
    pers = sorted(D.period.unique()); gap = HLAG[tg] + 1
    oos = {m: [] for m in METH}; oos_y = []; oos_bench = []; oos_per = []
    for k, per in enumerate(pers):
        if k < 120: continue                              # need 10y of history to calibrate
        train = D[D.period <= pers[k - gap]]; test = D[D.period == per]
        if len(test) == 0: continue
        oos_y += list(test.ly); oos_bench += [train.ly.mean()] * len(test); oos_per += [per] * len(test)
        for m in METH:
            X = np.log(train[m].clip(lower=1e-4)); b, a = np.polyfit(X, train.ly, 1)
            oos[m] += list(a + b * np.log(test[m].clip(lower=1e-4)))
    oos_y = np.array(oos_y); oos_bench = np.array(oos_bench); oos_per = np.array(oos_per)
    for m in METH:
        rho = cs[m]
        r2 = stats.pearsonr(np.log(D[m].clip(lower=1e-4)), D.ly)[0]**2
        Dm = D[[m, "ly", "ticker"]].copy(); Dm["x"] = np.log(Dm[m].clip(lower=1e-4))
        Dm[["x", "ly"]] = Dm[["x", "ly"]] - Dm.groupby("ticker")[["x", "ly"]].transform("mean")
        r2w = stats.pearsonr(Dm.x, Dm.ly)[0]**2
        e = oos_y - np.array(oos[m]); r2oos = 1 - np.sum(e**2) / np.sum((oos_y - oos_bench)**2)
        pred_rows.append(dict(target=tg, method=m, pooled_spearman=stats.spearmanr(D[m], D[tg])[0],
                              cs_spearman_mean=rho.mean(), cs_months=len(rho), ts_spearman_mean=ts[m].mean(),
                              r2_pooled_loglog=r2, r2_within_loglog=r2w, r2_oos=r2oos,
                              mse_oos=np.mean(e**2), n_obs=len(D)))
        for k2, v2 in pred_rows[-1].items():
            if k2 not in ("target", "method"): rec("C_pred", tg, m, k2, v2)
    # DM tests: DRT vs each other method on OOS squared log error (per-month mean loss differential)
    eD = (oos_y - np.array(oos["DRT"]))**2
    for m in METH:
        if m == "DRT": continue
        em = (oos_y - np.array(oos[m]))**2
        dser = pd.Series(em - eD).groupby(oos_per).mean()       # >0 means DRT better
        tdm, T = nw_t(dser.values, HLAG[tg] + 1)
        rec("C_dm", tg, f"DRT_vs_{m}", "DM_t", tdm); rec("C_dm", tg, f"DRT_vs_{m}", "DM_p", 2 * stats.norm.sf(abs(tdm)))
        rec("C_dm", tg, f"DRT_vs_{m}", "mean_loss_diff", dser.mean())
        # paired test on cross-sectional rank correlation differential
        dd = (cs["DRT"] - cs[m]).values; tcs, T = nw_t(dd, HLAG[tg] + 1)
        rec("C_cs_paired", tg, f"DRT_vs_{m}", "mean_diff", np.nanmean(dd))
        rec("C_cs_paired", tg, f"DRT_vs_{m}", "NW_t", tcs); rec("C_cs_paired", tg, f"DRT_vs_{m}", "p", 2 * stats.norm.sf(abs(tcs)))
PRED = pd.DataFrame(pred_rows); PRED.to_csv("results/prediction_summary.csv", index=False)
print(PRED.pivot(index="method", columns="target", values="cs_spearman_mean").round(3))
print(PRED.pivot(index="method", columns="target", values="r2_oos").round(3))

# block bootstrap (resample 12-month blocks of dates) for pooled Spearman differences
def block_boot_pooled(D, tg, m1, m2, B=1000, blk=12):
    pers = np.array(sorted(D.period.unique())); nP = len(pers)
    grp = {p: g_.index.values for p, g_ in D.groupby("period")}
    a1 = D[m1].values; a2 = D[m2].values; y = D[tg].values
    pos = {i: np.r_[[D.index.get_loc(j) for j in grp[p]]] for i, p in enumerate(pers)}
    out = []
    for _ in range(B):
        starts = np.random.randint(0, nP - blk, size=int(np.ceil(nP / blk)))
        ids = np.concatenate([pos[i] for s0 in starts for i in range(s0, s0 + blk)])
        out.append(stats.spearmanr(a1[ids], y[ids])[0] - stats.spearmanr(a2[ids], y[ids])[0])
    return np.percentile(out, [2.5, 97.5]), np.mean(np.array(out) > 0)
boot_rows = []
for tg in ["fwd_ES63", "fwd_MDD63", "fwd_MDD252"]:
    D = P.dropna(subset=[tg]).reset_index(drop=True)
    for m in ["SD", "DD", "CVaR", "EWMA", "FHS"]:
        ci, share = block_boot_pooled(D, tg, "DRT", m, B=500)
        pt = stats.spearmanr(D["DRT"], D[tg])[0] - stats.spearmanr(D[m], D[tg])[0]
        boot_rows.append(dict(target=tg, comparison=f"DRT_minus_{m}", diff=pt, ci_lo=ci[0], ci_hi=ci[1], share_pos=share))
        rec("C_boot", tg, f"DRT_minus_{m}", "diff", pt); rec("C_boot", tg, f"DRT_minus_{m}", "ci_lo", ci[0]); rec("C_boot", tg, f"DRT_minus_{m}", "ci_hi", ci[1])
# per-asset time-series Spearman: DRT vs SD, Wilcoxon signed-rank across assets
for tg in ["fwd_ES63", "fwd_MDD63", "fwd_MDD252", "fwd_worst21"]:
    D = P.dropna(subset=[tg])
    ts = D.groupby("ticker").apply(lambda Gp: pd.Series({m: stats.spearmanr(Gp[m], Gp[tg])[0] for m in METH}))
    for m in ["SD", "DD", "CVaR", "EWMA"]:
        d = ts["DRT"] - ts[m]; w = stats.wilcoxon(d)
        rec("C_ts_wilcoxon", tg, f"DRT_vs_{m}", "share_assets_DRT_better", (d > 0).mean())
        rec("C_ts_wilcoxon", tg, f"DRT_vs_{m}", "median_diff", d.median()); rec("C_ts_wilcoxon", tg, f"DRT_vs_{m}", "p", w.pvalue)
BOOT = pd.DataFrame(boot_rows); BOOT.to_csv("results/prediction_bootstrap.csv", index=False); print(BOOT.round(3))

# crisis case study: risk readings at month-end before crises vs. what followed
crisis = []
for t, per in [("SPY", "2008-08"), ("SPY", "2020-01"), ("SPY", "1998-06"), ("SPY", "2007-09"), ("QQQ", "2000-02"), ("SPY", "2022-12"), ("SPY", "2025-02"), ("BTC-USD", "2021-10")]:
    q = P[(P.ticker == t) & (P.period == pd.Period(per))]
    if len(q): crisis.append(q.iloc[0][["ticker", "period"] + METH + ["fwd_ES63", "fwd_MDD63", "fwd_MDD252"]].to_dict())
pd.DataFrame(crisis).to_csv("results/crisis_snapshots.csv", index=False)

# ======================================================== D. VaR / ES BACKTESTS
print("D. backtests")
def kupiec(x, p):
    n, k = len(x), int(x.sum()); ph = k / n
    l0 = (n - k) * np.log(1 - p) + k * np.log(p)
    l1 = (n - k) * np.log(1 - ph) + (k * np.log(ph) if k > 0 else 0)
    return -2 * (l0 - l1)
def christoffersen(x):
    x = x.astype(int); a, b = x[:-1], x[1:]
    n00 = np.sum((a == 0) & (b == 0)); n01 = np.sum((a == 0) & (b == 1)); n10 = np.sum((a == 1) & (b == 0)); n11 = np.sum((a == 1) & (b == 1))
    p01 = n01 / max(n00 + n01, 1); p11 = n11 / max(n10 + n11, 1); p = (n01 + n11) / (n00 + n01 + n10 + n11)
    def ll(q, k0, k1): return (k0 * np.log(1 - q) if k0 else 0) + (k1 * np.log(q) if k1 and q > 0 else 0)
    l0 = ll(p, n00 + n10, n01 + n11); l1 = ll(p01, n00, n01) + ll(p11, n10, n11)
    return -2 * (l0 - l1)
VAR_P = 0.01; ES_P = 0.025
bt_rows = []; bt_series = {}
for t, c in COMP.items():
    r = c.r.values; N = len(r)
    if N < ZWIN + 300: continue
    W = swv(r, 252)                      # window ending at i: W[i-251]
    Zd = swv(np.nan_to_num(c.z_dn.values, nan=0.0), ZWIN); Zs = swv(np.nan_to_num(c.z_sym.values, nan=0.0), ZWIN)
    idx = np.arange(ZWIN, N - 1)         # forecast made at close i for day i+1
    w = W[idx - 251]; zd = Zd[idx - ZWIN + 1]; zs = Zs[idx - ZWIN + 1]
    mu = w.mean(1); sd = w.std(1, ddof=1); S = stats.skew(w, axis=1); K = stats.kurtosis(w, axis=1)
    zq = stats.norm.ppf(VAR_P); zcf = zq + (zq**2 - 1) * S / 6 + (zq**3 - 3 * zq) * K / 24 - (2 * zq**3 - 5 * zq) * S**2 / 36
    qd = np.quantile(zd, VAR_P, axis=1); qs = np.quantile(zs, VAR_P, axis=1)
    VaR = {"Normal-SD": -(mu + zq * sd), "Historical": -np.quantile(w, VAR_P, axis=1),
           "Cornish-Fisher": -(mu + zcf * sd), "EWMA-Normal": -zq * c.sig.values[idx],
           "FHS": -qs * c.sig.values[idx], "DRT": -qd * c.sdn.values[idx]}
    # ES 97.5
    ze = stats.norm.ppf(ES_P); phi = stats.norm.pdf(ze) / ES_P
    def es_rows(M, a):
        q = np.quantile(M, a, axis=1)[:, None]; msk = M <= q
        return -(np.where(msk, M, 0).sum(1) / msk.sum(1))
    ESf = {"Normal-SD": -(mu - phi * sd), "Historical": es_rows(w, ES_P), "EWMA-Normal": phi * c.sig.values[idx],
           "FHS": es_rows(zs, ES_P) * c.sig.values[idx], "DRT": es_rows(zd, ES_P) * c.sdn.values[idx]}
    VaRes = {"Normal-SD": -(mu + ze * sd), "Historical": -np.quantile(w, ES_P, axis=1), "EWMA-Normal": -ze * c.sig.values[idx],
             "FHS": -np.quantile(zs, ES_P, axis=1) * c.sig.values[idx], "DRT": -np.quantile(zd, ES_P, axis=1) * c.sdn.values[idx]}
    nxt = r[idx + 1]
    for m, v in VaR.items():
        hit = (nxt < -v); n_ = len(hit); k_ = hit.sum()
        lr_uc = kupiec(hit, VAR_P); lr_ind = christoffersen(hit); lr_cc = lr_uc + lr_ind
        row = dict(ticker=t, method=m, n=n_, exceed=int(k_), rate=k_ / n_, kupiec_p=stats.chi2.sf(lr_uc, 1),
                   chr_ind_p=stats.chi2.sf(lr_ind, 1), chr_cc_p=stats.chi2.sf(lr_cc, 2), avg_var=v.mean())
        if m in ESf:
            h2 = nxt < -VaRes[m]
            ratio = (-nxt[h2]) / ESf[m][h2]
            row.update(es_hits=int(h2.sum()), es_ratio=ratio.mean(),
                       es_ratio_t=(ratio.mean() - 1) / (ratio.std(ddof=1) / np.sqrt(len(ratio))) if len(ratio) > 2 else np.nan,
                       es_avg=ESf[m].mean())
        bt_rows.append(row)
    if t == "SPY":
        bt_series = dict(dates=c.index[idx + 1], r=nxt, **{f"VaR_{m}": v for m, v in VaR.items()})
BT = pd.DataFrame(bt_rows); BT.to_csv("results/var_es_backtests.csv", index=False)
BTs = BT.groupby("method").agg(assets=("ticker", "count"), mean_rate=("rate", "mean"), median_rate=("rate", "median"),
                                kupiec_pass=("kupiec_p", lambda x: (x > .05).mean()), ind_pass=("chr_ind_p", lambda x: (x > .05).mean()),
                                cc_pass=("chr_cc_p", lambda x: (x > .05).mean()), es_ratio=("es_ratio", "mean"),
                                es_ratio_pass=("es_ratio_t", lambda x: (x.dropna().abs() < 1.96).mean()),
                                avg_var=("avg_var", "mean"), avg_es=("es_avg", "mean"))
BTs.to_csv("results/var_es_backtest_summary.csv"); print(BTs.round(3))
for m, rw in BTs.iterrows():
    for k, v in rw.items(): rec("D_backtest", "all_assets", m, k, v)
for _, rw in BT[BT.ticker.isin(["SPY", "^GSPC", "QQQ", "TLT", "GLD", "BTC-USD", "NVDA"])].iterrows():
    for k in ["rate", "kupiec_p", "chr_ind_p", "chr_cc_p", "es_ratio"]:
        rec("D_backtest", rw.ticker, rw.method, k, rw[k])

# chart D: SPY VaR exceedances 2006-2010 and 2019-2021
fig, axs = plt.subplots(1, 2, figsize=(13, 4.2))
for ax_, (a0, a1) in zip(axs, [("2007-01-01", "2009-12-31"), ("2019-07-01", "2021-06-30")]):
    dts = bt_series["dates"]; msk = (dts >= a0) & (dts <= a1)
    ax_.bar(dts[msk], bt_series["r"][msk], color=GREY, width=1.5)
    ax_.plot(dts[msk], -bt_series["VaR_Normal-SD"][msk], color=RED, lw=1.4, label="99% VaR: normal, 1y SD")
    ax_.plot(dts[msk], -bt_series["VaR_DRT"][msk], color=NAVY, lw=1.4, label="99% VaR: DRT")
    ax_.set_title(f"SPY daily returns vs 99% VaR, {a0[:4]}-{a1[:4]}"); ax_.legend(frameon=False, fontsize=8)
    ax_.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
    import matplotlib.dates as mdates
    ax_.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7])); ax_.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
fig.savefig(CH + "08_spy_var_backtest.png"); plt.close()

# ======================================================== E. PORTFOLIO TEST
print("E. portfolios")
UNIV = ["SPY", "IWM", "EFA", "TLT", "IEF", "LQD", "GLD", "XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLU", "XLI", "XLB"]
R = pd.DataFrame({t: RET[t] for t in UNIV}).dropna()
CU = {t: components(R[t]) for t in UNIV}
SIG = pd.DataFrame({t: CU[t].sig for t in UNIV}); SDN = pd.DataFrame({t: CU[t].sdn for t in UNIV})
ZD = pd.DataFrame({t: CU[t].z_dn for t in UNIV}); ZS = pd.DataFrame({t: CU[t].z_sym for t in UNIV})
rf_d = (irx.reindex(R.index).ffill() / 100 / 252)
nA = len(UNIV); WMAX = 0.35
cons = ({"type": "eq", "fun": lambda w: w.sum() - 1},); bnds = [(0, WMAX)] * nA
def min_var(X):
    C = np.cov(X.T); return optimize.minimize(lambda w: w @ C @ w * 1e4, np.ones(nA) / nA, bounds=bnds, constraints=cons, method="SLSQP").x
def min_semi(X):
    f = lambda w: np.mean(np.minimum(X @ w, 0)**2) * 1e4
    return optimize.minimize(f, np.ones(nA) / nA, bounds=bnds, constraints=cons, method="SLSQP").x
def min_cvar(X, a):
    T = X.shape[0]; # vars: w (nA), zeta (1), u (T); min zeta + 1/(aT) sum u ; u >= -Xw - zeta, u>=0
    c = np.r_[np.zeros(nA), 1.0, np.ones(T) / (a * T)]
    A = np.hstack([-X, -np.ones((T, 1)), -np.eye(T)]); b = np.zeros(T)
    Aeq = np.r_[np.ones(nA), 0, np.zeros(T)][None, :]
    res = optimize.linprog(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=[1], bounds=[(0, WMAX)] * nA + [(None, None)] + [(0, None)] * T, method="highs")
    return res.x[:nA]
me_idx = pd.Series(np.arange(len(R)), index=R.index).groupby(R.index.to_period("M")).max()
starts = me_idx[me_idx >= ZWIN + 1]
W = {k: [] for k in ["EqualWeight", "MinVar (SD)", "MinSemiVar (DD)", "MinCVaR95 (hist)", "MinVar-EWMA", "MinFHS-ES", "MinDRT"]}
wdates = []
for per, i in starts.items():
    X = R.values[i - 251:i + 1]
    zd = ZD.values[i - ZWIN + 1:i + 1]; zs = ZS.values[i - ZWIN + 1:i + 1]
    Xd = zd * SDN.values[i]; Xs = zs * SIG.values[i]          # regime-rescaled scenarios
    Xe = R.values[i - 251:i + 1]; lw = LAM ** np.arange(251, -1, -1); lw /= lw.sum()
    Ce = np.cov(Xe.T, aweights=lw)
    W["EqualWeight"].append(np.ones(nA) / nA)
    W["MinVar (SD)"].append(min_var(X)); W["MinSemiVar (DD)"].append(min_semi(X))
    W["MinCVaR95 (hist)"].append(min_cvar(X, 0.05))
    W["MinVar-EWMA"].append(optimize.minimize(lambda w: w @ Ce @ w * 1e4, np.ones(nA) / nA, bounds=bnds, constraints=cons, method="SLSQP").x)
    W["MinFHS-ES"].append(min_cvar(Xs, 1 - ALPHA)); W["MinDRT"].append(min_cvar(Xd, 1 - ALPHA))
    wdates.append(i)
COST = 0.0005   # 5 bp per unit of turnover (one-way)
port = {}; turn = {}
for k, ws in W.items():
    ws = np.array(ws); out = pd.Series(0.0, index=R.index); tv = []
    prev = np.zeros(nA)
    for j, i in enumerate(wdates):
        end = wdates[j + 1] if j + 1 < len(wdates) else len(R) - 1
        seg = R.values[i + 1:end + 1]
        if len(seg) == 0: continue
        w0 = ws[j]; to = np.abs(w0 - prev).sum(); tv.append(to)
        wealth = np.cumprod(1 + seg, axis=0) * w0; val = wealth.sum(1)
        pr = np.r_[val[0], val[1:] / val[:-1]] - 1
        pr[0] -= COST * to
        out.iloc[i + 1:end + 1] = pr
        prev = wealth[-1] / wealth[-1].sum()
    port[k] = out.iloc[wdates[0] + 1:]; turn[k] = np.mean(tv[1:]) * 12
PR = pd.DataFrame(port); PR.to_csv("results/portfolio_daily_returns.csv")
rfp = rf_d.reindex(PR.index).fillna(0)
def perf(x, rf):
    ex = x - rf; ann = (1 + x).prod() ** (252 / len(x)) - 1; vol = x.std() * np.sqrt(252)
    dd = np.sqrt(np.mean(np.minimum(ex, 0)**2)) * np.sqrt(252)
    w = (1 + x).cumprod(); ddser = w / w.cummax() - 1
    m = (1 + x).resample("ME").prod() - 1
    return dict(CAGR=ann, Vol=vol, Sharpe=ex.mean() * 252 / vol, Sortino=ex.mean() * 252 / dd, MaxDD=-ddser.min(),
                Calmar=ann / -ddser.min(), CVaR95_daily=es_left(x.values, .05), CVaR99_daily=es_left(x.values, .01),
                Worst_day=-x.min(), Worst_month=-m.min(), Ulcer=np.sqrt(np.mean((100 * ddser)**2)),
                Skew=stats.skew(x), ExKurt=stats.kurtosis(x))
PERF = pd.DataFrame({k: perf(PR[k], rfp) for k in PR}).T
PERF["Turnover_pa"] = pd.Series(turn)
PERF.to_csv("results/portfolio_performance.csv"); print(PERF.round(4))
for m, rw in PERF.iterrows():
    for k, v in rw.items(): rec("E_portfolio", "16-ETF universe", m, k, v)
# sub-periods
subs = {"GFC 2008-09": ("2008-06-01", "2009-06-30"), "COVID 2020": ("2020-02-01", "2020-04-30"), "2022 bear": ("2022-01-01", "2022-12-31")}
SUB = {}
for nm, (a0, a1) in subs.items():
    x = PR.loc[a0:a1]; SUB[nm] = {k: ((1 + x[k]).prod() - 1) for k in PR}
    for k in PR:
        w = (1 + x[k]).cumprod(); SUB[nm + " MDD"] = SUB.get(nm + " MDD", {}); SUB[nm + " MDD"][k] = -(w / w.cummax() - 1).min()
SUB = pd.DataFrame(SUB); SUB.to_csv("results/portfolio_subperiods.csv"); print(SUB.round(3))
for m, rw in SUB.iterrows():
    for k, v in rw.items(): rec("E_subperiod", k, m, "value", v)
# stationary block bootstrap of performance differences (MinDRT minus others)
def stat_boot_idx(T, p=1/21):
    idx = np.empty(T, dtype=int); idx[0] = np.random.randint(T)
    for k in range(1, T):
        idx[k] = np.random.randint(T) if np.random.rand() < p else (idx[k - 1] + 1) % T
    return idx
B = 1000; Xv = PR.values; rfv = rfp.values; cols = list(PR.columns)
bs = {c: {"CVaR95": [], "MaxDD": [], "Sharpe": [], "Vol": [], "Sortino": []} for c in cols}
for b in range(B):
    ii = stat_boot_idx(len(PR))
    for j, c in enumerate(cols):
        x = Xv[ii, j]; ex = x - rfv[ii]; w = np.cumprod(1 + x)
        vol = x.std(); dn = np.sqrt(np.mean(np.minimum(ex, 0)**2))
        bs[c]["CVaR95"].append(es_left(x, .05)); bs[c]["MaxDD"].append(-(w / np.maximum.accumulate(w) - 1).min())
        bs[c]["Sharpe"].append(ex.mean() / vol * np.sqrt(252)); bs[c]["Vol"].append(vol * np.sqrt(252)); bs[c]["Sortino"].append(ex.mean() / dn * np.sqrt(252))
bt_out = []
for c in cols:
    if c == "MinDRT": continue
    for k in ["CVaR95", "MaxDD", "Sharpe", "Vol", "Sortino"]:
        d = np.array(bs["MinDRT"][k]) - np.array(bs[c][k])
        point = {"CVaR95": PERF.loc["MinDRT", "CVaR95_daily"] - PERF.loc[c, "CVaR95_daily"],
                 "MaxDD": PERF.loc["MinDRT", "MaxDD"] - PERF.loc[c, "MaxDD"], "Sharpe": PERF.loc["MinDRT", "Sharpe"] - PERF.loc[c, "Sharpe"],
                 "Vol": PERF.loc["MinDRT", "Vol"] - PERF.loc[c, "Vol"], "Sortino": PERF.loc["MinDRT", "Sortino"] - PERF.loc[c, "Sortino"]}[k]
        bt_out.append(dict(vs=c, metric=k, point_diff=point, ci_lo=np.percentile(d, 2.5), ci_hi=np.percentile(d, 97.5), p_le0=np.mean(d <= 0)))
        rec("E_boot", c, "MinDRT_minus", k, point); rec("E_boot", c, "MinDRT_minus", k + "_ci_lo", np.percentile(d, 2.5)); rec("E_boot", c, "MinDRT_minus", k + "_ci_hi", np.percentile(d, 97.5))
BB = pd.DataFrame(bt_out); BB.to_csv("results/portfolio_bootstrap.csv", index=False); print(BB.round(4))
# Also MinVar vs MinCVaR (hist) for context
# chart E: equity curves and drawdowns
fig, ax = plt.subplots(2, 1, figsize=(11, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]})
cols_plot = {"MinVar (SD)": RED, "MinSemiVar (DD)": GOLD, "MinCVaR95 (hist)": GREY, "MinDRT": NAVY, "EqualWeight": GREEN}
for k, col in cols_plot.items():
    w = (1 + PR[k]).cumprod(); ax[0].plot(w.index, w, color=col, lw=1.3, label=k)
    ax[1].plot(w.index, w / w.cummax() - 1, color=col, lw=1)
ax[0].set_yscale("log"); ax[0].legend(frameon=False, ncol=3, fontsize=8); ax[0].set_title("Out-of-sample growth of $1, minimum-risk portfolios (16 ETFs, monthly rebalance, 5bp costs)")
ax[1].set_title("Drawdown"); ax[1].yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
fig.savefig(CH + "09_portfolio_equity_drawdown.png"); plt.close()
# chart: results comparison (prediction)
fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
lab = {"fwd_ES63": "Next-3m tail loss (ES 5%)", "fwd_MDD63": "Next-3m max drawdown", "fwd_MDD252": "Next-12m max drawdown"}
colors = [RED, GOLD, GREY, "#6C757D", "#5DADE2", "#1F618D", NAVY]
for a_, tg in zip(ax, lab):
    q = PRED[PRED.target == tg].set_index("method").loc[METH]
    a_.bar(METH, q.r2_oos, color=colors); a_.set_title(lab[tg]); a_.set_ylabel("Out-of-sample R²")
    for i, v in enumerate(q.r2_oos): a_.text(i, v + .005, f"{v:.2f}", ha="center", fontsize=8)
    a_.tick_params(axis="x", rotation=45)
fig.suptitle("How well does each risk measure predict future pain? (48 assets, pooled, expanding-window calibration)", y=1.03, fontweight="bold")
fig.savefig(CH + "07_prediction_r2.png"); plt.close()
fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
for a_, tg in zip(ax, lab):
    q = PRED[PRED.target == tg].set_index("method").loc[METH]
    a_.bar(METH, q.cs_spearman_mean, color=colors); a_.set_title(lab[tg]); a_.set_ylabel("Avg cross-sectional Spearman ρ")
    for i, v in enumerate(q.cs_spearman_mean): a_.text(i, v + .005, f"{v:.2f}", ha="center", fontsize=8)
    a_.tick_params(axis="x", rotation=45)
fig.suptitle("Ranking assets by future pain: average monthly rank correlation", y=1.03, fontweight="bold")
fig.savefig(CH + "06_prediction_rank_corr.png"); plt.close()
# chart: DRT components for SPY
c = COMP["SPY"]; kap = pd.Series([es_left(c.z_dn.values[i - ZWIN + 1:i + 1], 1 - ALPHA) if i >= ZWIN else np.nan for i in range(len(c))], index=c.index)
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(c.index, c.r.rolling(252).std() * np.sqrt(252), color=RED, lw=1.2, label="Trailing 1-year SD (annualized)")
ax.plot(c.index, c.sdn * kap * np.sqrt(252) / 2.34, color=NAVY, lw=1, label="DRT, rescaled to SD units (÷2.34)")
ax.legend(frameon=False); ax.set_title("SPY: standard deviation is slow; DRT reacts to the regime and remembers the tail")
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0))
fig.savefig(CH + "10_spy_drt_vs_sd.png"); plt.close()
facts["spy_kappa_last"] = kap.iloc[-1]; facts["spy_kappa_median"] = kap.median(); facts["spy_kappa_min"] = kap.min(); facts["spy_kappa_max"] = kap.max()
facts["normal_ES975_multiplier"] = phi
kap_all = {t: es_left(COMP[t].z_dn.values[-ZWIN:], 1 - ALPHA) for t in COMP}
facts["kappa_latest_by_asset"] = kap_all
# Sharpe vs Sortino rank changes
sr = {}
for t in PANEL_ASSETS:
    r = RET[t].loc["2016-10-01":END]
    if len(r) < 2000: continue
    rf_ = (irx.reindex(r.index).ffill() / 100 / 252).fillna(0); ex = r - rf_
    sr[t] = dict(Sharpe=ex.mean() / r.std() * np.sqrt(252), Sortino=ex.mean() / np.sqrt(np.mean(np.minimum(ex, 0)**2)) * np.sqrt(252),
                 DD_SD=np.sqrt(np.mean(np.minimum(r, 0)**2)) / r.std(), Skew=stats.skew(r), MaxDD=mdd(r.values))
SR = pd.DataFrame(sr).T; SR["rank_Sharpe"] = SR.Sharpe.rank(ascending=False); SR["rank_Sortino"] = SR.Sortino.rank(ascending=False)
SR.to_csv("results/sharpe_vs_sortino_10y.csv")
facts["spearman_sharpe_sortino_10y"] = stats.spearmanr(SR.Sharpe, SR.Sortino)[0]
facts["max_rank_change"] = float((SR.rank_Sharpe - SR.rank_Sortino).abs().max())
facts["max_rank_change_ticker"] = (SR.rank_Sharpe - SR.rank_Sortino).abs().idxmax()

fig, ax = plt.subplots(figsize=(12, 4))
ks_ = pd.Series(kap_all).drop("^GSPC").sort_values()
ax.bar(ks_.index, ks_.values, color=NAVY); ax.axhline(phi, color=RED, ls="--", lw=1.5, label=f"Normal distribution: {phi:.2f}")
ax.set_ylim(2, ks_.max() + .3); ax.tick_params(axis="x", rotation=90); ax.legend(frameon=False)
ax.set_title("Tail multiplier κ (ES 97.5% of standardized down-shocks, last 3 years) vs. the normal assumption")
fig.savefig(CH + "11_kappa_by_asset.png"); plt.close()
json.dump(facts, open("results/stylized_facts.json", "w"), indent=2, default=lambda o: float(o) if np.isscalar(o) else str(o))
pd.DataFrame(RES).to_csv("results.csv", index=False)
print("done; results rows:", len(RES))
